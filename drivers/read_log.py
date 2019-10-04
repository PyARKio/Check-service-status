# -- coding: utf-8 --
from __future__ import unicode_literals
import pickle


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


data_s = pickle.load(open('d:\qua\check_service_status\drivers\\battery.io', 'rb'))
for data in data_s:
    print('{}: {}'.format(data, data_s[data]))


