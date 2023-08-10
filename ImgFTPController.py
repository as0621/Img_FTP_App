# Img FTP Controller File
# Aldo Siswanto
# 2023/07/08

import tkinter as tk
from Controller_FTPClass import FTPController
from Controller_SQLClass import SQLController


class ImgFTPController:
    VERSION = "1.1.0"

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

        if self.model.quality == 'All':
            sql_txid_list = self.sql.get_txid_list_all(self.model.start_datetime,
                                                       self.model.end_datetime,
                                                       self.model.eq_number,
                                                       tk_status)
        else:
            sql_txid_list = self.sql.get_txid_list_general(self.model.start_datetime,
                                                           self.model.end_datetime,
                                                           self.model.eq_number,
                                                           self.model.quality,
                                                           self.model.selected_reject,
                                                           tk_status)

        if len(sql_txid_list) > 0:
            for day in self.model.list_of_days:
                tk_status.set(f'Getting data for day: {day}')
                self.ftp.get_images(self.model, f"{day:02d}", tk_status, txid_list=sql_txid_list)

                tk_status.set('DONE')
                return 0
        else:
            tk_status.set(f'ERROR: No {self.model.eq} {self.model.selected_reject} Rejects.')
