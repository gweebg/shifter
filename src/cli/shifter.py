from datetime import datetime

import questionary
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text

from src.lib.builder.builder import Builder
from src.lib.builder.builder_factory import BuilderFactory
from src.lib.builder.ical.ical_builder import IcalBuilder
from src.lib.builder.json.json_builder import JsonBuilder
from src.lib.builder.xlsx.xlsx_builder import XlsxBuilder
from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule, ScheduleGroup
from src.lib.scraper.scraper import ScheduleScraper

FIRST_SEMESTER_DATE: str = "01-11-2023"
SECOND_SEMESTER_DATE: str = "01-03-2024"


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def title_case_except(words: str, exceptions: list[str]) -> str:
    return " ".join(
        word.capitalize() if word.lower() not in exceptions else word
        for word in words.split()
    )


def prompt_semester() -> str:
    r_semester: str = questionary.select(
        "Choose the semester",
        choices=[
            f"1st semester ({FIRST_SEMESTER_DATE})",
            f"2nd semester ({SECOND_SEMESTER_DATE})",
            "Insert custom date",
        ],
    ).ask()

    if r_semester == "Insert custom date":
        return questionary.text(
            "New date", validate=validate_date, instruction="dd-mm-YYYY"
        ).ask()

    return FIRST_SEMESTER_DATE if r_semester.startswith("1") else SECOND_SEMESTER_DATE


def main() -> None:
    builder_factory: BuilderFactory = BuilderFactory()
    builder_factory.register_builder("xlsx", XlsxBuilder)
    builder_factory.register_builder("ics", IcalBuilder)
    builder_factory.register_builder("json", JsonBuilder)

    exceptions: list[str] = ["e", "de", "da", "do", "das", "dos", "em", "na", "para"]

    console = Console()
    parser: ScheduleParser = ScheduleParser()
    progress = Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        transient=True,
    )

    semester: str = prompt_semester()

    with progress as p:
        task = p.add_task("Fetching courses", total=None, start=False)
        scraper: ScheduleScraper = ScheduleScraper(is_headless=True)
        course_names: list[str] = scraper.get_courses()

    course_name: str = questionary.autocomplete(
        "Choose your course",
        choices=course_names,
        validate=lambda val: val in course_names,
    ).ask()

    with progress as p:
        p.remove_task(task_id=task)
        task = p.add_task("Downloading schedule", total=None, start=False)

        schedule: ScheduleGroup = scraper.get(
            course_name=course_name,
            formatted=True,
            date_str=semester,
            parser=parser,
        )

    if not schedule:
        error_msg = Text(
            "Schedule is empty or doesn't exist, try using a different semester date."
        )
        error_msg.stylize("bold red")
        console.print(error_msg)
        return

    year: int = int(
        questionary.select(
            "Choose years",
            choices=list(map(lambda val: str(val), schedule.years.keys())),
        ).ask()
    )

    shifts: dict[int, dict[str, list[str]]] = schedule.shifts[year]
    confirm: bool = False
    while not confirm:
        console.print(f" [underline]Year {year}")

        for c in shifts:
            shifts[c] = (
                questionary.checkbox(
                    title_case_except(c, exceptions),
                    choices=schedule.shifts[year][c],
                    instruction="",
                ).ask()
                or []
            )

        table = Table(title="Selected Shifts")

        table.add_column("Class Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("Shifts", style="magenta")

        for c in shifts:
            table.add_row(title_case_except(c, exceptions), ", ".join(shifts[c]) or "-")

        console.print(table)
        confirm = questionary.confirm("Is everything correct ?").ask()

    filtered_schedule: Schedule = schedule.years[year].filter(shifts)

    formats: list[str] = questionary.checkbox(
        "Download schedules as", choices=["xlsx", "json", "ics"]
    ).ask()

    path: str = (
        questionary.path("Save path", only_directories=True, default=".").ask() or "."
    )

    progress = Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
    )

    for fmt in formats:
        with progress as p:
            task = p.add_task(
                f"Generating {path}/schedule.{fmt}",
                total=None,
            )

            builder: Builder = builder_factory.create(fmt, schedule=filtered_schedule)
            content: bytes = builder.build()

            with open(f"{path}/schedule.{fmt}", "wb") as file:
                file.write(content)

    scraper.close()


if __name__ == "__main__":
    SystemExit(main())
