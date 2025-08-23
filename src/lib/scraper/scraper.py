from datetime import date
from typing import Optional

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement

import src.lib.scraper.elements as elements
from src.lib.exceptions import (
    CourseNameDoesNotExistException,
    EmptyScheduleException,
    YearOutOfBoundsException,
)
from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule, ScheduleGroup

from result import Result, Ok, Err


class ScheduleScraper:
    """
    This class is responsible for scraping the web for the desired schedules that are specified by a name,
    a date string and the school years to get.

    :param is_headless: This boolean is used for debugging, and runs selenium in a non-headless mode.
    :type is_headless: bool
    """

    def __init__(self, url: Optional[str], headless: bool = True) -> None:
        self.__url: str = (
            url
            or "https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx"
        )
        self.__fetched: bool = False
        self.options: FirefoxOptions = FirefoxOptions()

        if headless:
            self.options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=self.options)  # webdriver set-up

    def get_courses(self) -> list[str]:
        """
        Return a list of every available course on the schedules page.
        :return: list of course names
        :rtype: list[str]
        """
        if not self.__fetched:
            self.driver.get(self.__url)
            self.__fetched = True

        courses: list[WebElement] = self.driver.find_elements(
            by=By.CLASS_NAME, value="rcbItem"
        )
        return list(map(lambda item: item.get_property("innerText"), courses))

    def __get_single(
        self, year: int, date_str: str, parser: ScheduleParser
    ) -> Result[Schedule, BaseException]:
        """
        This private method is responsible for getting an actual schedule and parsing it into a Schedule object if
        indicated.
        :param year: Wanted school year.
        :type year: int
        :param date_str: From what date to scrape the schedule.
        :type date_str: str
        :param formatted: Indicates whether we want the result as a raw html string or formatted as a Schedule.
        :type formatted: bool
        :param parser: Dependency injected to parse the raw html content into a Schedule object.
        :type parser: ScheduleParser
        :return: None if there still isn't a published schedule, raw html string if formatted is false, Schedule
            object if formatted is true.
        :rtype: Optional[str | Schedule]
        """

        try:
            search = self.driver.find_element(By.ID, elements.search_button)
            search.click()  # click the search button

            year_input = self.driver.find_element(By.ID, elements.year_to_id[year])
            year_input.click()  # click the year radio button

            date_input = self.driver.find_element(By.ID, elements.date_bar)
            date_input.clear()
            date_input.send_keys(date_str)  # write out the date on the date field

            expand = self.driver.find_element(By.ID, elements.expand_check)
            if not expand.get_property("checked"):
                expand.click()  # click expand checkbox if not yet

            page_content: str = self.driver.page_source

        except NoSuchElementException:
            return Err(YearOutOfBoundsException(f"year {year} not found"))

        finally:  # reset page to year selection
            self.driver.back()
            self.driver.back()

        try:
            sched: Schedule = parser.parse(page_content)
            return Ok(sched)

        except IndexError:  # schedule page exist but it hasn't been posted yet
            return Err(
                EmptyScheduleException("schedule hasn't been posted yet, page is blank")
            )

    def get(
        self,
        course_name: str,
        parser: ScheduleParser,
        date_str: Optional[str] = None,
        year: Optional[int] = None,
    ) -> Result[ScheduleGroup, BaseException]:
        """
        This method is the main method of this class, it handles the fetching, scraping and parsing of the schedule
        based on the given parameters.

        :param course_name: Name of the course.
        :type course_name: str
        :param parser: Dependency injected parser, only used if formatted is true.
        :type parser: ScheduleParser
        :param date_str: Date of the schedule.
        :type date_str: str
        :param year: Year of the course.
        :type year: int
        :param formatted: Indicates whether we want the result as a raw html string or formatted as a Schedule.
        :type formatted: bool
        :return: ScheduleGroup object containing all the scraped content if everything went well, None if the schedule
            doesn't exist.
        :rtype: Optional[ScheduleGroup]
        """

        if not self.__fetched:
            self.driver.get(self.__url)
            self.__fetched = not self.__fetched

        if course_name not in self.get_courses():
            return Err(
                CourseNameDoesNotExistException(f"course {course_name} does not exist")
            )

        result = ScheduleGroup(course_name)

        if not date_str:  # if no date is specified we use today's date
            date_str: str = date.today().strftime("%d-%m-%Y")

        # search for the course name
        course_name_input = self.driver.find_element(By.NAME, elements.search_bar)
        course_name_input.send_keys(course_name)

        if not year:  # if year is not specified we fetch every year possible.
            for y in range(1, 5):
                content: Result[Schedule, BaseException] = self.__get_single(
                    y, date_str, parser
                )

                if content.is_err() and content.err_value:
                    return Err(content.err_value)

                result.add_event_to_year(y, content)

        else:  # If the year is specified, then we get only that year.
            content: Optional[str | Schedule] = self.get_single(
                date_str=date_str, year=year, parser=parser
            )

            if content is None:
                return None

            result.add_event_to_year(year, content)

        return result

    def close(self) -> None:
        self.driver.quit()
