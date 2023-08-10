# Get Images from FTP server using name generating method
# Aldo Yew Siswanto
# 08/09/23
import ftplib
import os

from FTP_GetImagesNLSTClass import GetImagesNlst


class GetImagesNameGenerator(GetImagesNlst):
    IMG_NUM_ITER_START = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, tk_status):
        camera_inspection_list = self.model.cam_inspection_list

        if self.model.inspection:
            camera_inspection_list = [inspection for inspection in camera_inspection_list if
                                      self.model.inspection in inspection]

        for txid in self.txid_list:
            for inspection in camera_inspection_list:
                self.__pull_images(inspection, txid, tk_status, "Gd")
                self.__pull_images(inspection, txid, tk_status, "Bd")

    def __pull_images(self, inspection, txid, tk_status, status):
        img_num_iter = GetImagesNameGenerator.IMG_NUM_ITER_START
        while img_num_iter < 100:
            try:
                file_name = f"{self.model.line}{self.model.eq}{inspection}_{status}_{txid}_{img_num_iter}.bmp"

                self.get_images_single(file_name, len(self.txid_list), tk_status)

                img_num_iter += 1
                print(img_num_iter)
            except ftplib.error_perm:
                os.unlink(os.path.join(self.target_path, file_name))
                return
