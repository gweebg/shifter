from typing import Optional

from fastapi import APIRouter, HTTPException, Response

from src.api.models.convert_request import ConvertRequest
from src.api.models.schedule_request import ScheduleRequest
from src.api.models.schedule_response import ScheduleResponse

from src.lib.builder.builder import Builder
from src.lib.builder.builder_factory import BuilderFactory
from src.lib.builder.ical.ical_builder import IcalBuilder
from src.lib.builder.json.json_builder import JsonBuilder
from src.lib.builder.xlsx.xlsx_builder import XlsxBuilder

from src.lib.cache.ttl_cache import Cache

from src.lib.exceptions import YearOutOfBoundsException, CourseNameDoesNotExistException

from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import ScheduleGroup, Schedule
from src.lib.scraper.scraper import ScheduleScraper

router: APIRouter = APIRouter(
    prefix="/shifter",
    tags=["shifter"],
)

scraper: ScheduleScraper = ScheduleScraper(is_headless=True)  # Scraper
parser: ScheduleParser = ScheduleParser()  # Parser
cache: Cache = Cache("debug.db")  # Cache

builder_factory: BuilderFactory = BuilderFactory()  # Builder
builder_factory.register_builder("xlsx", XlsxBuilder)
builder_factory.register_builder("ics", IcalBuilder)
builder_factory.register_builder("json", JsonBuilder)


def cached_get(
        body: ScheduleRequest,
        cache_obj: Cache,
        scraper_obj: ScheduleScraper,
        parser_obj: ScheduleParser) -> Optional[ScheduleGroup]:
    schedules: Optional[ScheduleGroup]

    if cache_obj.has(key=body.cache_key):  # If value is already cached we use it.
        schedules = cache_obj.get(key=body.cache_key)

    else:  # Otherwise we scrape the schedule and built the response from it.

        schedules = scraper_obj.get(
            course_name=body.course_name,
            year=body.actual_year,
            date_str=body.course_date,
            parser=parser_obj
        )

        if schedules is not None:  # No schedule was found for the given date.
            cache_obj.set(body.cache_key, schedules)  # Only saving to cache if result is not None.

    return schedules


@router.get("/courses")
async def get_course_names() -> list[str]:
    """
    This function is the handler for GET requests to '/courses'.
    :return: The name of every course available at the institution.
    :rtype: list[str]
    """
    if cache.has(key="courses"):
        return cache.get(key="courses")

    course_name_list: list[str] = scraper.get_courses()
    cache.set("courses", course_name_list)

    return course_name_list


@router.post("/schedule/", response_model=ScheduleResponse)
async def fetch_schedule(body: ScheduleRequest) -> ScheduleResponse:
    """
    This function represents the API endpoint '/schedule/' for POST requests.
    The server must receive as the body a JSON object compliant with ScheduleRequest.

    :param body: The body (as json) received from the client.
    :type body: ScheduleRequest
    """

    try:

        schedules: Optional[ScheduleGroup] = cached_get(
            body=body,
            cache_obj=cache,
            scraper_obj=scraper,
            parser_obj=parser
        )

        if schedules is None:  # No schedule was found for the given date.
            raise HTTPException(status_code=404,
                                detail=f"No schedule found for {body.course_name} at {body.course_date}")

    except YearOutOfBoundsException:  # The provided course_year does not exist for the specified course.
        raise HTTPException(status_code=400,
                            detail=f"The course {body.course_name} doesn't have an year {body.course_year}")

    except CourseNameDoesNotExistException:  # Somehow the course name doesn't exist.
        raise HTTPException(status_code=404, detail=f"The course {body.course_name} does not exist")

    # Building final response if everything went ok.
    response: ScheduleResponse = ScheduleResponse(
        course_name=body.course_name,
        course_date=body.course_date,
        schedules=schedules.as_dict(),
        shifts=schedules.shifts
    )

    return response


@router.post("/schedule/convert/")
async def convert_schedule(request: ConvertRequest):
    """
    This function handles the POST requests to /schedule/convert/, the request must be formatted as a ConvertRequest.
    This function when given a schedule and shifts, filters the shifts and converts the schedule into the specified
    format (xlsx, ics, json).

    :param request: The body of the post request.
    :type request: ConvertRequest
    """

    try:

        schedules: Optional[ScheduleGroup] = cached_get(
            body=request.body,
            cache_obj=cache,
            scraper_obj=scraper,
            parser_obj=parser
        )

        if schedules is None:  # No schedule was found for the given date.
            raise HTTPException(status_code=404,
                                detail=f"No schedule found for {request.body.course_name} at {request.course_date}")

    except YearOutOfBoundsException:  # The provided course_year does not exist for the specified course.
        raise HTTPException(status_code=400,
                            detail=f"The course {request.body.course_name} doesn't have an year {request.body.course_year}")

    except CourseNameDoesNotExistException:  # Somehow the course name doesn't exist.
        raise HTTPException(status_code=404, detail=f"The course {request.body.course_name} does not exist")

    # Filtering the schedules by the provided shifts.
    used_schedules: list[Schedule] = []

    year: int
    shifts: dict[str, list[str]]
    for year, shifts in request.shifts.items():
        used_schedules.append(schedules.years[year].filter(shifts))

    # Obtaining the correct builder for the specified format type.
    builder: Builder = builder_factory.create(
        str(request.fmt.value),  # json | xlsx | ical
        schedule=used_schedules
    )

    result: bytes = builder.build()  # Converting the schedule into its respective format.

    response: Response = Response(content=result)
    response.headers["Content-Type"] = f"application/{builder.content_type}"  # Defining content type.
    response.headers["Content-Disposition"] = f'attachment; filename="schedule.{str(request.fmt.value)}"'  # Filename.

    return response


router.add_event_handler("shutdown", lambda: scraper.close())
