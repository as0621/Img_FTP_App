import unittest
from FTP_CreateDirectoryClass import CreateDirectory
# from FTP_CreateDirectoryRejectClass import CreateDirectoryReject


class MyTestCase(unittest.TestCase):
    def testCreateTargetPath(self):
        create_dir_obj = CreateDirectory(r"C:\Users\as0621\OneDrive - Dexcom\Images",
                                         "EQ-000000",
                                         "2023",
                                         "08",
                                         "09",
                                         "Gd")

        self.assertEqual(r"C:\Users\as0621\OneDrive - Dexcom\Images\EQ-000000\2023\08\09\Gd",
                         create_dir_obj.target_path_directory)

    def testCreateTargetPathRejects(self):
        create_dir_obj = CreateDirectory(r"C:\Users\as0621\OneDrive - Dexcom\Images",
                                         "EQ-000000",
                                         "2023",
                                         "08",
                                         "09",
                                         "Bd",
                                         "6208")

        self.assertEqual(r"C:\Users\as0621\OneDrive - Dexcom\Images\EQ-000000\2023\08\09\Bd\6208",
                         create_dir_obj.target_path_directory)

if __name__ == '__main__':
    unittest.main()
