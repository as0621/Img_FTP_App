# Img FTP Model File
# Aldo Siswanto
# 2023/07/08

class ImgFTPModel:
    VERSION = "0.0.1"
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

    def __init__(self):
        self.start_datetime = None
        self.end_datetime = None
        self.home_directory = None
        self.eq = None
        self.quality = None
        self.reject = None
        self.inspection = None
        self.settings_save_txid = None

    @property
    def start_datetime(self):
        return self._start_datetime

    @start_datetime.setter
    def start_datetime(self, start_datetime):
        self._start_datetime = start_datetime

    @property
    def end_datetime(self):
        return self._end_datetime

    @end_datetime.setter
    def end_datetime(self, end_datetime):
        self._end_datetime = end_datetime

    @property
    def eq(self):
        return self._eq

    @eq.setter
    def eq(self, eq):
        self._eq = eq

