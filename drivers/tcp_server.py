# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
import socket
from time import sleep
import datetime
import json
import pickle
from drivers.log_settings import log


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"

my_ip = socket.gethostbyname_ex(socket.gethostname())  # [2][0]
print(my_ip)

ip_vpn = '10.8.0.5'
ip_local = '192.168.0.49'
port = 1717


class Thread4Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None
        self.connection = None
        self.address = None
        self.flag_run = 0
        self.info = dict()
        # data_s = pickle.load(open('d:\qua\check_service_status\drivers\\battery_discharge.io', 'rb'))

        self.ip = 0
        self.port = 0

        self.acceptThread = Thread4Accept(self.accept_handler, self.accept_error_handler)
        self.speakThread = dict()

    def run(self):
        print('START SERVER')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, int(self.port)))
        self.sock.listen(10)
        self.acceptThread.sock = self.sock
        self.acceptThread.start()
        while self.flag_run:
            sleep(0.01)

    def func_connect(self):
        print('Connecting to {}'.format(self.acceptThread.address))
        # mySocket.send(message)
        self.speakThread[self.acceptThread.address] = Thread4Speak(self.speak_handler, self.speak_error_handler)
        self.speakThread[self.acceptThread.address].conn = self.acceptThread.connection
        self.speakThread[self.acceptThread.address].addr = self.acceptThread.address

        self.speakThread[self.acceptThread.address].flag_run = 1
        self.speakThread[self.acceptThread.address].start()

        print(self.speakThread)

        # 'Number of active clients: %s' % str(len(self.speakThread))

    @staticmethod
    def accept_error_handler(string_err):
        print(string_err)

    def accept_handler(self, accept_conn, accept_addr):
        print(accept_addr)
        print(accept_conn)
        self.func_connect()

    def speak_error_handler(self, string_err, who):
        print('{} from {}'.format(string_err, who))
        self.speakThread.pop(who)
        print(self.speakThread)

    def speak_handler(self, string, who):
        try:
            print('{}: {} from {}'.format(datetime.datetime.now(), json.loads(string), who))
        except Exception as err:
            print('{}\n{}\n{}'.format(datetime.datetime.now(), err, string))

        try:
            self.info[datetime.datetime.now()] = json.loads(string)
        except Exception as err:
            print('{}\n{}\n{}'.format(datetime.datetime.now(), err, string))

        try:
            pickle.dump(self.info, open('battery_discharge.io', 'wb'))
        except Exception as err:
            print('{}\n{}\n{}'.format(datetime.datetime.now(), err, string))


class Thread4Speak(threading.Thread):
    # Need to receive data
    def __init__(self, callback_handler, error_callback_handler):
        threading.Thread.__init__(self)
        self.__handler = callback_handler
        self.__err_handler = error_callback_handler
        self.connection = None
        self.address = None
        self.flag_run = 0

    def run(self):
        print('Start for {}'.format(self.address))
        while self.flag_run:
            try:
                data = self.connection.recv(1000000)
            except ConnectionResetError:
                # data = conn.recv(1024).decode()
                # ConnectionResetError: [WinError 10054] Удаленный хост принудительно разорвал существующее подключение
                self.__err_handler('ConnectionResetError', self.address)
                self.connection.close()
                self.flag_run = 0
                break
            except Exception as err:
                self.__err_handler(str(err), self.address)
                self.connection.close()
                self.flag_run = 0
                break
            else:
                if not data:
                    self.__err_handler('No data', self.address)
                    self.connection.close()
                    self.flag_run = 0
                    break
                elif 'close' in data.decode('cp1251'):
                    self.__handler('close_ok', self.address)
                    self.connection.close()
                    self.flag_run = 0
                    break
                else:
                    udata = data.decode('cp1251')
                    self.__handler(udata, self.address)


class Thread4Accept(threading.Thread):
    # Need to identity new connection
    def __init__(self, callback_handler, error_callback_handler):
        threading.Thread.__init__(self)
        self.__handler = callback_handler
        self.__err_handler = error_callback_handler
        self.sock = None
        self.connection = None
        self.address = None

    def run(self):
        while True:
            try:
                self.connection, self.address = self.sock.accept()
            except Exception as err:
                self.__err_handler('Error accept: {}'.format(err))
                break
            else:
                log.info("Connection from: " + str(self.address))
                # self.check_new_acceptance()
                self.__handler(self.connection, self.address)

    def check_new_acceptance(self):
        log.info('ask from connection: {}, address: {} password'.format(self.connection, self.address))
        self.connection.send(bytes('Password', encoding='UTF-8'))


if __name__ == '__main__':
    serverThread = Thread4Server()
    serverThread.ip = ip_vpn
    serverThread.port = port
    serverThread.flag_run = 1
    serverThread.start()

    while True:
        sleep(100)



