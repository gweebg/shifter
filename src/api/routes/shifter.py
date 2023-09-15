from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from src.api.models.schedule_request import ScheduleRequest
from src.api.models.schedule_response import ScheduleResponse
from src.lib.cache.ttl_cache import Cache
from src.lib.exceptions import YearOutOfBoundsException, CourseNameDoesNotExistException
from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule, ScheduleGroup
from src.lib.scraper.scraper import ScheduleScraper

router: APIRouter = APIRouter(
    prefix="/shifter",
    tags=["shifter"],
)

parser: ScheduleParser = ScheduleParser()
scraper: ScheduleScraper = ScheduleScraper(is_headless=True)
cache: Cache = Cache("debug.db")


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
async def fetch_schedule(body: ScheduleRequest):
    """
    This function represents the API endpoint '/schedule/' for POST requests.
    The server must receive as the body a JSON object compliant with ScheduleRequest.

    :param body: The body (as json) received from the client.
    :type body: ScheduleRequest
    """

    course_year: Optional[int] = None if body.course_years == 0 else body.course_years  # Normalize the course year.
    schedules: Optional[ScheduleGroup]

    if cache.has(key=body.cache_key):  # If value is already cached we use it.
        schedules = cache.get(key=body.cache_key)

    else:  # Otherwise we scrape the schedule and built the response from it.

        try:

            schedules = scraper.get(
                course_name=body.course_name,
                year=course_year,
                date_str=body.course_date,
                parser=parser
            )

            if schedules is None:  # No schedule was found for the given date.
                raise HTTPException(status_code=404,
                                    detail=f"No schedule found for {body.course_name} at {course_date}")

            cache.set(body.cache_key, schedules)  # Only saving to cache if result is not None.

        except YearOutOfBoundsException:  # The provided course_year does not exist for the specified course.
            raise HTTPException(status_code=400,
                                detail=f"The course {body.course_name} doesn't have an year {course_year}")

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
