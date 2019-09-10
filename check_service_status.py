# -- coding: utf-8 --
from __future__ import unicode_literals
import os
import subprocess
import re
from time import sleep
import datetime


# Active: inactive (dead) since Tue 2019-09-10 11:01:27 EEST; 3s ago
# Active: active (running) since Tue 2019-09-10 10:15:22 EEST; 43min ago
print('start')


services = {'application': 'systemctl status application',
            'bios': 'systemctl status bios',
            'bronsrv': 'systemctl status bronsrv',
            'video_streamer': 'systemctl status videostreamer',
            'audio_streamer':'systemctl status audiostreamer',
            'netswitcher': 'systemctl status netswitcher',
            'oad': 'systemctl status oad',
            'update_client': 'systemctl status update_client'
            }
# hist = {'application': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]},
#         'bios': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]},
#         'bronsrv': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]},
#         'video_streamer': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]},
#         'audio_streamer': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]},
#         'netswitcher': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]},
#         'oad': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]},
#         'update_client': {'name': [None], 'last_state': [None], 'start_at': [None], 'ago': [None]}
#         }
hist = {'application': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'bios': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'bronsrv': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'video_streamer': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'audio_streamer': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'netswitcher': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'oad': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'update_client': {'name': None, 'last_state': None, 'start_at': None, 'ago': None}
        }


def check_status(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def print_status(status_app, name_service):
    for number, line in enumerate(status_app.stdout):
        tmp = re.sub(r'[^a-zA-Z0-9:()-;]+', ' ', line.rstrip())

        if parse_status(number, tmp, name_service=name_service):
            print('>>> {} {}\n'.format(name_service, tmp))


def parse_status(integer, sting, name_service):
    if 'Active: ' in sting:
        # current_state = sting.split('Active: ')[1].split(' since')[0]
        current_at_start = sting.split('since ')[1].split(' EEST;')[0]
        # current_ago = sting.split('EEST; ')[1].split(' ago')[0]
        # current_dimention = check_time_dimention(current_ago)

        if hist[name_service]['start_at']:
            # if check_time_dimention(hist[name_service]['ago']) == current_dimention:
            if hist[name_service]['start_at'] != current_at_start:
                hist[name_service]['start_at'] = current_at_start
                return True
            else:
                return False
        else:
            hist[name_service]['start_at'] = current_at_start
            return False


def check_time_dimention(string):
    if 'h' in string:
        return 'h'
    elif 'min' in string:
        return 'min'
    elif 's' in string:
        return 's'


while True:
    for key in services.keys():
        print_status(check_status(services[key]), key)
        # print('\n\n')
    sleep(3)

# os.system('systemctl status application')

# status_application = os.system('systemctl status application')

# print(status_application)
# print(type(status_application))
# print(status_application.find('Active:'))



# os.system('systemctl start application')

