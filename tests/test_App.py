import unittest
from datetime import datetime
from App import Main


class Test(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_get_data(self):
        data = Main.Importdata().get_data('A')
        print(data)
        assert data == datetime.now().strftime("%d_%m_%Y %H-%M-%S")

    def test_get_time(self):
        assert Main.DataLogs().get_time() == datetime.now().strftime("%d_%m_%Y %H-%M-%S")



