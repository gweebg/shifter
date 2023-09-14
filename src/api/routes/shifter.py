from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.lib.cache.ttl_cache import Cache
from src.lib.scraper.parser import ScheduleParser
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

    if cache.has(key="courses"):
        return cache.get(key="courses")

    course_name_list: list[str] = scraper.get_courses()
    cache.set("courses", course_name_list)

    return course_name_list
