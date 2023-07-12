# Img FTP View to pull image from FTP server
# Aldo Siswanto
# 23/07/07

# Import Classes
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ImgFTPModel import ImgFTPModel
from ImgFTPController import ImgFTPController
import os
import threading


class App:
    # Constants
    VERSION = "0.0.1"
    APP_TITLE = 'FAST ImgServer Pull'
    APP_SIZE = '800x400'

    # Initializes frame
    def __init__(self):
        self.model = None
        self.controller = None
        self.view = None

        root = tk.Tk()
        root.title(App.APP_TITLE)
        root.geometry(App.APP_SIZE)

        self.initialize_model(root)
        self.initialize_controller()
        self.initialize_view(root)

    def initialize_model(self, root):
        self.model = ImgFTPModel(root)

    def initialize_controller(self):
        self.controller = ImgFTPController(self.model)

    def initialize_view(self, root):
        MainFrame(root, self.model, self.controller).pack(side='top')
        root.mainloop()


class MainFrame(tk.Frame):
    def __init__(self, parent, model, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = model
        self.controller = controller

        self.date_range_frame = DateRangeFrame(self)
        self.target_directory_frame = TargetDirectoryFrame(self)
        self.eq_frame = EqFrame(self)
        self.quality_frame = QualityFrame(self)
        self.inspection_frame = InspectionFrame(self)
        self.settings_frame = SettingsFrame(self)
        self.execute_frame = ExecuteFrame(self)

        self.date_range_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        ttk.Separator(self, orient='horizontal').grid(row=2, column=1, columnspan=2, sticky='ew')

        self.target_directory_frame.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        ttk.Separator(self, orient='horizontal').grid(row=4, column=1, columnspan=2, sticky='ew')

        self.eq_frame.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        ttk.Separator(self, orient='horizontal').grid(row=6, column=1, columnspan=2, sticky='ew')

        self.quality_frame.grid(row=7, column=1, rowspan=2, padx=5, pady=5, sticky='w')
        self.inspection_frame.grid(row=7, column=2, columnspan=1, padx=5, pady=5, sticky='nw')
        self.settings_frame.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky='w')
        ttk.Separator(self, orient='horizontal').grid(row=9, column=1, columnspan=2, sticky='ew')

        self.execute_frame.grid(row=10, column=1, columnspan=2, sticky='ew')


class DateRangeFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = parent.model

        self.start_datetime_range_title = self.create_start_datetime_range_title()
        self.start_datetime_range_entry = self.create_start_datetime_range_entry()
        self.end_datetime_range_title = self.create_end_datetime_range_title()
        self.end_datetime_range_entry = self.create_end_datetime_range_entry()

        self.start_datetime_range_title.grid(row=1, column=1, sticky='w')
        self.start_datetime_range_entry.grid(row=2, column=1, sticky='w')
        self.end_datetime_range_title.grid(row=1, column=2, padx=20, sticky='w')
        self.end_datetime_range_entry.grid(row=2, column=2, padx=20, sticky='w')

    def create_start_datetime_range_title(self):
        title = ttk.Label(self, text='Start Datetime Range (YYYY-MM-DD HH:MM:SS):')
        return title

    def create_start_datetime_range_entry(self):
        entry_box = ttk.Entry(self, textvariable=self.model.start_datetime_var)
        return entry_box

    def create_end_datetime_range_title(self):
        title = ttk.Label(self, text='End Datetime Range (YYYY-MM-DD HH:MM:SS):')
        return title

    def create_end_datetime_range_entry(self):
        entry_box = ttk.Entry(self, textvariable=self.model.end_datetime_var)
        return entry_box


class TargetDirectoryFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = parent.model

        self.target_directory_title = self.create_target_directory_title()
        self.target_directory_label = self.create_target_directory_label()
        self.target_directory_button = self.create_target_directory_button()

        self.target_directory_title.grid(row=1, column=1, sticky='w')
        self.target_directory_label.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.target_directory_button.grid(row=1, column=2, sticky='e')

    def create_target_directory_title(self):
        title = ttk.Label(self, text='Current Image Home Directory:')
        return title

    def create_target_directory_label(self):
        label = ttk.Label(self, textvariable=self.model.home_directory_var, width=80, anchor='w')
        return label

    def create_target_directory_button(self):
        button = ttk.Button(self, text='Select Directory', command=self.open_directory_selector)
        return button

    def open_directory_selector(self):
        filepath = filedialog.askdirectory()
        self.model.home_directory = filepath


class EqFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = parent.model

        self.eq_name_title = self.create_eq_name_title()
        self.eq_name_dropdown = self.create_eq_name_dropdown()
        self.eq_number_title = self.create_eq_number_title()
        self.eq_number_label = self.create_eq_number_label()

        self.eq_name_title.grid(row=1, column=1, sticky='w')
        self.eq_name_dropdown.grid(row=1, column=2, sticky='w')
        self.eq_number_title.grid(row=1, column=4, sticky='w')
        self.eq_number_label.grid(row=1, column=5, sticky='w')

    def create_eq_name_title(self):
        title = tk.Label(self, text='EQ:')
        return title

    def create_eq_name_dropdown(self):
        dropdown = ttk.OptionMenu(self, self.model.eq_var, ImgFTPModel.OPTION_MENU_DEFAULT, *self.model.eq_list,
                                  command=self.eq_select)
        dropdown.configure(width=20)
        return dropdown

    def create_eq_number_title(self):
        title = tk.Label(self, text='EQ#:')
        return title

    def create_eq_number_label(self):
        label = tk.Label(self, textvariable=self.model.eq_number_var)
        return label

    def eq_select(self, *args):
        self.parent.quality_frame.refresh_reject_dropdown()


class QualityFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = parent.model

        self.quality_title = self.create_quality_title()
        self.quality_radio_buttons = self.create_quality_radio_button()
        self.quality_reject_dropdown = self.create_quality_reject_dropdown()

        self.model.quality_var.trace('w', self.refresh_reject_dropdown_state)

        self.quality_title.pack(anchor='nw')
        for radio_button in self.quality_radio_buttons:
            radio_button.pack(anchor='nw')
            radio_button.configure(state='disabled')
        self.quality_reject_dropdown.pack(anchor='nw')

        # Temporary enable reject radio
        self.quality_radio_buttons[-1].configure(state='normal')

    def create_quality_title(self):
        label = ttk.Label(self, text='Quality:')
        return label

    def create_quality_radio_button(self):
        gd_radio_button = ttk.Radiobutton(self, text='Gd', variable=self.model.quality_var, value='Gd')
        bd_radio_button = ttk.Radiobutton(self, text='Bd', variable=self.model.quality_var, value='Bd')
        all_radio_button = ttk.Radiobutton(self, text='All', variable=self.model.quality_var, value='All')
        reject_radio_button = ttk.Radiobutton(self, text='Reject', variable=self.model.quality_var, value='Reject')

        # reject_radio_button.configure(state='disabled')

        return gd_radio_button, bd_radio_button, all_radio_button, reject_radio_button

    def create_quality_reject_dropdown(self):
        dropdown = ttk.OptionMenu(self, self.model.selected_reject_var, 'None')
        dropdown.configure(state='disabled', width=20)
        return dropdown

    def refresh_reject_dropdown_state(self, *args):
        if self.model.quality == 'Reject':
            self.quality_reject_dropdown.configure(state='active')
        else:
            self.quality_reject_dropdown.configure(state='disabled')

    def refresh_reject_dropdown(self):
        self.quality_reject_dropdown['menu'].delete(0, 'end')

        new_options = self.model.reject_list
        for option in new_options:
            self.quality_reject_dropdown['menu'].add_command(label=option,
                                                             command=tk._setit(self.model.selected_reject_var, option))


class InspectionFrame(tk.Frame):
    def __init__(self, parent):
        self.custom_inspection_bool = tk.BooleanVar()

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = parent.model

        self.inspection_title = self.create_inspection_title()
        self.inspection_check_button = self.create_inspection_check_button()
        self.inspection_entry = self.create_inspection_entry()

        self.custom_inspection_bool.trace('w', self.refresh_entry_state)

        self.inspection_title.pack(anchor='nw')
        self.inspection_check_button.pack(anchor='nw')
        self.inspection_entry.pack(anchor='nw')

        # Temporary disable
        # self.inspection_check_button.configure(state='disabled')

    def create_inspection_title(self):
        title = tk.Label(self, text='Custom Preferences: ')
        return title

    def create_inspection_check_button(self):
        check_button = ttk.Checkbutton(self, text='Cstm Inspection #', variable=self.custom_inspection_bool)
        return check_button

    def create_inspection_entry(self):
        entry_box = ttk.Entry(self, textvariable=self.model.inspection_var)
        entry_box.configure(state='disabled')
        return entry_box

    def refresh_entry_state(self, *args):
        if self.custom_inspection_bool.get() == 1:
            self.inspection_entry.configure(state='normal')
        else:
            self.inspection_entry.delete(0, 'end')
            self.inspection_entry.configure(state='disabled')


class SettingsFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = parent.model
        self.settings_title = self.create_settings_title()
        self.settings_save_txid_checkbox = self.create_settings_save_txid_checkbox()
        self.settings_use_scada_checkbox = self.create_settings_use_scada_checkbox()
        self.settings_use_scada_filepath_button = self.create_settings_use_scada_filepath_button()
        self.settings_use_scada_filepath_label = self.create_settings_use_scada_filepath_label()

        self.settings_title.pack(anchor='w')
        self.settings_save_txid_checkbox.pack(anchor='w')
        self.settings_use_scada_checkbox.pack(anchor='w')
        self.settings_use_scada_filepath_button.pack(anchor='w')
        self.settings_use_scada_filepath_label.pack(anchor='w')

        # Momentary disable
        self.settings_save_txid_checkbox.configure(state='disabled')
        self.settings_use_scada_checkbox.configure(state='disabled')

    def create_settings_title(self):
        title = tk.Label(self, text='Settings: ')
        return title

    def create_settings_save_txid_checkbox(self):
        check_button = ttk.Checkbutton(self, text='Save TxID in csv', variable=self.model.settings_save_txid_var)
        return check_button

    def create_settings_use_scada_checkbox(self):
        check_button = ttk.Checkbutton(self, text='Use SCADA export (.csv)', variable=self.model.settings_use_scada_var,
                                       command=self.scada_mode_change_status)
        return check_button

    def create_settings_use_scada_filepath_button(self):
        button = ttk.Button(self, text='Load SCADA export', command=self.load_scada_filepath)
        button.configure(state='disabled')
        return button

    def create_settings_use_scada_filepath_label(self):
        label = ttk.Label(self, textvariable=self.model.settings_use_scada_filepath_var, width=80)
        return label

    def load_scada_filepath(self):
        file = filedialog.askopenfilename(filetypes=[('SCADA export CSV (.csv)', '*.csv')], initialdir='C:/myExports/')
        self.model.settings_use_scada_filepath = os.path.abspath(file)

    def scada_mode_change_status(self):
        if self.model.settings_use_scada:
            self.parent.date_range_frame.start_datetime_range_entry.delete(0, 'end')
            self.parent.date_range_frame.start_datetime_range_entry.configure(state='disabled')
            self.parent.date_range_frame.end_datetime_range_entry.delete(0, 'end')
            self.parent.date_range_frame.end_datetime_range_entry.configure(state='disabled')
            # self.parent.quality_frame.quality_radio_buttons[-1].configure(state='normal')
            # self.parent.quality_frame.quality_reject_dropdown.configure(state='normal')
            self.settings_use_scada_filepath_button.configure(state='normal')
        else:
            self.parent.date_range_frame.start_datetime_range_entry.configure(state='normal')
            self.parent.date_range_frame.end_datetime_range_entry.configure(state='normal')
            # self.parent.quality_frame.quality_radio_buttons[-1].configure(state='active')
            # self.parent.quality_frame.quality_radio_buttons[-1].configure(state='disabled')
            # self.parent.quality_frame.quality_reject_dropdown.configure(state='disabled')
            self.model.settings_use_scada_filepath = ''
            self.settings_use_scada_filepath_button.configure(state='disabled')


class ExecuteFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.model = parent.model
        self.controller = parent.controller
        self.status_var = tk.StringVar()

        self.execute_button = self.create_execute_button()
        self.execute_status_label = self.create_execute_status_label()

        self.execute_button.pack(anchor='n')
        self.execute_status_label.pack(anchor='n')

    def create_execute_button(self):
        button = ttk.Button(self, text="Execute", command=self.execute_pull)
        return button

    def execute_pull(self):
        thread = threading.Thread(target=self.controller.get_images, args=(self.status_var, ))
        thread.start()

    def create_execute_status_label(self):
        label = ttk.Label(self, textvariable=self.status_var)
        return label

