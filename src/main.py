# Built-in libraries
import sys
import json

# Local modules
from scraper import parse_schedule


def main() -> None:
    # schedule: dict = parse_schedule('Licenciatura em Engenharia Informática', '2', '19-05-2022')
    schedule: dict = parse_schedule('Licenciatura em Direito', '2', '19-05-2022')
    formatted = json.dumps(schedule, indent = 4, ensure_ascii = False)
    print(formatted)


if __name__ == '__main__':
    sys.exit(main())
