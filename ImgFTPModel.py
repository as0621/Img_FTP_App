# Img FTP Model File
# Aldo Siswanto
# 2023/07/08

import tkinter as tk


class ImgFTPModel:
    VERSION = "0.0.1"
    OPTION_MENU_DEFAULT = 'Select One...'
    EQ_LIST = {'Equipment1': 'EQ-1',
               'Equipment2': 'EQ-2',
               'Equipment3': 'EQ-3'}
    REJECT_LIST = {'EQ-1': ['EQ1_FC1',
                            'EQ1_FC2',
                            'EQ1_FC3'],
                   'EQ-2': ['EQ2_FC1',
                            'EQ2_FC2',
                            'EQ2_FC3'],
                   'EQ-3': ['EQ3_FC1',
                            'EQ3_FC2',
                            'EQ3_FC3'],
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

        # TODO: Move traces to it's own function
        self.eq_var.trace_add('write', self.update_eq_name)

    @property
    def settings_save_txid(self):
        return self.settings_save_txid_var.get()

    @property
    def start_datetime(self):
        return self.start_datetime_var.get()

    @start_datetime.setter
    def start_datetime(self, datetime):
        self.start_datetime_var.set(datetime)

    @property
    def end_datetime(self):
        return self.end_datetime_var.get()

    @end_datetime.setter
    def end_datetime(self, datetime):
        self.end_datetime_var.set(datetime)

    @property
    def inspection(self):
        return self.inspection_var.get()

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
