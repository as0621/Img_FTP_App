# Create Directory Class for use of the Controller class
# Aldo Yew Siswanto
# 08/09/23
import os


class CreateDirectory:
    def __init__(self, *args):
        self.target_path_directory = self.create_target_path(*args)

    @staticmethod
    def create_target_path(*args):
        return os.path.join(*args)

    def create(self):
        if not os.path.exists(self.target_path_directory):
            os.makedirs(self.target_path_directory)
