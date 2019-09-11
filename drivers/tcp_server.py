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


class ServerOnSocket():
    def __init__(self):
        self.my_ip = socket.gethostbyname_ex(socket.gethostname())[2][0]

        self.serverThread = Thread4Server()
        # self.acceptThread = Thread4Accept()
        self.speakThread = []

        self.connect(self.button_listen, QtCore.SIGNAL('clicked()'), self.func_listen)
        self.connect(self.button_send, QtCore.SIGNAL('clicked()'), self.func_send)
        # self.connect(self.acceptThread, QtCore.SIGNAL("newAccept(QString)"),
        #              self.func_connect, QtCore.Qt.QueuedConnection)
        self.connect(self.serverThread, QtCore.SIGNAL("rec(QString)"),
                     self.func_rec, QtCore.Qt.QueuedConnection)
        self.connect(self.serverThread, QtCore.SIGNAL("label_clients(QString)"),
                     self.func_label_client, QtCore.Qt.QueuedConnection)

    # *****************************************************************
    def func_listen(self):
        if self.button_listen.text() == 'Listen':
            self.button_listen.setText('Close')
            self.serverThread.ip = self.text_ip.text()
            self.serverThread.port = self.text_port.text()
            self.serverThread.flag_run = 1
            self.serverThread.start()

            # self.sock = socket.socket()
            # self.sock.bind((self.text_ip.text(), int(self.text_port.text())))
            # self.sock.listen(10)
            # self.acceptThread.sock = self.sock
            # self.acceptThread.start()
        else:
            # self.acceptThread.terminate()
            for number in range(len(self.speakThread)):
                self.speakThread[number].terminate()
                while self.speakThread[number].isRunning():
                    print('running')
                if self.speakThread[number].isFinished():
                    print('speak OK')
                    self.speakThread[number].conn.close()
                else:
                    print('speak BAD')
                    self.speakThread[number].terminate()
                    self.speakThread[number].conn.close()

            if self.acceptThread.isFinished():
                print('accept OK')
                self.sock.close()
            else:
                print('accept BAD')
                self.acceptThread.terminate()
                if self.acceptThread.isFinished():
                    print('accept OK')
                    self.sock.close()
                else:
                    print('accept BAD')

            self.speakThread = []
            self.serverThread.flag_run = 0
            self.button_listen.setText('Listen')
        self.label_clients.setText('Number of active clients: %s' % str(len(self.speakThread)))
        # subprocess.Popen('pyinstaller -F work_with_socet.py')

    def func_connect(self):
        self.speakThread.append(Thread4Speak())
        self.connect(self.speakThread[len(self.speakThread) - 1], QtCore.SIGNAL("newM(QString)"),
                     self.func_rec, QtCore.Qt.QueuedConnection)
        self.connect(self.speakThread[len(self.speakThread) - 1], QtCore.SIGNAL("newClose(QString)"),
                     self.func_close_session, QtCore.Qt.QueuedConnection)
        self.speakThread[len(self.speakThread) - 1].conn = self.acceptThread.conn
        self.speakThread[len(self.speakThread) - 1].addr = self.acceptThread.addr

        self.func_write_log('  ' + str(self.acceptThread.conn))
        self.func_write_log('  ' + str(self.acceptThread.addr))

        self.speakThread[len(self.speakThread) - 1].flag_run = 1
        self.speakThread[len(self.speakThread) - 1].start()

        self.label_clients.setText('Number of active clients: %s' % str(len(self.speakThread)))

    def func_close_session(self, temp):
        print(temp)
        print('')
        number_del = -1
        for number in range(len(self.speakThread)):
            print(self.speakThread[number].addr)
            if temp == str(self.speakThread[number].addr):
                print('FIND')
                number_del = number

        if number_del != -1:
            if self.speakThread[number_del].isFinished():
                print('OK')
                self.speakThread.pop(number_del)
            else:
                print('BAD')
                self.speakThread[number_del].terminate()
                self.speakThread.pop(number_del)
        else:
            self.func_write_log('  can\'t find ' + str(temp))

        print('')
        for number in range(len(self.speakThread)):
            print(self.speakThread[number].addr)

        self.label_clients.setText('Number of active clients: %s' % str(len(self.speakThread)))

        # self.speakThread[0].conn.send(''.encode('cp1251'))
        # self.speakThread[0].conn.send(b'')

    def calculate_rx(self):
        if self.counter_rx > 1024:
            if self.counter_rx > 1048576:
                self.rx_text_bytes = 'Mb'
                text_temp_rx = str(float(self.counter_rx / 1048576)).split('.')
                text_rx = text_temp_rx[0] + '.' + list(text_temp_rx[1])[0] + list(text_temp_rx[1])[1]
                number_bytes = text_rx
            else:
                self.rx_text_bytes = 'kb'
                text_temp_rx = str(float(self.counter_rx / 1024)).split('.')
                text_rx = text_temp_rx[0] + '.' + list(text_temp_rx[1])[0] + list(text_temp_rx[1])[1]
                number_bytes = text_rx
        else:
            self.rx_text_bytes = 'b'
            number_bytes = str(self.counter_rx)

        text4Button = 'Rx: %s' %number_bytes + '%s' %self.rx_text_bytes
        self.button_counter_rx_bytes.setText(text4Button)

    def calculate_tx(self):
        if self.counter_tx > 1024:
            if self.counter_tx > 1048576:
                self.tx_text_bytes = 'Mb'
                text_temp_tx = str(float(self.counter_tx / 1048576)).split('.')
                text_tx = text_temp_tx[0] + '.' + list(text_temp_tx[1])[0] + list(text_temp_tx[1])[1]
                number_bytes = text_tx
            else:
                self.tx_text_bytes = 'kb'
                text_temp_tx = str(self.counter_tx / 1024).split('.')
                text_tx = text_temp_tx[0] + '.' + list(text_temp_tx[1])[0] + list(text_temp_tx[1])[1]
                number_bytes = text_tx
        else:
            self.tx_text_bytes = 'b'
            number_bytes = str(self.counter_tx)

        text4Button = 'Tx: %s' %number_bytes + '%s' %self.tx_text_bytes
        self.button_counter_tx_bytes.setText(text4Button)

    def func_send(self, string):
        temp = string.encode('cp1251')
        temp += b'\n'
        self.counter_tx += len(temp)
        self.counter_tx_arc.append(self.counter_tx)

        self.calculate_tx()

        if self.serverThread.speakThread:
            self.serverThread.func_send(temp)
            self.func_write_log('  ans from server  ' + str(temp))
        else:
            self.func_write_log('  NO ACTIVE CLIENTS !!!')

    def func_rec(self, temp):
        self.func_write_log('  ' + str(temp))
        self.counter_rx += len(temp)
        self.counter_rx_arc.append(self.counter_rx)

        self.calculate_rx()

        self.text_rec.append(temp)

        if 'DEVICE_TYPE:11' in temp:
            self.counter_time_arc.append(str(datetime.now()).split('.')[0].split(' ')[0] + '\n' + str(datetime.now()).split('.')[0].split(' ')[1])

            calc_crc = 0
            pack_crc = temp.split('CRC32B:')[1].split('\r\n')[0]
            try:
                calc_crc = (hex(binascii.crc32(temp.split('CRC32B:')[0].encode()))).split('x')[1].upper()
            except:
                print('error crc')

            if pack_crc == calc_crc:
                print('good')
                answer = self.parseRx_handlerSlaveError(temp)
                self.parseRx_handlerSlaveData(temp)

                temp_list = temp.split('\r\n')
                data = str()
                for number in range(len(temp_list)):
                    data += temp_list[number] + '*'
                print(data)
                answer += ',' + self.new_time.text() + ',' + self.new_number.text()
                self.id = temp_list[0].split(':')[1]
                self.func_write_data(temp_list[0].split(':')[1], data)
                self.parseRx_DatPack(temp_list)
            else:
                for number_ff in range(8 - len(calc_crc)):
                    calc_crc = '0' + calc_crc
                    # print(crc_calculate)
                    # print(crc_data.decode())
                if pack_crc == calc_crc:
                    print('double good')
                    answer = self.parseRx_handlerSlaveError(temp)
                    self.parseRx_handlerSlaveData(temp)

                    temp_list = temp.split('\r\n')
                    data = str()
                    for number in range(len(temp_list)):
                        data += temp_list[number] + '*'
                    print(data)
                    answer += ',' + self.new_time.text() + ',' + self.new_number.text()
                    self.id = temp_list[0].split(':')[1]
                    self.func_write_data(temp_list[0].split(':')[1], data)
                    self.parseRx_DatPack(temp_list)
                else:
                    print('not good')
                    answer = '404'
        elif '$ERR:' in temp:
            self.counter_time_arc.append(str(datetime.now()).split('.')[0].split(' ')[0] + '\n' + str(datetime.now()).split('.')[0].split(' ')[1])

            answer = '200'
            temp_split = temp.split(',')
            print('')
            print('*************************************************************')
            print('')
            for number in range(len(temp_split)):
                print(str(number) + ' - ' + temp_split[number])
            print('')
            print('*************************************************************')
            print('')
            self.func_write_error(self.id, temp)
            self.parseRx_ErrPack(temp_split)
        else:
            answer = '404'
            print('BAD')
        # answer = '200'

        # answer to client !!!
        self.func_send(answer)


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

