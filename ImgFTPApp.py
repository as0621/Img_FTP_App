# Img FTP View to pull image from FTP server
# Aldo Siswanto
# 23/07/07

# Import Classes
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo


class App:
    # Constants
    APP_TITLE = 'FAST ImgServer Pull'
    APP_SIZE = '600x400'

    # Initializes frame
    def __init__(self):
        root = tk.Tk()
        root.title(App.APP_TITLE)
        root.geometry(App.APP_SIZE)
        MainFrame(root).pack(side='top')
        root.mainloop()


class MainFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
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
        self.start_datetime_range_title = self.create_start_datetime_range_title()
        self.start_datetime_range_entry = self.create_start_datetime_range_entry()
        self.end_datetime_range_title = self.create_end_datetime_range_title()
        self.end_datetime_range_entry = self.create_end_datetime_range_entry()

        self.start_datetime_range_title.grid(row=1, column=1, sticky='w')
        self.start_datetime_range_entry.grid(row=2, column=1, sticky='w')
        self.end_datetime_range_title.grid(row=1, column=2, padx=20, sticky='w')
        self.end_datetime_range_entry.grid(row=2, column=2, padx=20, sticky='w')

    def create_start_datetime_range_title(self):
        title = tk.Label(self, text='Start Datetime Range (YYYY/MM/DD HH:MM:SS):')
        return title

    def create_start_datetime_range_entry(self):
        entry_box = tk.Entry(self)
        return entry_box

    def create_end_datetime_range_title(self):
        title = tk.Label(self, text='End Datetime Range (YYYY/MM/DD HH:MM:SS):')
        return title

    def create_end_datetime_range_entry(self):
        entry_box = tk.Entry(self)
        return entry_box


class TargetDirectoryFrame(tk.Frame):
    def __init__(self, parent):
        self.current_target_directory = tk.StringVar(value='')

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.target_directory_title = self.create_target_directory_title()
        self.target_directory_label = self.create_target_directory_label()
        self.target_directory_button = self.create_target_directory_button()

        self.target_directory_title.grid(row=1, column=1, sticky='w')
        self.target_directory_label.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.target_directory_button.grid(row=1, column=2, sticky='e')

    def create_target_directory_title(self):
        title = tk.Label(self, text='Current Image Home Directory:')
        return title

    def create_target_directory_label(self):
        label = tk.Label(self, textvariable=self.current_target_directory, width=80, anchor='w')
        return label

    def create_target_directory_button(self):
        button = tk.Button(self, text='Select Directory', command=self.open_directory_selector)
        return button

    def open_directory_selector(self):
        filepath = tk.filedialog.askdirectory()
        self.current_target_directory.set(filepath)


class EqFrame(tk.Frame):
    EQ_LIST = {'Equipment1': 'EQ-1',
               'Equipment2': 'EQ-2',
               'Equipment3': 'EQ-3'}

    def __init__(self, parent):
        self.selected_eq = tk.StringVar()
        self.selected_eq_number = tk.StringVar()

        tk.Frame.__init__(self, parent)
        self.parent = parent
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
        self.selected_eq.set('Select One...')
        dropdown = tk.OptionMenu(self, self.selected_eq, *EqFrame.EQ_LIST.keys(), command=self.eq_select)
        dropdown.configure(width=20)
        return dropdown

    def create_eq_number_title(self):
        title = tk.Label(self, text='EQ#:')
        return title

    def create_eq_number_label(self):
        label = tk.Label(self, textvariable=self.selected_eq_number)
        return label

    def eq_select(self, selected_eq):
        self.selected_eq_number.set(EqFrame.EQ_LIST[selected_eq])
        self.parent.quality_frame.refresh_reject_dropdown()


class QualityFrame(tk.Frame):
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

    def __init__(self, parent):
        self.selected_quality = tk.StringVar(value='Gd')
        self.selected_eq_number = 'default'
        self.selected_reject = tk.StringVar()

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.quality_title = self.create_quality_title()
        self.quality_radio_buttons = self.create_quality_radio_button()
        self.quality_reject_dropdown = self.create_quality_reject_dropdown()
        self.selected_quality.trace('w', self.refresh_reject_dropdown_state)

        self.quality_title.pack(anchor='w')
        for radio_button in self.quality_radio_buttons:
            radio_button.pack(anchor='w')
        self.quality_reject_dropdown.pack(anchor='w')

    def create_quality_title(self):
        label = tk.Label(self, text='Quality:')
        return label

    def create_quality_radio_button(self):
        gd_radio_button = tk.Radiobutton(self, text='Gd', variable=self.selected_quality, value='Gd')
        bd_radio_button = tk.Radiobutton(self, text='Bd', variable=self.selected_quality, value='Bd')
        all_radio_button = tk.Radiobutton(self, text='All', variable=self.selected_quality, value='All')
        reject_radio_button = tk.Radiobutton(self, text='Reject', variable=self.selected_quality, value='Reject')

        return gd_radio_button, bd_radio_button, all_radio_button, reject_radio_button

    def create_quality_reject_dropdown(self):
        self.selected_reject.set('None')
        dropdown = tk.OptionMenu(self, self.selected_reject, *QualityFrame.REJECT_LIST[self.selected_eq_number])
        dropdown.configure(state='disabled', width=20)
        return dropdown

    def refresh_reject_dropdown_state(self, *args):
        if self.selected_quality.get() == 'Reject':
            self.quality_reject_dropdown.configure(state='active')
        else:
            self.quality_reject_dropdown.configure(state='disabled')

    def refresh_reject_dropdown(self):
        self.selected_reject.set('Select one..')
        self.quality_reject_dropdown['menu'].delete(0, 'end')

        new_options = QualityFrame.REJECT_LIST[self.parent.eq_frame.selected_eq_number.get()]
        for option in new_options:
            self.quality_reject_dropdown['menu'].add_command(label=option,
                                                             command=tk._setit(self.selected_reject, option))


class InspectionFrame(tk.Frame):
    def __init__(self, parent):
        self.custom_inspection_bool = tk.BooleanVar()

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.inspection_title = self.create_inspection_title()
        self.inspection_check_button = self.create_inspection_check_button()
        self.inspection_entry = self.create_inspection_entry()

        self.custom_inspection_bool.trace('w', self.refresh_entry_state)

        self.inspection_title.pack(anchor='nw')
        self.inspection_check_button.pack(anchor='nw')
        self.inspection_entry.pack(anchor='nw')

    def create_inspection_title(self):
        title = tk.Label(self, text='Custom Preferences: ')
        return title

    def create_inspection_check_button(self):
        check_button = tk.Checkbutton(self, text='Cstm Inspection #', variable=self.custom_inspection_bool)
        return check_button

    def create_inspection_entry(self):
        entry_box = tk.Entry(self)
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
        self.save_txid_bool = tk.BooleanVar(value=False)
        tk.Frame.__init__(self, parent)
        self.settings_title = self.create_settings_title()
        self.settings_save_txid_checkbox = self.create_settings_save_txid_checkbox()

        self.settings_title.pack(anchor='w')
        self.settings_save_txid_checkbox.pack(anchor='w')

    def create_settings_title(self):
        title = tk.Label(self, text='Settings: ')
        return title

    def create_settings_save_txid_checkbox(self):
        check_button = tk.Checkbutton(self, text='Save TxID in csv', variable=self.save_txid_bool)
        return check_button


class ExecuteFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.execute_button = self.create_execute_button()

        self.execute_button.pack(anchor='n')

    def create_execute_button(self):
        button = tk.Button(self, text="Execute")
        return button
