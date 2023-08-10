import unittest
import tkinter as tk
from FTP_GetImagesNameGeneratorClass import GetImagesNameGenerator
import ftplib
from ImgFTPModel import ImgFTPModel

class MyTestCase(unittest.TestCase):
    def testNameGenerator(self):
        ftp = ftplib.FTP("10.3.84.33", "nth", "nthnth1")
        ftp.cwd('/Images/EQ-901853-004/2023/08/09')

        root = tk.Tk()
        model = ImgFTPModel(root)
        model.eq = "SNL"

        txid_list = [940750706871,
                     940755119537,
                     942062856120]

        target_path = r"C:\Users\as0621\OneDrive - Dexcom\Images\Test"
        var = GetImagesNameGenerator(txid_list, model, ftp, target_path)
        var.IMG_NUM_ITER_START = 70
        var.get(tk.StringVar())

if __name__ == '__main__':
    unittest.main()