"""
    def func_close_session(self, temp):
        print('close session')
        new_time = str(datetime.now())
        print(new_time)
        # print(temp)
        print(len(self.speakThread))
        print('')
        try:
            file = open('stab_test_1', 'a')
            file.write(new_time + temp + '\n')
            file.close()
        except:
            file = open('stab_test_1', 'w')
            file.write(new_time + temp + '\n')
            file.close()

        print(temp)
        print('')
        number_del = -1
        for number in range(len(self.speakThread)):
            print(self.speakThread[number].addr)
            if temp == str(self.speakThread[number].addr):
                print('FIND')
                number_del = number

        if number_del != -1:
            if self.speakThread[number_del].isFinished():
                print('OK')
                self.speakThread.pop(number_del)
            else:
                print('BAD')
                self.speakThread[number_del].terminate()
                self.speakThread.pop(number_del)
        else:
            # self.func_write_log('  can\'t find ' + str(temp))
            print('can\'t find ' + str(temp))

        print('')
        for number in range(len(self.speakThread)):
            print(self.speakThread[number].addr)

        self.emit(QtCore.SIGNAL("label_clients(QString)"), 'Number of active clients: %s' % str(len(self.speakThread)))
        # self.label_clients.setText('Number of active clients: %s' % str(len(self.speakThread)))

    def func_send(self, temp):
        if self.speakThread:
            for number in range(len(self.speakThread)):
                self.speakThread[number].conn.send(temp)
                print('server  ' + str(temp))
        else:
            self.func_write_log('  NO ACTIVE CLIENTS !!!')
"""


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



