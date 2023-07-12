# Img FTP Controller File
# Aldo Siswanto
# 2023/07/08

from ImgFTPModel import ImgFTPModel
import mysql.connector as mysql
import pyodbc
import os
import ftplib
import tkinter as tk


class ImgFTPController:
    VERSION = "0.0.1"
    def __init__(self, model):
        self.model = model
        self.sql = SQLController()
        self.ftp = FTPController()
        self.target_path_directory = None

    def test_print(self):
        print(f"Executing Request\n"
              f"-----------------\n"
              f"start datetime: {self.model.start_datetime}\n"
              f"end datetime: {self.model.end_datetime}\n"
              f"home: {self.model.home_directory}\n"
              f"eq: {self.model.eq}\n"
              f"eq no: {self.model.eq_number}\n"
              f"quality: {self.model.quality}\n"
              f"reject: {self.model.selected_reject}\n"
              f"inspection: {self.model.inspection}\n"
              # f"save_txid: {model.settings_save_txid}\n"
              f"use_scada: {self.model.settings_use_scada}\n")

    def test_get_txid_list(self):
        txid_list = self.sql.get_txid_list_from_rejects(self.model.start_datetime,
                                                        self.model.end_datetime,
                                                        self.model.selected_reject)

        print(txid_list)

    def get_images(self, tk_status):
        # print(self.model)

        sql_txid_list = self.sql.get_txid_list_from_rejects(self.model.start_datetime,
                                                            self.model.end_datetime,
                                                            self.model.selected_reject,
                                                            tk_status)

        if len(sql_txid_list) > 0:
            name_list = self.ftp.get_images_list(self.model.home_directory,
                                                 self.model.eq,
                                                 self.model.eq_number,
                                                 self.model.start_year,
                                                 self.model.start_month,
                                                 self.model.start_day,
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

    def create_dir(self, home_dir, eq, year, month, day, quality, reject):
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
        tk_status.set('Creating local directory...')
        print("Creating local directory....")
        self.create_dir(home_dir, eq, year, month, day, quality, reject)  # Create local directory

        tk_status.set('Getting directory...')
        print("Getting directory....")
        self.change_ftp_dir(eq_num, year, month, day)

        name_list = self.ftp.nlst('*.bmp')
        name_list = [f"{name}" for name in name_list if any(txid in name for txid in txid_list)]

        # Inspection Filter
        if inspection:
            name_list = [f"{name}" for name in name_list if inspection in name]

        return name_list

    def get_images(self, name_list, tk_status):
        tk_status.set('Starting Transfer...')
        for f in name_list:
            tk_status.set("Transferring " + str(f) + "....")
            print("Transferring " + str(f) + "....")
            with open(os.path.join(self.target_path_directory, f), 'wb') as fh:
                self.ftp.retrbinary('RETR ' + f, fh.write)


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
