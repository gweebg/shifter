# Elements id's and classes names for inputs on .aspx form for Selenium. #

search_button = 'ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_btnSearchHorario'
search_bar = 'ctl00$ctl40$g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef$ctl00$dataCurso'

first_year = 'ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_dataAnoCurricular_0'
second_year = 'ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_dataAnoCurricular_1'
third_year = 'ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_dataAnoCurricular_2'
fourth_year = 'ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_dataAnoCurricular_3'

date_bar = 'ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_dataWeekSelect_dateInput'
expand_check = 'ctl00_ctl40_g_e84a3962_8ce0_47bf_a5c3_d5f9dd3927ef_ctl00_chkMostraExpandido'

# Global variables for the parser. #

table_class = 'rsContentTable'

HOURS = ["8h00", "8h30",
         "9h00", "9h30",
         "10h00", "10h30",
         "11h00", "11h30",
         "12h00", "12h30",
         "13h00", "13h30",
         "14h00", "14h30",
         "15h00", "15h30",
         "16h00", "16h30",
         "17h00", "17h30",
         "18h00", "18h30",
         "19h00", "19h30",
         "20h00"]

# Global variables for the Excel schedule generator. #

dark_color_format = {
    "align": "center",
    "valign": "vcenter",
    "bg_color": "#A6A6A6"
}

light_color_format = {
    "align": "center",
    "valign": "vcenter",
    "bg_color": "#ffffff",
}

header_format = {
    "align": "center",
    "valign": "vcenter",
    "bg_color": "#666666",
}

merge_format = {
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'text_wrap': True
}

weekdays_map = {
    "Segunda-Feira": "B",
    "Terça-Feira": "C",
    "Quarta-Feira": "D",
    "Quinta-Feira": "E",
    "Sexta-Feira": "F"
}

hours_map = {
    "8h00": 2, "9h00": 3, "10h00": 4,
    "11h00": 5, "12h00": 6, "13h00": 7,
    "14h00": 8, "15h00": 9, "16h00": 10,
    "17h00": 11, "18h00": 12, "19h00": 13, "20h00": 14
}

colors = ["#BAF2BB", "#BAF2D8", "#F2BAC9", "#F4F7F9", "#F4F39A", "#AA4465"]
