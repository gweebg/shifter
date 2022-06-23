from pydantic import BaseModel, Field


class ScheduleRequest(BaseModel):
    """
    Class representing an Excel schedule request.
    """

    course_name: str = Field(
        title="The name of the course.",
        max_length=128
    )

    year: int = Field(
        gt=0, lt=5,
        description="The year must be an integer number within [1,4].",
        title="The school year."
    )

    week_date: str = Field(
        title="Week date of schedule.",
        max_length=16
    )

    file_name: str | None = Field(
        default="new_schedule",
        max_length=32)

    shifts: dict

    class Config:
        schema_extra = {
            "example": {
                "course_name": "Licenciatura em Engenharia Informática",
                "year": 2,
                "week_date": "12-05-2022",
                "file_name": "my_new_schedule",
                "shifts": {
                    "Investigação Operacional": ["T1", "TP4"],
                    "Bases de Dados": ["T2", "PL4"],
                    "Métodos Numéricos e Otimização não Linear": ["T1", "PL3"],
                    "Programação Orientada aos Objetos": ["T1", "PL3"],
                    "Redes de Computadores": ["T1", "PL9"],
                    "Sistemas Operativos": ["T2", "PL9"]
                }
            }
        }


class JsonRequest(BaseModel):
    """
    Class representing a json only request.
    """

    course_name: str = Field(
        title="The name of the course.",
        max_length=128
    )

    year: int = Field(
        gt=0, lt=5,
        description="The year must be an integer number within [1,4].",
        title="The school year."
    )

    week_date: str = Field(
        title="Week date of schedule.",
        max_length=16
    )

    shifts: dict | None
