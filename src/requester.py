# Outside libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from jellyfish import levenshtein_distance

# Built-in libraries
import os
import datetime

# Local modules
from elements import *

# ASP form webpage to scrape.
URL: str = "https://alunos.uminho.pt/pt/estudantes/paginas/infouteishorarios.aspx"

year_to_id: dict = {'1': first_year,
                    '2': second_year,
                    '3': third_year,
                    '4': fourth_year}

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--headless") # Makes a silent scrape by not showing the browser.

chrome_service = Service(ChromeDriverManager().install())


class InvalidParameter(Exception):
    pass


def check_date(date: str) -> bool:
    """
    Checks if a date string is formatted in the format '%d-%m-%Y'.

    :param date: Date string passed to the function.
    :return: True if it's in the correct format, False otherwise.
    """

    try:
        datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        return False

    return True


def check_course_parameters(course_name: str, year: str, date: str) -> None:
    """
    Checks if the parameters couse_name, year and date are valid for the function schedule_lookup.

    :param course_name: The course name to lookup.
    :param year: The school year of the schedule.
    :param date: Date of the day we make the request.

    :raises InvalidParameter: If one of the three parameters is invalid.
    """

    distances = {}

    with open('./docs/course_names.txt', 'r', encoding='utf-8') as file:

        for line in file:
            dist: float = 1 - (levenshtein_distance(line, course_name) / float(max(len(line), len(course_name))))
            distances[line] = dist

    best_match = max(distances, key=distances.get)
    # print(best_match, distances[best_match])

    if distances[best_match] >= 0.95:
        if int(year) in range(1, 4):
            if check_date(date):
                return
            else:
                raise InvalidParameter("Date not valid: Date must use the format dd-mm-YYYY.")
        else:
            raise InvalidParameter("Year not valid: Year has to be a values between 1 and 4 (inclusive).")

    elif distances[best_match] >= 0.80:
        stripped = best_match.replace('\n', "")
        raise InvalidParameter(f"Course name not found: Did you mean '{stripped}' ?")

    else:
        raise InvalidParameter("Course name not found: You can check every course name at "
                        "https://www.uminho.pt/PT/ensino/oferta-educativa/paginas/licenciaturas-e-mestrados"
                        "-integrados.aspx")


def schedule_lookup(course_name: str, year: str, date: str) -> str:
    """
    Downloads the schedule web page corresponding to the given parameters.

    :param course_name: The course name to lookup.
    :param year: The school year of the schedule.
    :param date: Date of the day we make the request.

    :return: The file location for the downloaded page.
    :rtype: str
    """

    file_name = course_name.replace('\n', '').replace(' ', '_').lower() + '_' + date + '_' + year + '.html'
    for file in os.listdir('./schedules/'):
        if file == file_name:
            print(f"Found an existing file for the given parameters: {file}")
            print("Skipping fetch and continuing with stored file...")
            return './schedules/' + file

    check_course_parameters(course_name, year, date)

    # Setting up a chrome environment with the parameters above.
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    driver.get(URL)

    # Enter the course name onto the text input bar.
    text_input = driver.find_element(By.NAME, search_bar)
    text_input.send_keys(course_name)

    # Click on the button to get the page of schedule.
    search = driver.find_element(By.ID, search_button)
    search.click()

    # Click on the year select button.
    year_input = driver.find_element(By.ID, year_to_id[year])
    year_input.click()

    # Select the date when the schedule came out.
    date_input = driver.find_element(By.ID, date_bar)  # Date format : dd-mm-YYYY
    date_input.clear()
    date_input.send_keys(date)

    # Expand schedule in order to get the full html document, it also acts like a search button.
    expand = driver.find_element(By.ID, expand_check)
    expand.click()

    formatted_filename = f'./schedules/{file_name}'
    with open(formatted_filename, 'w', encoding='utf-8') as file:
        file.write(driver.page_source)

    driver.close()
    driver.quit()

    return formatted_filename
