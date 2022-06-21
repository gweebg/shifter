# Built-in libraries
import sys
import json

# Local modules
from parser import parse_schedule
from generator import generate_schedule


def main() -> None:
    # schedule: dict = parse_schedule('Licenciatura em Engenharia Informática', '2', '19-05-2022')
    schedule: dict = parse_schedule('Licenciatura em Direito', '2', '19-05-2022')
    generate_schedule(schedule, "./schedules/DIR2ano2sem2022.xlsx")

    #formatted = json.dumps(schedule, indent = 4, ensure_ascii = False)
    #print(formatted)


if __name__ == '__main__':
    sys.exit(main())
