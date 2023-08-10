# SQL Class for use of the Controller class
# Aldo Yew Siswanto
# 08/09/23

import pyodbc

class SQLController:
    SERVER = 'azrmfgsqlp01'
    DATABASE = 'MfgFstCentral'

    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   f'Server={SQLController.SERVER};'
                                   f'Database={SQLController.DATABASE};'
                                   f'Trusted_Connection=yes;')

    def get_txid_list_general(self, start_time, end_time, eq, quality, reject_code, tk_status):
        # TO DO: Status
        tk_status.set('Getting TXID List...')
        print('Getting TXID List...')

        if quality == 'Gd':
            q_string = 'IS NULL'
        elif quality == 'Bd':
            q_string = 'IS NOT NULL'
        elif quality == 'Reject':
            q_string = f'= {reject_code}'

        cursor = self.conn.cursor()

        print("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
              "WHERE Site = 'SAN' AND "
              f"RejectCode {q_string} AND "
              f"EQNumber = '{eq}' AND "
              f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")
        cursor.execute("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
                       "WHERE Site = 'SAN' AND "
                       f"RejectCode {q_string} AND "
                       f"EQNumber = '{eq}' AND "
                       f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")

        return list(set([row[0] for row in cursor if row[0] is not None]))

    def get_txid_list_all(self, start_time, end_time, eq, tk_status):
        # TO DO: Status
        tk_status.set('Getting TXID List...')
        print('Getting TXID List...')

        cursor = self.conn.cursor()

        print("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
              "WHERE Site = 'SAN' AND "
              f"EQNumber = '{eq}' AND "
              f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")
        cursor.execute("SELECT [TXID] FROM [MfgFstCentral].[ENG].[vwFSTProcessRecords]   "
                       "WHERE Site = 'SAN' AND "
                       f"EQNumber = '{eq}' AND "
                       f"CompletedDateTime BETWEEN '{start_time}' AND '{end_time}'")

        return list(set([row[0] for row in cursor if row[0] is not None]))
