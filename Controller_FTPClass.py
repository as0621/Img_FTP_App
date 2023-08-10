# FTP Class for use of the Controller class
# Aldo Yew Siswanto
# 08/09/23

import ftplib
from FTP_CreateDirectoryClass import CreateDirectory
from FTP_GetImagesNLSTClass import GetImagesNlst
from FTP_GetImagesNameGeneratorTest import GetImagesNameGenerator


class FTPController:
    HOSTNAME = "10.3.84.33"
    USERNAME = "nth"
    PASSWORD = "nthnth1"

    CREATE_DIR_CLASS = CreateDirectory
    IMG_PULL_CLASS = GetImagesNameGenerator

    def __init__(self):
        self.target_path_directory = None
        self.ftp = ftplib.FTP(FTPController.HOSTNAME, FTPController.USERNAME, FTPController.PASSWORD)

    def change_ftp_dir(self, eq_num, year, month, day):
        image_path = f'/Images/{eq_num}/{year}/{month}/{day}'
        self.ftp.cwd(image_path)

    def get_images(self, model, current_day, tk_status,
                   txid_list=None,
                   create_dir=CREATE_DIR_CLASS,
                   get_images=IMG_PULL_CLASS):
        if model.quality == 'Reject':
            create_dir_var = create_dir(model.home_directory, model.eq, model.start_year, model.start_month,
                                        current_day, model.quality, model.selected_reject)
        else:
            create_dir_var = create_dir(model.home_directory, model.eq, model.start_year, model.start_month,
                                        current_day, model.quality)

        # Create Directory
        tk_status.set('Creating local directory...')
        create_dir_var.create()

        # Entering FTP Directory
        tk_status.set(f'Getting directory for {model.start_year}/{model.start_month}/{current_day}...')
        self.change_ftp_dir(model.eq_number, model.start_year, model.start_month, current_day)

        # Pull Images
        get_images_var = get_images(txid_list, model, self.ftp, create_dir_var.target_path_directory)
        get_images_var.get(tk_status)
