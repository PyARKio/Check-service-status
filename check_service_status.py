# -- coding: utf-8 --
from __future__ import unicode_literals
import config
import subprocess
import re
from time import sleep
import datetime
import time
from drivers.log_settings import log


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


# Active: inactive (dead) since Tue 2019-09-10 11:01:27 EEST; 3s ago
# Active: active (running) since Tue 2019-09-10 10:15:22 EEST; 43min ago
log.info('Starting of check_service_status')


services = {'application': 'systemctl status application',
            'bios': 'systemctl status bios',
            'bronsrv': 'systemctl status bronsrv',
            'video_streamer': 'systemctl status videostreamer',
            'audio_streamer':'systemctl status audiostreamer',
            'netswitcher': 'systemctl status netswitcher',
            'oad': 'systemctl status oad',
            'update_client': 'systemctl status update_client',
            'wvdial': 'systemctl status wvdial',
            'openvpn-client': 'systemctl status openvpn-client',
            'chromeapp': 'systemctl status chromeapp',
            'ntp': 'systemctl status ntp',
            'user@1000': 'systemctl status user@1000',
            'polkitd': 'systemctl status polkidt',
            'wpa_supplicant': 'systemctl status wpa_supplicant',
            'nginx': 'systemctl status nginx',
            'shh': 'systemctl status ssh',
            'redis-server': 'systemctl status redis-server',
            'systemd-logind': 'systemctl status systemd-logind',
            'NetworkManager': 'systemctl status NetworkManager',
            'dbus': 'systemctl status dbus',
            'cron': 'systemctl status cron',
            'rsyslog': 'systemctl status rsyslog',
            'mosquitto': 'systemctl status mosquitto',
            'mongodb': 'systemctl status mongodb',
            'system-getty': 'systemctl status system-getty',
            'systemd-journald': 'systemctl status systemd-journald',
            'desktop-splash': 'systemctl status desktop-splash',
            'haveged': 'systemctl status haveged',
            'systemd-udevd': 'systemctl status systemd-udevd',
            'serial-getty@ttyS0': 'systemctl status serial-getty@ttyS0'
            }


hist = {'application': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'bios': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'bronsrv': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'video_streamer': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'audio_streamer': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'netswitcher': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'oad': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'wvdial': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'openvpn-client': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'chromeapp': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'ntp': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'user@1000': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'polkitd': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'wpa_supplicant': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'nginx': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'shh': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'redis-server': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'systemd-logind': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'NetworkManager': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'dbus': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'cron': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'rsyslog': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'mosquitto': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'mongodb': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'system-getty': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'systemd-journald': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'desktop-splash': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'haveged': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'systemd-udevd': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'serial-getty@ttyS0': {'name': None, 'last_state': None, 'start_at': None, 'ago': None},
        'update_client': {'name': None, 'last_state': None, 'start_at': None, 'ago': None}
        }


log.info('All services:')
for key in services.keys():
    log.info(key)
log.info('')


def check_status(cmd):
    try:
        response = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    except Exception as err:
        log.error(err)
        return False
    else:
        log.info('Response: successfully')
        return response


def print_status(status_app, name_service):
    if status_app:
        for number, line in enumerate(status_app.stdout):
            tmp = re.sub(r'[^a-zA-Z0-9:()-;]+', ' ', line.rstrip())
            if number == 0 or number == 2:
                log.info(tmp)

            if parse_status(number, tmp, name_service=name_service):
                log.info('\n' + '*' * 25)
                log.info('Service {} change state\n>>> {}'.format(name_service, tmp))
                print('>>> {} {}'.format(name_service, tmp))

                re_tmp = str()
                for i in tmp.split('since ')[1].split(' EEST;')[0].split(' '):
                    re_tmp += '_{}'.format(re.sub(r'[^a-zA-Z0-9()]+', '_', i))

                dir_name = '{}{}'.format(name_service, re_tmp)
                mkdir_for_syslog(dir_name)
                cp_syslog(dir_name)
                log.info('\n' + '*' * 25 + '\n')


def parse_status(integer, sting, name_service):
    if 'Active: ' in sting:
        # current_state = sting.split('Active: ')[1].split(' since')[0]
        try:
            current_at_start = sting.split('since ')[1].split(' EEST;')[0]
        except Exception as err:
            log.error(err)
            return False
        # current_ago = sting.split('EEST; ')[1].split(' ago')[0]
        # current_dimention = check_time_dimention(current_ago)
        else:
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


def mkdir_for_syslog(dir_name):
    log.info('mkdir /home/user/{}'.format(dir_name))
    try:
        subprocess.Popen('mkdir /home/user/{}'.format(dir_name), shell=True, stdout=subprocess.PIPE)
    except Exception as err:
        log.error(err)
    else:
        log.info('mkdir successfully')


def cp_syslog(dir_name):
    log.info('cp /var/log/syslog /home/user/{}'.format(dir_name))
    try:
        subprocess.Popen('cp /var/log/syslog /home/user/{}'.format(dir_name), shell=True, stdout=subprocess.PIPE)
    except Exception as err:
        log.error(err)
    else:
        log.info('cp syslog successfully')


while True:
    for key in services.keys():
        log.info('Check status for {}'.format(key))
        print_status(check_status(services[key]), key)
        log.info('\n')

    log.info('Sleep at {}'.format(config.sleep_at))
    sleep(config.sleep_at)








