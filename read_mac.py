# -- coding: utf-8 --
from __future__ import unicode_literals
import sys
import subprocess


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


def get_mac(cmd):
    response = read_mac(cmd=cmd)
    response_strings = parse(response)

    for i in response_strings:
        if 'eth1' in i:
            find_eth1(i)
        elif 'wlan0' in i:
            find_wlan0(i)


def parse(response):
    string = list()
    number_segment = 0
    string.append(str())
    for number, line in enumerate(response.stdout):
        if '\n' == line:
            number_segment += 1
            string.append(str())
        else:
            string[number_segment] += line
    return string


def read_mac(cmd):
    try:
        response = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    except Exception as err:
        print(err)
        sys.exit(0)
    else:
        return response


def find_eth1(data):
    if 'HWaddr' in data:
        return data.split('HWaddr ')[1].split('\n')[0]
    return None


def find_wlan0(data):
    if 'HWaddr' in data:
        return data.split('HWaddr ')[1].split('\n')[0]
    return None


if __name__ == '__main__':
    get_mac('ifconfig')



