# -- coding: utf-8 --
from __future__ import unicode_literals
import pickle


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


# data_s = pickle.load(open('d:\qua\check_service_status\drivers\\battery.io', 'rb'))
data_s = pickle.load(open('d:\qua\check_service_status\drivers\\battery_discharge.io', 'rb'))
for data in data_s:
    print('{}: {}'.format(data, data_s[data]))

print(len(data_s))
print(type(list(data_s.keys())[0]))
print(list(data_s.keys())[0])


