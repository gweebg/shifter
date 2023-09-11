from datetime import date
from typing import Optional

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement

import src.lib.elements as elements
from src.lib.exceptions import YearOutOfBoundsException, CourseNameDoesNotExistException
from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule


class ScheduleScraper:

    def __init__(self, is_headless: bool = True) -> None:

        self.__url: str = "https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx"
        self.options: FirefoxOptions = FirefoxOptions()

        if is_headless:
            self.options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=self.options)
        self.driver.get(self.__url)

    def _get_courses(self) -> list[str]:

        courses: list[WebElement] = self.driver.find_elements(by=By.CLASS_NAME, value="rcbItem")
        return list(map(lambda item: item.get_property("innerText"), courses))

    def _get_single(self, year: int, date_str: str, formatted: bool, parser: ScheduleParser) -> str | Schedule:

        page_content: str = ""

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

            page_content = self.driver.page_source

        except NoSuchElementException:
            raise YearOutOfBoundsException(f"The course doesn't have an year {year}.")

        finally:
            self.driver.back()

        return page_content if not formatted else parser.parse(page_content)

    def get(self, course_name: str, parser: ScheduleParser, date_str: Optional[str] = None, year: Optional[int] = None,
            formatted: bool = True) -> dict:

        if course_name not in self._get_courses():
            raise CourseNameDoesNotExistException(f"Course '{course_name}' does not exist.")

        result: dict = {course_name: {}}

        if not date_str:
            date_str: str = date.today().strftime("%d-%m-%Y")  # Current date.

        course_name_input = self.driver.find_element(By.NAME, elements.search_bar)
        course_name_input.send_keys(course_name)

        if not year:
            for y in range(1, 5):

                try:
                    content: str | Schedule = self._get_single(date_str=date_str, year=y, formatted=formatted,
                                                               parser=parser)
                    result[course_name][y] = content

                except YearOutOfBoundsException:
                    break

        else:
            content: str = self._get_single(date_str=date_str, year=year, formatted=formatted, parser=parser)
            result[course_name][year] = content

        self.driver.close()
        self.driver.quit()

        return result
