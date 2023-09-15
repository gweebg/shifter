from datetime import date
from typing import Optional

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement

import src.lib.scraper.elements as elements
from src.lib.exceptions import YearOutOfBoundsException, CourseNameDoesNotExistException
from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule, ScheduleGroup


class ScheduleScraper:
    """
    TODO: Catch connection errors for graceful shutdown.

    This class is responsible for scraping the web for the desired schedules that are specified by a name,
    a date string and the school years to get.

    :param is_headless: This boolean is used for debugging, and runs selenium in a non-headless mode.
    :type is_headless: bool
    """
    def __init__(self, is_headless: bool = True) -> None:
        """
        Class constructor.
        """

        self.__url: str = "https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx"
        self.__fetched: bool = False
        self.options: FirefoxOptions = FirefoxOptions()

        if is_headless:
            self.options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=self.options)  # Selenium driver set-up.

    def get_courses(self) -> list[str]:
        """
        Method that returns the list of every course on present on the scraped schedule list.
        :return: List containing the name of every course.
        :rtype: list[str]
        """

        if not self.__fetched:
            self.driver.get(self.__url)
            self.__fetched = True

        courses: list[WebElement] = self.driver.find_elements(by=By.CLASS_NAME, value="rcbItem")
        return list(map(lambda item: item.get_property("innerText"), courses))

    def _get_single(self, year: int, date_str: str, formatted: bool, parser: ScheduleParser) -> Optional[
        str | Schedule]:
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

            # Click on the button to get the page of schedule.
            search = self.driver.find_element(By.ID, elements.search_button)
            search.click()

            # Click on the year select button.
            year_input = self.driver.find_element(By.ID, elements.year_to_id[year])
            year_input.click()

            # Select the date when the schedule came out.
            date_input = self.driver.find_element(By.ID, elements.date_bar)  # Date format : dd-mm-YYYY
            date_input.clear()
            date_input.send_keys(date_str)

            # Expand schedule in order to get the full html document, it also acts like a search button.
            expand = self.driver.find_element(By.ID, elements.expand_check)

            if not expand.get_property("checked"):
                expand.click()

            page_content: str = self.driver.page_source

        except NoSuchElementException:  # If the provided year does not exist then we can't scrape the page.
            raise YearOutOfBoundsException(f"The course doesn't have an year {year}.")

        finally:  # Go to the previous page in case we want to scrape any more years.
            self.driver.back()

        if formatted:  # If we want the result as a Schedule object.
            parsed_content: Schedule
            try:
                parsed_content = parser.parse(page_content)
                return parsed_content  # Return the parsed schedule.

            except IndexError:  # If we can't parse the schedule scraped, then it doesn't exist yet.
                return None

        return page_content

    def get(self, course_name: str, parser: ScheduleParser, date_str: Optional[str] = None, year: Optional[int] = None,
            formatted: bool = True) -> Optional[ScheduleGroup]:
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

        self.driver.get(self.__url)  # Getting the page.
        self.__fetched = True

        if course_name not in self.get_courses():  # Throwing an error if the course name doesn't exist.
            raise CourseNameDoesNotExistException(f"Course '{course_name}' does not exist.")

        result: ScheduleGroup = ScheduleGroup(course_name=course_name)

        if not date_str:  # If no date is specified we use the today's date.
            date_str: str = date.today().strftime("%d-%m-%Y")  # Current date.

        # Getting the course schedule page.
        course_name_input = self.driver.find_element(By.NAME, elements.search_bar)
        course_name_input.send_keys(course_name)

        if not year:  # If year is not specified we fetch every year possible.
            for y in range(1, 5):

                try:  # Parsing the schedule for the current year (y).
                    content: Optional[str | Schedule] = self._get_single(date_str=date_str, year=y, formatted=formatted,
                                                                         parser=parser)
                    if content is None:  # If content is None then we abort since there are no schedule for the provided date.
                        return None

                    result.add_event_to_year(y, content)

                except YearOutOfBoundsException:
                    break  # Stop iterating once there are no more years parsable.

        else:  # If the year is specified, then we get only that year.
            content: Optional[str | Schedule] = self._get_single(date_str=date_str, year=year, formatted=formatted, parser=parser)

            if content is None:
                return None

            result.add_event_to_year(year, content)

        return result

    def close(self) -> None:
        self.driver.close()
        self.driver.quit()

