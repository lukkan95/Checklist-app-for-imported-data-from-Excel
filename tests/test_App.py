import unittest
from datetime import datetime
from App import Main
import os
import tkinter as tk


class Test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)


    def test_get_time(self):
        assert Main.ConvertedDateTime.get_time() == datetime.now().strftime("%d_%m_%Y %H-%M-%S")

    def test_create_test_file(self):
        temp_file = Main.DataToTxt().create_text_file()
        with open(temp_file, 'r') as file:
            line = file.readlines()
            assert line[0] != 0
        path = f'{os.path.dirname(os.path.realpath(__file__))}\{temp_file}'
        os.remove(path)






