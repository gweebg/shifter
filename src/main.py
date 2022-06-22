# Outside libraries
from fastapi import FastAPI
from fastapi.responses import FileResponse

# Built-in libraries
import sys
import json

# Local modules
from parser import parse_schedule, ParsingError
from generator import generate_schedule
from models import ScheduleRequest, JsonRequest

app = FastAPI()  # uvicorn main:app --reload

"""
{
  "course_name": "Licenciatura em Engenharia Informática",
  "year": 2,
  "week_date": "12-05-2022",
  "file_name": "LEI_2ano_2sem_atualizado",
  "shifts": {
        "Investigação Operacional": ["T1", "TP4"],
        "Bases de Dados": ["T2", "PL4"],
        "Métodos Numéricos e Otimização não Linear": ["T1", "PL3"],
        "Programação Orientada aos Objetos": ["T1", "PL3"],
        "Redes de Computadores": ["T1", "PL9"],
        "Sistemas Operativos": ["T2", "PL9"]
    }
}
"""


@app.get("/courses")
async def get_course_names() -> str:
    with open("../docs/course_names.txt", "r", encoding="utf-8") as file:
        course_names = [line.replace("\n", "") for line in file]

    return json.dumps(course_names, ensure_ascii=False)


@app.post("/generate/excel/", response_description="xlsx")
async def generate(entry: ScheduleRequest) -> FileResponse | dict:

    if entry.file_name:
        entry.file_name = '../schedules/' + entry.file_name + '.xlsx'

    try:
        schedule: dict = parse_schedule(entry.course_name, str(entry.year), entry.week_date, entry.shifts)
        generate_schedule(schedule, entry.file_name)

    except TypeError as param_err:
        return {"invalid_parameter": param_err}

    except Exception as error:
        return {"error": error}

    path: str = entry.file_name if not None else "../schedules/new_schedule.xlsx"
    headers = {'Content-Disposition': f'attachment; filename=\"{path}\"'}

    return FileResponse(entry.file_name, headers=headers)


@app.post("/generate/json/")
async def generate_json(entry: JsonRequest) -> dict:

    try:
        schedule: dict = parse_schedule(entry.course_name, str(entry.year), entry.week_date, entry.shifts)
        return schedule

    except TypeError as param_err:
        return {"invalid_parameter": param_err}

    except Exception as error:
        return {"error": error}


def main() -> None:
    schedule: dict = parse_schedule('Licenciatura em Engenharia Informática', '2', '19-05-2022')
    # generate_schedule(schedule, "./schedules/DIR2ano2sem2022.xlsx")
    formatted = json.dumps(schedule, indent=4, ensure_ascii=False)
    print(formatted)

    pass


if __name__ == '__main__':
    sys.exit(main())
