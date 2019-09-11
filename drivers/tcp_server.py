# -- coding: utf-8 --
from __future__ import unicode_literals
import threading
import socket
from time import sleep
from Drivers import handlers


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


ip = '192.168.1.120'
port = 4040


class Thread4Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = None
        self.conn = None
        self.addr = None
        self.flag_run = 0

        self.ip = 0
        self.port = 0

        self.acceptThread = Thread4Accept(self.accept_handler, self.accept_error_handler)
        self.speakThread = []

    def run(self):
        print('START SERVER')
        self.sock = socket.socket()
        self.sock.bind((self.ip, int(self.port)))
        self.sock.listen(10)
        self.acceptThread.sock = self.sock
        self.acceptThread.start()
        while self.flag_run:
            sleep(0.01)

    def func_connect(self):
        print('Connecting to {}'.format(self.acceptThread.addr))
        self.speakThread.append(Thread4Speak(self.speak_handler, self.speak_error_handler))
        self.speakThread[len(self.speakThread) - 1].conn = self.acceptThread.conn
        self.speakThread[len(self.speakThread) - 1].addr = self.acceptThread.addr

        self.speakThread[len(self.speakThread) - 1].flag_run = 1
        self.speakThread[len(self.speakThread) - 1].start()

        # 'Number of active clients: %s' % str(len(self.speakThread))

    @staticmethod
    def accept_error_handler(string_err):
        print(string_err)

    def accept_handler(self, accept_conn, accept_addr):
        print(accept_addr)
        print(accept_conn)
        self.func_connect()

    @staticmethod
    def speak_error_handler(string_err, who):
        print('{} from {}'.format(string_err, who))

    @staticmethod
    def speak_handler(string, who):
        print('{} from {}'.format(string, who))


class Thread4Speak(threading.Thread):
    # Need to receive data
    def __init__(self, callback_handler, error_callback_handler):
        threading.Thread.__init__(self)
        self.__handler = callback_handler
        self.__err_handler = error_callback_handler
        self.conn = None
        self.addr = None
        self.flag_run = 0

    def run(self):
        print('Start for {}'.format(self.addr))
        while self.flag_run:
            try:
                data = self.conn.recv(1000000)
            except ConnectionResetError:
                # data = conn.recv(1024).decode()
                # ConnectionResetError: [WinError 10054] Удаленный хост принудительно разорвал существующее подключение
                self.__err_handler('ConnectionResetError', self.addr)
                self.conn.close()
                self.flag_run = 0
                break
            except Exception as err:
                self.__err_handler(str(err), self.addr)
                self.conn.close()
                self.flag_run = 0
                break
            else:
                if not data:
                    self.__err_handler('No data', self.addr)
                    self.conn.close()
                    self.flag_run = 0
                    break
                elif 'close' in data.decode('cp1251'):
                    self.__handler('close_ok', self.addr)
                    self.conn.close()
                    self.flag_run = 0
                    break
                else:
                    udata = data.decode('cp1251')
                    self.__handler(udata, self.addr)


class Thread4Accept(threading.Thread):
    # Need to identity new connection
    def __init__(self, callback_handler, error_callback_handler):
        threading.Thread.__init__(self)
        self.__handler = callback_handler
        self.__err_handler = error_callback_handler
        self.sock = None
        self.conn = None
        self.addr = None

    def run(self):
        while True:
            try:
                self.conn, self.addr = self.sock.accept()
            except Exception as err:
                self.__err_handler('Error accept: {}'.format(err))
                break
            else:
                print("Connection from: " + str(self.addr))
                self.__handler(self.conn, self.addr)


if __name__ == '__main__':
    serverThread = Thread4Server()
    serverThread.ip = ip
    serverThread.port = port
    serverThread.flag_run = 1
    serverThread.start()

    while True:
        sleep(100)



