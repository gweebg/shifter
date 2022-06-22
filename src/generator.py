# Outside libraries
import xlsxwriter as excel

# Local modules
from elements import (dark_color_format, light_color_format, colors,
                      header_format, weekdays_map, hours_map, merge_format)
from parser import ParsingError


def generate_schedule(schedule: dict, path: str | None = None) -> None:
    """
    Generates the schedule as an Excel worksheet using the result from 'parse_schedule'.
    If 'path' is not provided the result file name will be 'new_schedule.xlsx'.
    The 'schedule' object has to be filtered by shifts. Can't be a full schedule.

    :param schedule: Dictionary containing parsed schedule by a set of shifts.
    :param path: The path of the file to be generated.
    :return: None
    :raises ParsingError: If, for some reason, a duration value is not in {1.0, 2.0}.
    """

    # If given path is None then set path to default value.
    if path is None:
        path: str = "../schedules/new_schedule.xlsx"

    # Creating a new Excel workbook.
    with excel.Workbook(path) as workbook:

        print("Setting up Excel workbook.")

        worksheet = workbook.add_worksheet("Your Schedule")  # Setting up a page.
        worksheet.set_column(0, 5, 23)  # Column length.
        worksheet.set_default_row(45)  # Default number of rows.
        worksheet.set_row(0, 20)  # Row length.

        dark_color = workbook.add_format(dark_color_format)
        light_color = workbook.add_format(light_color_format)
        header_style = workbook.add_format(header_format)

        header_style.set_font_color("white")

        time_data = ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
                     "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM",
                     "6:00 PM", "7:00 PM"]

        header_data = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Writting the header to the worksheet.
        worksheet.write_row("A1:F1", data=header_data, cell_format=header_style)

        # Writes time values and paints schedule background to kind of chess pattern.
        for i in range(2, 14):
            worksheet.write_row(f"A{i}:F{i}",
                                data=[time_data[i - 2], "", "", "", "", ""],
                                cell_format=light_color if i % 2 == 0 else dark_color)

        subjects_color_map: dict = {}
        color_index: int = 0

        print("Populating Excel sheet with the schedule.")
        for weekday in schedule:

            if len(schedule[weekday]) > 0:

                for subject in schedule[weekday]:

                    subject_name: str = subject["title"].split("\n")[0].strip()

                    if subject_name not in subjects_color_map.keys():
                        subjects_color_map[subject_name] = colors[color_index]
                        color_index += 1

                    color = subjects_color_map[subject_name]

                    merge_format["fg_color"] = color
                    merge_style = workbook.add_format(merge_format)
                    merge_style.set_font_size(9)

                    mapped_hour: int = hours_map[subject["starts_at"]]
                    mapped_days: str = weekdays_map[subject["weekday"]]

                    if subject["duration"] == 2.0:
                        worksheet.merge_range(
                            f"{mapped_days}{mapped_hour}:{mapped_days}{mapped_hour + 1}",
                            subject["title"], merge_style)

                    elif subject["duration"] == 1.0:
                        worksheet.write(f"{mapped_days}{mapped_hour}", subject["title"], merge_style)

                    else:
                        raise ParsingError("Unexpected value at subject duration, must be either 1 or 2.")

    print(f"Saved schedule at {path} :)")
    return
