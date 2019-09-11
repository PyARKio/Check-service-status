# -- coding: utf-8 --
from __future__ import unicode_literals


__author__ = "PyARKio"
__version__ = "1.0.1"
__email__ = "fedoretss@gmail.com"
__status__ = "Production"


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


