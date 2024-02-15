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


def main():
    builder_factory: BuilderFactory = BuilderFactory()  # Builder
    builder_factory.register_builder("xlsx", XlsxBuilder)
    builder_factory.register_builder("ics", IcalBuilder)
    builder_factory.register_builder("json", JsonBuilder)

    parser: ScheduleParser = ScheduleParser()
    scraper: ScheduleScraper = ScheduleScraper(is_headless=True)

    course_name: str = "Licenciatura em Estudos Portugueses"
    schedule: ScheduleGroup = scraper.get(
        course_name=course_name,
        formatted=True,
        date_str=SECOND_SEMESTER_DATE,
        parser=parser,
    )

    scraper.close()

    schedule_obj: Schedule = schedule.years[2]
    shifts: dict[str, list[str]] = {
        "Literaturas e Culturas Africanas de Língua Portuguesa 2": ["T1", "TP1"],
        "Literatura e Cultura Brasileiras 1": ["T1", "TP1", "PL1"],
        "Literatura Portuguesa do Barroco e do Neoclassicismo": ["T1", "TP1"],
        "Sintaxe do Português": ["T1", "TP1"],
        "Narrativas de Viagem": ["T1", "TP1"],
    }

    builder: Builder = JsonBuilder(schedule_obj)
    sched: bytes = builder.build()

    print(sched.decode())


if __name__ == "__main__":
    SystemExit(main())
