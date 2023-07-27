# Img FTP Model File
# Aldo Siswanto
# 2023/07/08

import tkinter as tk


class ImgFTPModel:
    VERSION = "0.0.2"
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
        'EQ-901848-004': ['1001', '1002', '1003', '1010'],
        'EQ-901853-004': ['6102', '6103', '6104', '6105', '6106', '6200', '6202', '6204', '6207', '6208', '6209'],
        'EQ-901849-004': ['2010', '2011', '2024', '2049'],
        'EQ-902050-003': ['11010'],
        'EQ-902052-003': ['13210'],
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
        self.start_datetime_var.set('YYYY-MM-DD HH:MM:SS')
        self.end_datetime_var.set('YYYY-MM-DD HH:MM:SS')

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
        return [day for day in range(int(self.start_month), int(self.end_month)+1)]

    @property
    def list_of_days(self):
        return [day for day in range(int(self.start_day), int(self.end_day)+1)]

    @property
    def inspection(self):
        return self.inspection_var.get() if len(self.inspection_var.get())>0 else None

    @property
    def selected_reject(self):
        return self.selected_reject_var.get()

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
