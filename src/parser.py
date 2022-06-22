# Outside libraries
import cchardet # Do not remove.
from bs4 import BeautifulSoup
from bs4.element import ResultSet

# Built-in libraries
from typing import List

# Local modules
# from generator import generate_schedule
from requester import schedule_lookup
from elements import table_class, HOURS


class ParsingError(Exception):
    """
    Custom exception for parsing errors.
    """
    pass


def get_weekdays(soup: BeautifulSoup) -> List[str]:
    """
    Returns a list with the work days of a schedule.

    :param soup: BeautifulSoup object in which to look.
    :return: List containing every occupied weekday.
    :rtype: List[str]
    """

    table = (soup.find_all("table", class_="rsHorizontalHeaderTable"))[0]
    weekdays = table.find_all("a")

    result: List[str] = [day.text.title() for day in weekdays]

    return result


def get_time(style: str) -> float:
    """
    Returns the 'time' value from a html style string based on the height parameter.

    :param style: String containing every style values.
    :return: The extracted time value.
    :rtype: float
    """

    position: int = style.find("height")

    if position != -1:
        height_string: str = style[position + 7: position + 10]
        return 1.0 if height_string == "116" else 2.0
    else:
        return 0.0


def get_shift(title: str) -> str:
    """
    Returns the shift from a schedule block title.

    :param title: Title of the block.
    :return: A string containing the shift value (e.g. 'PL9', 'TP1', ...).
    :rtype: str
    """

    # Title example: "Redes de Computadores\n [CG - Edificio 2 - 0.28]\n T2"
    title: List[str] = title.split("\n")
    return title[2]


def get_name(title: str) -> str:
    """
    Returns the course name value from a schedule block title.

    :param title: Title of the block.
    :return: A string containing the course name value.
    :rtype: str
    """

    return title.split("\n")[0].strip()


def parse_schedule(course_name: str, year: str, date: str, shifts: dict | None = None) -> dict:
    """
    Downloads the schedule html page using 'schedule_lookup' and parses it into a dict representing the schedule.

    :param course_name: The course name to lookup.
    :param year: The school year of the schedule.
    :param date: Date of the day we make the request.
    :param shifts: Optional parameter, if provided filters for shifts on dict.

    :return: The dictionary containing a representation of the schedule.
    :raises ParsingError: If there's an error while parsing the html page.
    """

    # File path where the html for the schedule is stored.
    schedule_filename: str = schedule_lookup(course_name, year, date)

    # Each <tr> element represents a line on the schedule, this means that for each <tr> we go 30 minutes in the day.

    with open(schedule_filename, encoding = 'utf-8') as fp:
        soup: BeautifulSoup = BeautifulSoup(fp, "lxml")

    items: ResultSet = soup.find_all("table", {"class": table_class})[0].find_all("tr")

    print(f"Loaded file {schedule_filename} successfully!")

    # We are returning this dictionary when it's populated.
    all_subjects = {
        "Segunda-Feira": [],
        "Terça-Feira": [],
        "Quarta-Feira": [],
        "Quinta-Feira": [],
        "Sexta-Feira": []
    }

    # Time and weekday control variables.
    cw: int = 0
    ch: int = 0

    print("Started parsing the schedule.")

    # In this type of schedules the days are divided in <td> elements and the time is divided in <tr> elements.
    for tr in items:

        tds: ResultSet = tr.find_all("td")

        # For each <td> we advance one weekday.
        for td in tds:

            weekdays: List[str] = get_weekdays(soup)  # List of weekdays present in the schedule.
            cw = 0 if cw == len(weekdays) - 1 else cw + 1  # Updating weekday counter.

            # Each schedule entry is stored inside a div containing its style, height and title.
            if divs := td.find_all("div", class_="rsApt rsAptSimple"):

                for subject in divs:
                    style: str = subject['style']  # 'style' parameter contains height of block.
                    duration: float = get_time(style)   # We can infer the duration of class using the block height.

                    if duration > 0.0:
                        title: str = subject['title']   # Formatted like 'subject_name [where - building - room] shift'
                        shift: str = get_shift(title)

                        if shift is None:
                            raise ParsingError("An error has occured while parsing shift string.")

                        # Entry for the all_subjects dict, contains information about a block in a schedule.
                        entry: dict = {
                            "title": title,
                            "shift": shift,
                            "duration": duration,
                            "weekday": weekdays[cw - 1],
                            "starts_at": HOURS[ch]
                        }

                        if shifts:  # If we provide the shifts' parameter we select the shifts we want to store.
                            try:
                                if shift in shifts[get_name(title)]:
                                    all_subjects[weekdays[cw - 1]].append(entry)

                            except KeyError:
                                print(f"Invalid | Missing subject from provided shifts: [{title}]")
                                print("Skipping block...")

                        else:   # Else we dump it all.
                            all_subjects[weekdays[cw - 1]].append(entry)

        # Updating hour counter.
        ch = 0 if ch == len(HOURS) - 1 else ch + 1

    print("Finished parsing!")
    return all_subjects
