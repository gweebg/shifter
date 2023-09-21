from src.lib.builder.builder import Builder
from src.lib.builder.ical.ical_builder import IcalBuilder
from src.lib.builder.json.json_builder import JsonBuilder
from src.lib.builder.xlsx.xlsx_builder import XlsxBuilder
from src.lib.cache.ttl_cache import Cache
from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule, ScheduleGroup
from src.lib.scraper.scraper import ScheduleScraper

FIRST_SEMESTER_DATE: str = "01-11-2023"
SECOND_SEMESTER_DATE: str = "01-03-2024"


def main():
    parser: ScheduleParser = ScheduleParser()
    scraper: ScheduleScraper = ScheduleScraper(is_headless=True)

    course_name: str = "Mestrado em Engenharia Informática"
    schedule: ScheduleGroup = scraper.get(
        course_name=course_name,
        formatted=True,
        year=1,
        date_str=FIRST_SEMESTER_DATE,
        parser=parser,
    )

    scraper.close()

    schedule_obj: Schedule = schedule.years[1]
    shifts: dict[str, list[str]] = {
        "Aplicações e Serviços de Computação em Nuvem": ["T1", "PL6"],
        "Métodos Formais em Engenharia de Software": ["T1", "TP4"],
        "Requisitos e Arquiteturas de Software": ["T1", "PL1"],
        "Computação Paralela": ["PL5", "T1"],
        "Engenharia de Serviços em Rede": ["PL3", "T1"],
        "Dados e Aprendizagem Automática": ["T1", "PL4"]
    }

    print(schedule_obj)

    # builder: Builder = XlsxBuilder(schedule=schedule_obj.filter(shifts), debug=True)
    # builder: Builder = IcalBuilder(schedule=schedule_obj.filter(shifts))
    # builder: Builder = JsonBuilder(schedule=schedule_obj.filter(shifts))
    # print(builder.build().decode())
    # builder.build()


if __name__ == '__main__':
    SystemExit(main())
