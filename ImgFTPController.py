# Img FTP Controller File
# Aldo Siswanto
# 2023/07/08

import pyodbc
import os
import ftplib
import tkinter as tk


class ImgFTPController:
    VERSION = "1.0.1"

    def __init__(self, model):
        self.model = model
        self.sql = SQLController()
        self.ftp = FTPController()

    def get_images(self, tk_status: tk.StringVar):
        try:
            self.get_images_general(tk_status)
        except Exception as e:
            tk_status.set(f"ERROR: {e}")
            raise Exception(e)

    def get_images_general(self, tk_status: tk.StringVar):
        if self.model.quality == 'Reject':
            sql_txid_list = self.sql.get_txid_list_from_rejects(self.model.start_datetime,
                                                                self.model.end_datetime,
                                                                self.model.selected_reject,
                                                                tk_status)
        else:
            sql_txid_list = self.sql.get_txid_list(self.model.start_datetime,
                                                   self.model.end_datetime,
                                                   tk_status)

        if len(sql_txid_list) > 0:
            for day in self.model.list_of_days:
                tk_status.set(f'Getting data for day: {day}')
                name_list = self.ftp.get_images_list(self.model.home_directory,
                                                     self.model.eq,
                                                     self.model.eq_number,
                                                     self.model.start_year,
                                                     self.model.start_month,
                                                     f"{day:02d}",
                                                     self.model.quality,
                                                     self.model.selected_reject,
                                                     self.model.inspection,
                                                     tk_status,
                                                     txid_list=sql_txid_list,
                                                     )

                self.ftp.get_images(name_list, tk_status)
                tk_status.set('DONE')
        else:
            tk_status.set(f'ERROR: No {self.model.eq} {self.model.selected_reject} Rejects.')


class FTPController:
    HOSTNAME = "10.3.84.33"
    USERNAME = "nth"
    PASSWORD = "nthnth1"

    def __init__(self):
        self.target_path_directory = None
        self.ftp = ftplib.FTP(FTPController.HOSTNAME, FTPController.USERNAME, FTPController.PASSWORD)

    def change_ftp_dir(self, eq_num, year, month, day):
        image_path = f'/Images/{eq_num}/{year}/{month}/{day}'
        self.ftp.cwd(image_path)

    def create_dir(self, home_dir, eq, year, month, day, quality, reject=None):
        if reject is None:
            self.target_path_directory = os.path.join(home_dir,
                                                      eq,
                                                      year,
                                                      month,
                                                      day,
                                                      quality)
        else:
            self.target_path_directory = os.path.join(home_dir,
                                                      eq,
                                                      year,
                                                      month,
                                                      day,
                                                      quality,
                                                      reject)

        if not os.path.exists(self.target_path_directory):
            os.makedirs(self.target_path_directory)

    def get_images_list(self, home_dir, eq, eq_num, year, month, day, quality, reject, inspection, tk_status,
                        txid_list=None):
        # Create Directory
        tk_status.set('Creating local directory...')
        if quality == 'Reject':
            self.create_dir(home_dir, eq, year, month, day, quality, reject)  # Create local directory
        else:
            self.create_dir(home_dir, eq, year, month, day, quality)

        # Entering FTP Directory
        tk_status.set(f'Getting directory for {year}/{month}/{day}...')
        self.change_ftp_dir(eq_num, year, month, day)

        # Getting all files from directory
        name_list = self.ftp.nlst()
        name_list = [f"{name}" for name in name_list if '.bmp' in name]

        if quality == 'Gd':
            name_list = [f"{name}" for name in name_list if ('Gd' in name and any(txid in name for txid in txid_list))]
        elif quality == 'Bd':
            name_list = [f"{name}" for name in name_list if ('Bd' in name and any(txid in name for txid in txid_list))]
        # elif quality == 'Reject':
        else:
            name_list = [f"{name}" for name in name_list if any(txid in name for txid in txid_list)]

        # Inspection Filter
        if inspection:
            name_list = [f"{name}" for name in name_list if inspection in name]

        return name_list

    def get_images(self, name_list, tk_status):
        tk_status.set('Starting Transfer...')
        for f in name_list:
            if tk_status.get() != 'STOP':
                tk_status.set("Transferring " + str(f) + "....")
                print("Transferring " + str(f) + "....")
                with open(os.path.join(self.target_path_directory, f), 'wb') as fh:
                    self.ftp.retrbinary('RETR ' + f, fh.write)
            else:
                raise Exception('Process Interrupted. Img pull is stopped.')


class SQLController:
    SERVER = 'azrmfgsqlp01'
    DATABASE = 'MfgFstCentral'

    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   f'Server={SQLController.SERVER};'
                                   f'Database={SQLController.DATABASE};'
                                   f'Trusted_Connection=yes;')

    def get_txid_list_from_rejects(self, start_time, end_time, reject_code, tk_status):
        # TO DO: Status
        tk_status.set('Getting TXID List...')
        print('Getting TXID List...')

        cursor = self.conn.cursor()

        print("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
              "WHERE Site = 'SAN' AND "
              f"RejectCode = {reject_code} AND "
              f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")
        cursor.execute("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
                       "WHERE Site = 'SAN' AND "
                       f"RejectCode = {reject_code} AND "
                       f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")

        return [row[0] for row in cursor]

    def get_txid_list(self, start_time, end_time, tk_status):
        # TO DO: Status
        tk_status.set('Getting TXID List...')
        print('Getting TXID List...')

        cursor = self.conn.cursor()

        print("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
              "WHERE Site = 'SAN' AND "
              f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")
        cursor.execute("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
                       "WHERE Site = 'SAN' AND "
                       f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")

        return [row[0] for row in cursor]
