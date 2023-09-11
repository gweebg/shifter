from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule
from src.lib.scraper.scraper import ScheduleScraper


def main():
    parser: ScheduleParser = ScheduleParser()
    scraper: ScheduleScraper = ScheduleScraper(is_headless=True)

    schedule = scraper.get(
        course_name="Mestrado em Engenharia Informática",
        year=1,
        formatted=True,
        date_str="11-09-2023",
        parser=parser,
    )

    schedule_obj: Schedule = schedule["Mestrado em Engenharia Informática"][1]

    shifts: dict[str, list[str]] = {
        "Aplicações e Serviços de Computação em Nuvem": ["T1", "PL3"],
        "Métodos Formais em Engenharia de Software": ["T1", "TP1"],
        "Requisitos e Arquiteturas de Software": ["T1", "PL2"],
        "Computação Paralela": ["PL6", "T1"],
        "Engenharia de Serviços em Rede": ["PL2", "T1"],
        "Dados e Aprendizagem Automática": ["T1", "PL5"]
    }

    print(schedule_obj.filter(shifts).get_as_dict())


if __name__ == '__main__':
    SystemExit(main())
