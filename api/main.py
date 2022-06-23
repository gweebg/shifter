# Outside libraries
from fastapi import FastAPI
from fastapi.responses import FileResponse

# Built-in libraries
import sys
import json

# Local modules
from parser import parse_schedule
from generator import generate_schedule
from models import ScheduleRequest, JsonRequest

app = FastAPI()  # uvicorn main:app --reload


@app.get("/courses")
async def get_course_names() -> list[str]:
    """
    Handle for get request at '/courses'. Returns a list of every course_name supported by this API.

    :return: List of strings containing with the course names.
    :rtype: Coroutine[Any, Any, list[str]]
    """

    with open("../docs/course_names.txt", "r", encoding="utf-8") as file:
        course_names = [line.replace("\n", "") for line in file]

    return course_names


@app.post("/generate/excel/", response_description="xlsx")
async def generate(entry: ScheduleRequest) -> FileResponse | dict:
    """
    Handle for post requests at '/generate/excel/'. Generates a '.xlsx' schedule from a ScheduleRequest object.

    :param entry: ScheduleRequest object containing data from post request.
    :return: Returns a FileResponse object (.xlsx file) if succssesfull or dict if a exception is caught.
    :rtype: Coroutine[Any, Any, FileResponse | dict]
    """

    if entry.file_name:
        entry.file_name = '../schedules/' + entry.file_name + '.xlsx'

    try:
        schedule: dict = parse_schedule(entry.course_name, str(entry.year), entry.week_date, entry.shifts)
        generate_schedule(schedule, entry.file_name)

    except TypeError as param_err:
        return {"invalid_parameter": param_err}

    except KeyError as key_err:
        return {"invalid_shift_entry": key_err.args[0]}

    except Exception as error:
        return {"error": error}

    path: str = entry.file_name if not None else "../schedules/new_schedule.xlsx"
    headers = {'Content-Disposition': f'attachment; filename=\"{path}\"'}

    return FileResponse(entry.file_name, headers=headers)


@app.post("/generate/json/")
async def generate_json(entry: JsonRequest) -> dict:
    """
    Handle for post requests at '/generate/json/'. Generates a json schedule from a JsonRequest object.

    :param entry: JsonRequest object containing data from post request.
    :return: Returns dict containing the schedule or error info if present.
    :rtype: Coroutine[Any, Any, dict]
    """

    try:
        schedule: dict = parse_schedule(entry.course_name, str(entry.year), entry.week_date, entry.shifts)
        return schedule

    except TypeError as param_err:
        return {"invalid_parameter": param_err}

    except Exception as error:
        return {"error": error}


def main() -> None:
    """
    Function for testing single functions of the API.

    :return: None
    """

    schedule: dict = parse_schedule('Licenciatura em Engenharia Informática', '2', '19-05-2022')
    # generate_schedule(schedule, "./schedules/DIR2ano2sem2022.xlsx")
    formatted = json.dumps(schedule, indent=4, ensure_ascii=False)
    print(formatted)

    pass


if __name__ == '__main__':
    sys.exit(main())
