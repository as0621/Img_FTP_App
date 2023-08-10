# Img FTP Model File
# Aldo Siswanto
# 2023/07/08

import tkinter as tk
from datetime import datetime, time


class ImgFTPModel:
    VERSION = "1.0.0"
    OPTION_MENU_DEFAULT = 'Select One...'
    EQ_LIST = {'TED': 'EQ-901848-004',
               'ABL': 'EQ-901849-004',
               'CLOUE LD': 'EQ-902282-001',
               'CLOUE UNLD': 'EQ-902280-001',
               'SNL': 'EQ-901853-004',
               'PAT': 'EQ-902044-004',
               'MAC': 'EQ-902045-004',
               'XFC': 'EQ-902046-004',
               'FTC': 'EQ-902031-003',
               'PLR': 'EQ-902050-003',
               'CAP': 'EQ-902051-003',
               'TLA': 'EQ-902052-003',
               'OFF': 'EQ-902053-003'}
    REJECT_LIST = {
        'EQ-901848-004': ['1001', '1002', '1003', '1004', '1010', '1089'],
        'EQ-901849-004': ['2010', '2011',
                          '2020', '2021', '2022', '2023', '2024', '2025', '2026',
                          '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037', '2038', '2039',
                          '2041', '2042', '2043', '2044', '2045', '2046', '2037', '2048', '2049',
                          '2050',
                          '2080', '2081'],
        'EQ-902282-001': ['3001',
                          '3040', '3041', '3042',
                          '3061', '3062', '3064', '3065', '3066', '3069', ],
        'EQ-902280-001': ['4001', '4050', '4051', '4052', '4053', '4054', '4055', '4056', '4057', '4058',
                          '5001', '5002', '5003', '5004', '5020'],
        'EQ-901853-004': ['6102', '6103', '6104', '6105', '6106', '6200', '6202', '6204', '6207', '6208', '6209'],
        'EQ-902044-004': ['7013', '7014', '7015', '7016', '7018', '7019', '7020',
                          '7030', '7031', '7032', '7034', '7036', '7037',
                          '7040', '7041',
                          '7060', '7061', '7062', '7063', '7064', '7065'],
        'EQ-902045-004': ['8020', '8021', '8025', '8026', '8027', '8028', '8030', '8040',
                          '8050', '8051', '8052', '8053', '8054', '8055', '8056', '8057',
                          '8060', '8061', '8065', '8066'],
        'EQ-902046-004': ['9071', '9091'],
        'EQ-902050-003': ['11010', '11020', '11021', '11022', '11023', '11024', '11025'],
        'EQ-902051-003': ['12010', '12020', '12030', '12044', '12050', '12051', '12052', '12053', '12054',
                          '12060', '12061', '12070', '12071', '12080', '12081'],
        'EQ-902052-003': ['13020', '13021', '13092', '13093', '13200', '13210', '13220', '13230', '13240', '13250',
                          '13260'],
        'default': ['None']
    }

    def __init__(self, root):
        self.start_datetime_var = tk.StringVar(root)
        self.end_datetime_var = tk.StringVar(root)
        self.home_directory_var = tk.StringVar(root)
        self.eq_var = tk.StringVar(root)
        self.eq_number_var = tk.StringVar(root)
        self.quality_var = tk.StringVar(root, value='Gd')
        self.selected_reject_var = tk.StringVar(root)
        self.inspection_var = tk.StringVar(root)
        self.settings_save_txid_var = tk.BooleanVar(root)
        self.settings_use_scada_var = tk.BooleanVar(root)
        self.settings_use_scada_filepath_var = tk.StringVar(root)

        # Debug
        self.start_datetime_var.set(datetime.combine(datetime.now(), time.min).strftime("%Y-%m-%d %H:%M:%S"))
        self.end_datetime_var.set(datetime.combine(datetime.now(), time.max).strftime("%Y-%m-%d %H:%M:%S"))

        # TODO: Move traces to it's own function
        self.eq_var.trace_add('write', self.update_eq_name)

    @property
    def settings_use_scada_filepath(self):
        return self.settings_use_scada_filepath_var.get()

    @settings_use_scada_filepath.setter
    def settings_use_scada_filepath(self, filepath):
        self.settings_use_scada_filepath_var.set(filepath)

    @property
    def settings_save_txid(self):
        return self.settings_save_txid_var.get()

    @property
    def settings_use_scada(self):
        return self.settings_use_scada_var.get()

    @staticmethod
    def split_date_var(datetime):
        date, time = datetime.split()
        year, month, day = date.split('-')

        return date, year, month, day

    @staticmethod
    def split_time_var(datetime):
        date, time = datetime.split()
        hour, minute, sec = time.split(':')

        return time, hour, minute, sec

    @property
    def start_datetime(self):
        return self.start_datetime_var.get()

    @start_datetime.setter
    def start_datetime(self, datetime):
        self.start_datetime_var.set(datetime)

    @property
    def start_year(self) -> str:
        date, year, month, day = ImgFTPModel.split_date_var(self.start_datetime)
        return year

    @property
    def start_month(self) -> str:
        date, year, month, day = ImgFTPModel.split_date_var(self.start_datetime)
        return month

    @property
    def start_day(self) -> str:
        date, year, month, day = ImgFTPModel.split_date_var(self.start_datetime)
        return day

    @property
    def end_datetime(self):
        return self.end_datetime_var.get()

    @end_datetime.setter
    def end_datetime(self, datetime):
        self.end_datetime_var.set(datetime)

    @property
    def end_year(self) -> str:
        date, year, month, day = ImgFTPModel.split_date_var(self.end_datetime)
        return year

    @property
    def end_month(self) -> str:
        date, year, month, day = ImgFTPModel.split_date_var(self.end_datetime)
        return month

    @property
    def end_day(self) -> str:
        date, year, month, day = ImgFTPModel.split_date_var(self.end_datetime)
        return day

    @property
    def list_of_months(self):
        return [day for day in range(int(self.start_month), int(self.end_month) + 1)]

    @property
    def list_of_days(self):
        return [day for day in range(int(self.start_day), int(self.end_day) + 1)]

    @property
    def inspection(self):
        return self.inspection_var.get() if len(self.inspection_var.get()) > 0 else None

    @property
    def selected_reject(self):
        return self.selected_reject_var.get() if len(self.selected_reject_var.get()) > 0 else None

    @selected_reject.setter
    def selected_reject(self, reject):
        self.selected_reject_var.set(reject)

    @property
    def reject_list(self):
        return ImgFTPModel.REJECT_LIST[self.eq_number]

    @property
    def quality(self):
        return self.quality_var.get()

    @quality.setter
    def quality(self, quality):
        self.quality_var.set(quality)

    def update_eq_name(self, *args):
        if self.eq != ImgFTPModel.OPTION_MENU_DEFAULT:
            self.eq_number = ImgFTPModel.EQ_LIST[self.eq]

    @property
    def eq(self):
        return self.eq_var.get()

    @eq.setter
    def eq(self, eq):
        self.eq_var.set(eq)

    @property
    def eq_number(self):
        return self.eq_number_var.get()

    @eq_number.setter
    def eq_number(self, eq_number):
        self.eq_number_var.set(eq_number)

    @property
    def eq_list(self):
        return ImgFTPModel.EQ_LIST.keys()

    @property
    def home_directory(self):
        return self.home_directory_var.get()

    @home_directory.setter
    def home_directory(self, filepath):
        self.home_directory_var.set(filepath)

    def __str__(self):
        return f"Executing Request\n" \
               f"-----------------\n" \
               f"start datetime: {self.start_datetime}\n" \
               f"end datetime: {self.end_datetime}\n" \
               f"home: {self.home_directory}\n" \
               f"eq: {self.eq}\n" \
               f"eq no: {self.eq_number}\n" \
               f"quality: {self.quality}\n" \
               f"reject: {self.selected_reject}\n" \
               f"inspection: {self.inspection}\n" \
               f"use_scada: {self.settings_use_scada}\n"
        # f"save_txid: {model.settings_save_txid}\n"
