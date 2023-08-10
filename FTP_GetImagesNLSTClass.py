# Get Images from FTP server using NLST method
# Aldo Yew Siswanto
# 08/09/23

import os


class GetImagesNlst:
    def __init__(self, txid_list, model, ftp, target_path):
        self.txid_list = txid_list
        self.model = model
        self.ftp = ftp
        self.target_path = target_path

    def get(self, tk_status):
        # Getting all files from directory
        name_list = self.ftp.nlst()

        tk_status.set(f'Filtering Images for .bmp')
        name_list = [f"{name}" for name in name_list if '.bmp' in name]

        # Inspection Filter
        tk_status.set(f'Filtering Images for Inspection')
        if self.model.inspection:
            name_list = [f"{name}" for name in name_list if self.model.inspection in name]

        tk_status.set(f'Filtering Images for txid list')

        for name in name_list:
            if any(txid in name for txid in self.txid_list):
                self.get_images_single(name, len(self.txid_list), tk_status)

    def get_images_single(self, name, total_n, tk_status):
        if tk_status.get() == 'STOP':
            raise Exception('Process Interrupted. Img pull is stopped.')

        with open(os.path.join(self.target_path, name), 'wb') as fh:
            self.ftp.retrbinary('RETR ' + name, fh.write)

        tk_status.set(f"Found {total_n} TxIDs. Transferred {name}....")