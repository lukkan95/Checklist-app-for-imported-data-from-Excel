import unittest
from datetime import datetime
from App import Main
import os
import tkinter as tk


class Test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    # def test_get_data(self):
    #     data = Main.Importdata().get_data('A')
    #     print(data)
    #     assert data == datetime.now().strftime("%d_%m_%Y %H-%M-%S")
    #
    def test_get_time(self):
        assert Main.DataLogs().get_time() == datetime.now().strftime("%d_%m_%Y %H-%M-%S")

    def test_create_test_file(self):
        temp_file = Main.DataLogs().create_text_file()
        with open(temp_file, 'r') as file:
            line = file.readlines()
            assert line[0] != 0
        path = f'{os.path.dirname(os.path.realpath(__file__))}\{temp_file}'
        os.remove(path)

    def test_add_checkbutton_and_log_status_of_checkbutton(self):
        temp_checkbutton = Main.Figure1().add_checkbutton('test_checkbutton', '0', progressbar=None, label_progressbar=None)
        # temp_file = Main.DataLogs().create_text_file()
        Main.DataLogs.log_status_of_checkbutton(listbox=None, name='Test', value=, sheet_name='0', filename=temp_file)


        assert temp_checkbutton






