import unittest
from ImgFTPModel import *


class MyTestCase(unittest.TestCase):
    def testListOfDays(self):
        root = tk.Tk()
        model = ImgFTPModel(root)
        model.start_datetime = '2023-06-01 00:00:00'
        model.end_datetime = '2023-06-05 00:00:00'

        self.assertEqual(model.list_of_days, [1,2,3,4,5])


if __name__ == '__main__':
    unittest.main()
