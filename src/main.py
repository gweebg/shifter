from src.lib.builder.builder import build_schedule_xlsx
from src.lib.builder.excel import XlsxBuilder
from src.lib.scraper.parser import ScheduleParser
from src.lib.scraper.schedule import Schedule
from src.lib.scraper.scraper import ScheduleScraper

"""
1º Receber dados com os turnos para cada ano e cada cadeira:
{
    "MEI": { 
        1: {
            "A": ["TP1", "T2"]
        },
        2: {...},
        3: {...}
    }
}

2º Pesquisar na cache por "MEI" e pela data.
3º Filtrar pelos turnos.
4º Dar merge a todos os horários.
5º Converter para json/excel/wtvh.
"""


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
        "Requisitos e Arquiteturas de Software": ["T1", "PL2", "PL1", "PL5"],
        "Computação Paralela": ["PL6", "T1"],
        "Engenharia de Serviços em Rede": ["PL2", "T1", "PL1"],
        "Dados e Aprendizagem Automática": ["T1", "PL5"]
    }

    xlsx_builder: XlsxBuilder = XlsxBuilder(schedule=schedule_obj.filter(shifts))
    xlsx_builder.build()


if __name__ == '__main__':
    SystemExit(main())
