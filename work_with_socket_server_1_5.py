#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import socket
from datetime import datetime
import os
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from time import sleep

import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from functools import wraps
import detal_info
import Adaptability


mpl.rcParams['font.family'] = 'fantasy'
mpl.rcParams['font.fantasy'] = 'Arial'


labelStyle_3 = """QLabel{background-color: red}"""


def left_click_press(func, parent):
    @wraps(func)
    def wrapper(evt):
        QtGui.QLabel.mousePressEvent(parent, evt)

        if evt.button() == QtCore.Qt.LeftButton:
            parent.emit(QtCore.SIGNAL('leftClickedPress()'))
        func(evt)

    return wrapper


def left_click_release(func, parent):
    @wraps(func)
    def wrapper(evt):
        QtGui.QLabel.mousePressEvent(parent, evt)

        if evt.button() == QtCore.Qt.LeftButton:
            parent.emit(QtCore.SIGNAL('leftClickedRelease()'))
        func(evt)

    return wrapper


class ServerOnSocket(QtGui.QMainWindow, QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.time_clear_point = str(datetime.now()).split(' ')[0]
        print(self.time_clear_point)

        self.my_ip = socket.gethostbyname_ex(socket.gethostname())[2][0]

        self.adaptiveCoordinateLabelSensor = Adaptability.AdaptiveSizeButton()
        self.detal_info_sensor_1 = detal_info.Calendar(self)
        self.detal_info_sensor_2 = detal_info.Calendar(self)
        self.detal_info_sensor_3 = detal_info.Calendar(self)
        self.detal_info_sensor_4 = detal_info.Calendar(self)
        self.detal_info_sensor_5 = detal_info.Calendar(self)
        self.detal_info_sensor_6 = detal_info.Calendar(self)
        self.detal_info_sensor_7 = detal_info.Calendar(self)
        self.detal_info_sensor_8 = detal_info.Calendar(self)
        self.detal_info_sensor_9 = detal_info.Calendar(self)
        self.detal_info_sensor_10 = detal_info.Calendar(self)

        self.info_bat = detal_info.StatGr(self)
        self.info_tem = detal_info.StatGr(self)
        self.info_hum = detal_info.StatGr(self)
        self.info_gsm = detal_info.StatGr(self)
        self.info_txb = detal_info.StatGr(self)
        self.info_rxb = detal_info.StatGr(self)

        self.info_bat.yText = 'BATTERY'
        self.info_tem.yText = 'TEMPERATURE'
        self.info_hum.yText = 'HUMIDITY'
        self.info_gsm.yText = 'dbm'

        self.serverThread = Thread4Server()
        # self.acceptThread = Thread4Accept()
        self.speakThread = []

        self.detal_info_sensor_1.label_number.setText('1')
        self.detal_info_sensor_2.label_number.setText('2')
        self.detal_info_sensor_3.label_number.setText('3')
        self.detal_info_sensor_4.label_number.setText('4')
        self.detal_info_sensor_5.label_number.setText('5')
        self.detal_info_sensor_6.label_number.setText('6')
        self.detal_info_sensor_7.label_number.setText('7')
        self.detal_info_sensor_8.label_number.setText('8')
        self.detal_info_sensor_9.label_number.setText('9')
        self.detal_info_sensor_10.label_number.setText('10')

        self.timeData = []
        self.past_point_temp_1 = []
        self.past_point_humi_1 = []
        self.past_point_temp_2 = []
        self.past_point_humi_2 = []
        self.past_point_temp_3 = []
        self.past_point_humi_3 = []
        self.past_point_temp_4 = []
        self.past_point_humi_4 = []
        self.past_point_temp_5 = []
        self.past_point_humi_5 = []
        self.past_point_temp_6 = []
        self.past_point_humi_6 = []
        self.past_point_temp_7 = []
        self.past_point_humi_7 = []
        self.past_point_temp_8 = []
        self.past_point_humi_8 = []
        self.past_point_temp_9 = []
        self.past_point_humi_9 = []
        self.past_point_temp_10 = []
        self.past_point_humi_10 = []

        self.slave_hum = []
        self.slave_tem = []
        self.slave_err = []
        self.slave_dat = []
        self.slave_tim = []

        self.flag_auto_scroll = 1
        self.flag_show_log = 1

        self.counter_tx = 0
        self.counter_rx = 0
        self.id = 0

        self.VYear = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.NYear = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        self.version = 'LONG-TERM TEST version 1.5 '

        self.tx_text_bytes = ''
        self.rx_text_bytes = ''

        self.counter_bat_arc = []
        self.counter_tem_arc = []
        self.counter_hum_arc = []
        self.counter_gsm_arc = []
        self.counter_tx_arc = []
        self.counter_rx_arc = []
        self.counter_time_arc = []

        self.button_listen = QtGui.QPushButton('Listen')
        self.button_listen.setFixedWidth(75)
        self.text_rec = QtGui.QTextEdit()
        self.text_send = QtGui.QTextEdit()
        self.button_send = QtGui.QPushButton('Send')
        self.label_port = QtGui.QLabel('Port')
        self.text_port = QtGui.QLineEdit()
        self.label_ip = QtGui.QLabel('IP')
        self.text_ip = QtGui.QLineEdit(self.my_ip)
        self.label_clients = QtGui.QLabel('Number of active clients: 0')
        self.label_pass = QtGui.QLabel('')

        self.new_time = QtGui.QLineEdit('10')
        self.new_number = QtGui.QLineEdit('*111#')
        self.new_time.setFixedWidth(75)
        self.new_number.setFixedWidth(75)
        self.new_bat = QtGui.QPushButton('Bat: 50%')
        self.new_bat.setFixedWidth(75)

        self.button_temperature_central_point = QtGui.QPushButton('Temp.: 20')
        self.button_temperature_central_point.setFixedWidth(75)
        self.button_humidity_central_point = QtGui.QPushButton('Humi.: 35')
        self.button_humidity_central_point.setFixedWidth(75)
        self.button_gsm_level_central_point = QtGui.QPushButton('dbm: 15')
        self.button_gsm_level_central_point.setFixedWidth(75)

        self.button_counter_tx_bytes = QtGui.QPushButton('Tx: 0 b')
        self.button_counter_tx_bytes.setFixedWidth(75)
        self.button_counter_rx_bytes = QtGui.QPushButton('Rx: 0 b')
        self.button_counter_rx_bytes.setFixedWidth(75)

        self.box_listen = QtGui.QHBoxLayout()
        self.box_listen.addWidget(self.label_ip)
        self.box_listen.addWidget(self.text_ip)
        self.box_listen.addWidget(self.label_port)
        self.box_listen.addWidget(self.text_port)
        self.box_listen.addWidget(self.button_listen)
        self.box_listen.addWidget(self.label_clients)
        self.box_listen.addWidget(self.label_pass, QtCore.Qt.AlignLeft)

        self.box_status_central_point = QtGui.QHBoxLayout()
        self.box_status_central_point.addWidget(self.new_time)
        self.box_status_central_point.addWidget(self.new_number)
        self.box_status_central_point.addWidget(self.new_bat)
        self.box_status_central_point.addWidget(self.button_temperature_central_point)
        self.box_status_central_point.addWidget(self.button_humidity_central_point)
        self.box_status_central_point.addWidget(self.button_gsm_level_central_point)
        self.box_status_central_point.addWidget(self.button_counter_tx_bytes)
        self.box_status_central_point.addWidget(self.button_counter_rx_bytes)

        self.box_send = QtGui.QHBoxLayout()
        self.box_send.addWidget(self.text_send)
        self.box_send.addWidget(self.button_send)

        self.box_data = QtGui.QVBoxLayout()
        self.box_data.addWidget(self.text_rec)
        self.box_data.addLayout(self.box_send)

        self.box_central = QtGui.QVBoxLayout()
        self.box_central.addLayout(self.box_data)

        self.box_head_status = QtGui.QHBoxLayout()
        self.box_head_status.addLayout(self.box_listen, QtCore.Qt.AlignLeft)
        self.box_head_status.addLayout(self.box_status_central_point, QtCore.Qt.AlignRight)

        self.label_sensor = QtGui.QLabel('', self)
        self.label_sensor.setFixedSize(600, 635)

        self.im = QtGui.QPixmap(600, 635)
        self.im.fill(QtGui.QColor('#005092'))
        self.label_sensor.setPixmap(self.im)

        self.draw_sensor()

        self.box_label_sensor = QtGui.QHBoxLayout()
        self.box_label_sensor.addWidget(self.label_sensor)

        self.group_label_sensor = QtGui.QGroupBox()
        self.group_label_sensor.setLayout(self.box_label_sensor)

        self.auto_scroll = QtGui.QCheckBox('Auto Scroll Log')
        self.show_log = QtGui.QCheckBox('Show Log')
        self.clean_log = QtGui.QPushButton('Clean Log')
        self.log_output = QtGui.QTextEdit()

        self.auto_scroll.setChecked(True)
        self.show_log.setChecked(True)

        horz_log = QtGui.QHBoxLayout()
        horz_log.addWidget(self.auto_scroll)
        horz_log.addWidget(self.show_log)
        horz_log.addWidget(self.clean_log)

        vert_log_calib = QtGui.QVBoxLayout()
        vert_log_calib.addLayout(horz_log)
        vert_log_calib.addWidget(self.log_output)

        group_log = QtGui.QGroupBox()
        group_log.setLayout(vert_log_calib)

        self.box_central_graph = QtGui.QHBoxLayout()
        self.box_central_graph.addWidget(group_log)
        self.box_central_graph.addLayout(self.box_central)
        self.box_central_graph.addWidget(self.group_label_sensor)

        self.box_central_graph_vert = QtGui.QVBoxLayout()
        self.box_central_graph_vert.addLayout(self.box_head_status)
        self.box_central_graph_vert.addLayout(self.box_central_graph)

        self.group_central = QtGui.QGroupBox()
        self.group_central.setLayout(self.box_central_graph_vert)

        self.setWindowTitle(self.version)
        self.setCentralWidget(self.group_central)

        self.connect(self.detal_info_sensor_1.cal, QtCore.SIGNAL('selectionChanged()'), self.show_1_DataFrom)
        self.connect(self.detal_info_sensor_1.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_1_DataTo)
        self.connect(self.detal_info_sensor_2.cal, QtCore.SIGNAL('selectionChanged()'), self.show_2_DataFrom)
        self.connect(self.detal_info_sensor_2.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_2_DataTo)
        self.connect(self.detal_info_sensor_3.cal, QtCore.SIGNAL('selectionChanged()'), self.show_3_DataFrom)
        self.connect(self.detal_info_sensor_3.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_3_DataTo)
        self.connect(self.detal_info_sensor_4.cal, QtCore.SIGNAL('selectionChanged()'), self.show_4_DataFrom)
        self.connect(self.detal_info_sensor_4.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_4_DataTo)
        self.connect(self.detal_info_sensor_5.cal, QtCore.SIGNAL('selectionChanged()'), self.show_5_DataFrom)
        self.connect(self.detal_info_sensor_5.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_5_DataTo)
        self.connect(self.detal_info_sensor_6.cal, QtCore.SIGNAL('selectionChanged()'), self.show_6_DataFrom)
        self.connect(self.detal_info_sensor_6.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_6_DataTo)
        self.connect(self.detal_info_sensor_7.cal, QtCore.SIGNAL('selectionChanged()'), self.show_7_DataFrom)
        self.connect(self.detal_info_sensor_7.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_7_DataTo)
        self.connect(self.detal_info_sensor_8.cal, QtCore.SIGNAL('selectionChanged()'), self.show_8_DataFrom)
        self.connect(self.detal_info_sensor_8.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_8_DataTo)
        self.connect(self.detal_info_sensor_9.cal, QtCore.SIGNAL('selectionChanged()'), self.show_9_DataFrom)
        self.connect(self.detal_info_sensor_9.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_9_DataTo)
        self.connect(self.detal_info_sensor_10.cal, QtCore.SIGNAL('selectionChanged()'), self.show_10_DataFrom)
        self.connect(self.detal_info_sensor_10.cal2, QtCore.SIGNAL('selectionChanged()'), self.show_10_DataTo)

        self.connect(self.clean_log, QtCore.SIGNAL("clicked()"), self.func_clean_log)
        self.connect(self.auto_scroll, QtCore.SIGNAL("clicked()"), self.func_auto_scroll)
        self.connect(self.show_log, QtCore.SIGNAL("clicked()"), self.func_show_log)

        self.connect(self.button_listen, QtCore.SIGNAL('clicked()'), self.func_listen)
        self.connect(self.button_send, QtCore.SIGNAL('clicked()'), self.func_send)
        # self.connect(self.acceptThread, QtCore.SIGNAL("newAccept(QString)"),
        #              self.func_connect, QtCore.Qt.QueuedConnection)
        self.connect(self.serverThread, QtCore.SIGNAL("rec(QString)"),
                     self.func_rec, QtCore.Qt.QueuedConnection)
        self.connect(self.serverThread, QtCore.SIGNAL("label_clients(QString)"),
                     self.func_label_client, QtCore.Qt.QueuedConnection)

        self.connect(self.new_bat, QtCore.SIGNAL('clicked()'), self.bat_info)
        self.connect(self.button_temperature_central_point, QtCore.SIGNAL('clicked()'), self.tep_info)
        self.connect(self.button_humidity_central_point, QtCore.SIGNAL('clicked()'), self.hum_info)
        self.connect(self.button_gsm_level_central_point, QtCore.SIGNAL('clicked()'), self.gsm_info)
        self.connect(self.button_counter_tx_bytes, QtCore.SIGNAL('clicked()'), self.txb_info)
        self.connect(self.button_counter_rx_bytes, QtCore.SIGNAL('clicked()'), self.rxb_info)

        var = '  Hello :)'
        self.func_write_log(var)
        self.func_write_log('  ' + self.version)

        self.sensor_label_1 = QtGui.QLabel('', self)
        # self.sensor_label_1.setStyleSheet(labelStyle_3)
        self.sensor_label_2 = QtGui.QLabel('', self)
        # self.sensor_label_2.setStyleSheet(labelStyle_3)
        self.sensor_label_3 = QtGui.QLabel('', self)
        # self.sensor_label_3.setStyleSheet(labelStyle_3)
        self.sensor_label_4 = QtGui.QLabel('', self)
        # self.sensor_label_4.setStyleSheet(labelStyle_3)
        self.sensor_label_5 = QtGui.QLabel('', self)
        # self.sensor_label_5.setStyleSheet(labelStyle_3)
        self.sensor_label_6 = QtGui.QLabel('', self)
        # self.sensor_label_6.setStyleSheet(labelStyle_3)
        self.sensor_label_7 = QtGui.QLabel('', self)
        # self.sensor_label_7.setStyleSheet(labelStyle_3)
        self.sensor_label_8 = QtGui.QLabel('', self)
        # self.sensor_label_8.setStyleSheet(labelStyle_3)
        self.sensor_label_9 = QtGui.QLabel('', self)
        # self.sensor_label_9.setStyleSheet(labelStyle_3)
        self.sensor_label_10 = QtGui.QLabel('', self)
        # self.sensor_label_10.setStyleSheet(labelStyle_3)

        self.showMaximized()

        self.adaptiveCoordinateLabelSensor.self_main = self
        self.adaptiveCoordinateLabelSensor.flag_run = 1
        self.adaptiveCoordinateLabelSensor.start()

        self.sensor_label_1.mouseReleaseEvent = left_click_release(self.sensor_label_1.mouseReleaseEvent, self.sensor_label_1)
        self.sensor_label_2.mouseReleaseEvent = left_click_release(self.sensor_label_2.mouseReleaseEvent, self.sensor_label_2)
        self.sensor_label_3.mouseReleaseEvent = left_click_release(self.sensor_label_3.mouseReleaseEvent, self.sensor_label_3)
        self.sensor_label_4.mouseReleaseEvent = left_click_release(self.sensor_label_4.mouseReleaseEvent, self.sensor_label_4)
        self.sensor_label_5.mouseReleaseEvent = left_click_release(self.sensor_label_5.mouseReleaseEvent, self.sensor_label_5)
        self.sensor_label_6.mouseReleaseEvent = left_click_release(self.sensor_label_6.mouseReleaseEvent, self.sensor_label_6)
        self.sensor_label_7.mouseReleaseEvent = left_click_release(self.sensor_label_7.mouseReleaseEvent, self.sensor_label_7)
        self.sensor_label_8.mouseReleaseEvent = left_click_release(self.sensor_label_8.mouseReleaseEvent, self.sensor_label_8)
        self.sensor_label_9.mouseReleaseEvent = left_click_release(self.sensor_label_9.mouseReleaseEvent, self.sensor_label_9)
        self.sensor_label_10.mouseReleaseEvent = left_click_release(self.sensor_label_10.mouseReleaseEvent, self.sensor_label_10)

        self.connect(self.sensor_label_1, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_1_left_clicked)
        self.connect(self.sensor_label_2, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_2_left_clicked)
        self.connect(self.sensor_label_3, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_3_left_clicked)
        self.connect(self.sensor_label_4, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_4_left_clicked)
        self.connect(self.sensor_label_5, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_5_left_clicked)
        self.connect(self.sensor_label_6, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_6_left_clicked)
        self.connect(self.sensor_label_7, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_7_left_clicked)
        self.connect(self.sensor_label_8, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_8_left_clicked)
        self.connect(self.sensor_label_9, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_9_left_clicked)
        self.connect(self.sensor_label_10, QtCore.SIGNAL('leftClickedRelease()'), self.sensor_label_10_left_clicked)

    def func_label_client(self, temp):
        self.label_clients.setText(temp)

    def draw_sensor(self):
        painter = QtGui.QPainter()
        painter.begin(self.label_sensor.pixmap())

        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(575, 20, 515, 20)
        painter.drawLine(515, 580, 515, 20)
        painter.drawLine(575, 580, 575, 20)
        painter.drawArc(515, 550, 60, 60, 180 * 16, 180 * 16)

        pen = QtGui.QPen(QtGui.QColor('#bbb7b7'), 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.fillRect(513, 50, 64, 25, QtGui.QColor('#bbb7b7'))   # 75   OK
        painter.fillRect(513, 105, 64, 25, QtGui.QColor('#bbb7b7'))  # 130  OK
        painter.fillRect(513, 160, 64, 25, QtGui.QColor('#bbb7b7'))  # 185  OK
        painter.fillRect(513, 215, 64, 25, QtGui.QColor('#bbb7b7'))  # 240  OK
        painter.fillRect(513, 270, 64, 25, QtGui.QColor('#bbb7b7'))  # 295  OK
        painter.fillRect(513, 325, 64, 25, QtGui.QColor('#bbb7b7'))  # 350
        painter.fillRect(513, 380, 64, 25, QtGui.QColor('#bbb7b7'))  # 405
        painter.fillRect(513, 435, 64, 25, QtGui.QColor('#bbb7b7'))  # 460
        painter.fillRect(513, 490, 64, 25, QtGui.QColor('#bbb7b7'))  # 515
        painter.fillRect(513, 545, 64, 25, QtGui.QColor('#bbb7b7'))  # 570

        painter.fillRect(550, 55, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 55, 5, 5, QtGui.QColor('red'))  # 130  OK
        painter.fillRect(570, 55, 5, 5, QtGui.QColor('green'))  # 185  OK

        painter.fillRect(550, 110, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 110, 5, 5, QtGui.QColor('red'))  # 130  OK
        painter.fillRect(570, 110, 5, 5, QtGui.QColor('green'))  # 185  OK

        painter.fillRect(550, 165, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 165, 5, 5, QtGui.QColor('red'))  # 130  OK
        painter.fillRect(570, 165, 5, 5, QtGui.QColor('green'))  # 185  OK

        painter.fillRect(550, 220, 5, 5, QtGui.QColor('green'))   # 75   OK
        painter.fillRect(560, 220, 5, 5, QtGui.QColor('black'))  # 130  OK
        painter.fillRect(570, 220, 5, 5, QtGui.QColor('black'))  # 185  OK

        painter.fillRect(550, 275, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 275, 5, 5, QtGui.QColor('green'))  # 130  OK
        painter.fillRect(570, 275, 5, 5, QtGui.QColor('black'))  # 185  OK

        painter.fillRect(550, 330, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 330, 5, 5, QtGui.QColor('red'))  # 130  OK
        painter.fillRect(570, 330, 5, 5, QtGui.QColor('green'))  # 185  OK

        painter.fillRect(550, 385, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 385, 5, 5, QtGui.QColor('red'))  # 130  OK
        painter.fillRect(570, 385, 5, 5, QtGui.QColor('green'))  # 185  OK

        painter.fillRect(550, 440, 5, 5, QtGui.QColor('green'))   # 75   OK
        painter.fillRect(560, 440, 5, 5, QtGui.QColor('black'))  # 130  OK
        painter.fillRect(570, 440, 5, 5, QtGui.QColor('black'))  # 185  OK

        painter.fillRect(550, 495, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 495, 5, 5, QtGui.QColor('green'))  # 130  OK
        painter.fillRect(570, 495, 5, 5, QtGui.QColor('black'))  # 185  OK

        painter.fillRect(550, 550, 5, 5, QtGui.QColor('red'))   # 75   OK
        painter.fillRect(560, 550, 5, 5, QtGui.QColor('red'))  # 130  OK
        painter.fillRect(570, 550, 5, 5, QtGui.QColor('red'))  # 185  OK

        pen = QtGui.QPen(QtGui.QColor('white'), 2, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(20, 23, 20, 72)
        painter.drawLine(20, 72, 505, 72)

        painter.drawLine(20, 78, 20, 127)
        painter.drawLine(20, 127, 505, 127)

        painter.drawLine(20, 133, 20, 182)
        painter.drawLine(20, 182, 505, 182)

        painter.drawLine(20, 188, 20, 237)
        painter.drawLine(20, 237, 505, 237)

        painter.drawLine(20, 243, 20, 292)
        painter.drawLine(20, 292, 505, 292)

        painter.drawLine(20, 298, 20, 347)
        painter.drawLine(20, 347, 505, 347)

        painter.drawLine(20, 353, 20, 402)
        painter.drawLine(20, 402, 505, 402)

        painter.drawLine(20, 408, 20, 457)
        painter.drawLine(20, 457, 505, 457)

        painter.drawLine(20, 463, 20, 512)
        painter.drawLine(20, 512, 505, 512)

        painter.drawLine(20, 518, 20, 567)
        painter.drawLine(20, 567, 505, 567)

        pen = QtGui.QPen(QtGui.QColor('grey'), 1, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(20, 47, 505, 47)
        painter.drawLine(20, 102, 505, 102)
        painter.drawLine(20, 157, 505, 157)
        painter.drawLine(20, 212, 505, 212)
        painter.drawLine(20, 267, 505, 267)
        painter.drawLine(20, 322, 505, 322)
        painter.drawLine(20, 377, 505, 377)
        painter.drawLine(20, 432, 505, 432)
        painter.drawLine(20, 487, 505, 487)
        painter.drawLine(20, 542, 505, 542)

        self.label_sensor.update()

    def draw_error_slave(self, number, status):
        painter = QtGui.QPainter()
        painter.begin(self.label_sensor.pixmap())

        if number == 1:
            if status == 0:
                painter.fillRect(550, 55, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 55, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 55, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 55, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 55, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 55, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 55, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 55, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 55, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 55, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 55, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 55, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 2:
            if status == 0:
                painter.fillRect(550, 110, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 110, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 110, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 110, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 110, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 110, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 110, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 110, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 110, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 110, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 110, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 110, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 3:
            if status == 0:
                painter.fillRect(550, 165, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 165, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 165, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 165, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 165, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 165, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 165, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 165, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 165, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 165, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 165, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 165, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 4:
            if status == 0:
                painter.fillRect(550, 220, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 220, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 220, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 220, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 220, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 220, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 220, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 220, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 220, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 220, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 220, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 220, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 5:
            if status == 0:
                painter.fillRect(550, 275, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 275, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 275, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 275, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 275, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 275, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 275, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 275, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 275, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 275, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 275, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 275, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 6:
            if status == 0:
                painter.fillRect(550, 330, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 330, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 330, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 330, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 330, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 330, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 330, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 330, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 330, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 330, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 330, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 330, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 7:
            if status == 0:
                painter.fillRect(550, 385, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 385, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 385, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 385, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 385, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 385, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 385, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 385, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 385, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 385, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 385, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 385, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 8:
            if status == 0:
                painter.fillRect(550, 440, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 440, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 440, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 440, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 440, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 440, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 440, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 440, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 440, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 440, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 440, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 440, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 9:
            if status == 0:
                painter.fillRect(550, 495, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 495, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 495, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 495, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 495, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 495, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 495, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 495, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 495, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 495, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 495, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 495, 5, 5, QtGui.QColor('red'))  # 185  OK
        elif number == 10:
            if status == 0:
                painter.fillRect(550, 550, 5, 5, QtGui.QColor('green'))   # 75   OK
                painter.fillRect(560, 550, 5, 5, QtGui.QColor('black'))  # 130  OK
                painter.fillRect(570, 550, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 1:
                painter.fillRect(550, 550, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 550, 5, 5, QtGui.QColor('green'))  # 130  OK
                painter.fillRect(570, 550, 5, 5, QtGui.QColor('black'))  # 185  OK
            elif status == 2:
                painter.fillRect(550, 550, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 550, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 550, 5, 5, QtGui.QColor('green'))  # 185  OK
            elif status >= 3:
                painter.fillRect(550, 550, 5, 5, QtGui.QColor('red'))   # 75   OK
                painter.fillRect(560, 550, 5, 5, QtGui.QColor('red'))  # 130  OK
                painter.fillRect(570, 550, 5, 5, QtGui.QColor('red'))  # 185  OK

        self.label_sensor.update()

    def draw_symbol_graph_slave(self, data):
        time_clear = str(datetime.now()).split(' ')[0]
        if time_clear != self.time_clear_point:
            self.time_clear_point = time_clear
            self.im.fill(QtGui.QColor('#005092'))
            self.label_sensor.setPixmap(self.im)
            self.draw_sensor()

        HumiCoef = 49 / 100
        TempCoef = 49 / 100
        TimeCoef = 485 / 1440

        self.timeData.append(data[3])

        self.past_point_humi_1.append(float(data[7].split(':')[1].split(',')[0]))
        self.past_point_temp_1.append(float(data[7].split(':')[1].split(',')[1]))
        self.past_point_humi_2.append(float(data[8].split(':')[1].split(',')[0]))
        self.past_point_temp_2.append(float(data[8].split(':')[1].split(',')[1]))
        self.past_point_humi_3.append(float(data[9].split(':')[1].split(',')[0]))
        self.past_point_temp_3.append(float(data[9].split(':')[1].split(',')[1]))
        self.past_point_humi_4.append(float(data[10].split(':')[1].split(',')[0]))
        self.past_point_temp_4.append(float(data[10].split(':')[1].split(',')[1]))
        self.past_point_humi_5.append(float(data[11].split(':')[1].split(',')[0]))
        self.past_point_temp_5.append(float(data[11].split(':')[1].split(',')[1]))
        self.past_point_humi_6.append(float(data[12].split(':')[1].split(',')[0]))
        self.past_point_temp_6.append(float(data[12].split(':')[1].split(',')[1]))
        self.past_point_humi_7.append(float(data[13].split(':')[1].split(',')[0]))
        self.past_point_temp_7.append(float(data[13].split(':')[1].split(',')[1]))
        self.past_point_humi_8.append(float(data[14].split(':')[1].split(',')[0]))
        self.past_point_temp_8.append(float(data[14].split(':')[1].split(',')[1]))
        self.past_point_humi_9.append(float(data[15].split(':')[1].split(',')[0]))
        self.past_point_temp_9.append(float(data[15].split(':')[1].split(',')[1]))
        self.past_point_humi_10.append(float(data[16].split(':')[1].split(',')[0]))
        self.past_point_temp_10.append(float(data[16].split(':')[1].split(',')[1]))

        if len(self.timeData) > 1:
            XPosition4_1_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_1_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if (self.past_point_humi_1[len(self.past_point_humi_1) - 2] > 0) and (self.past_point_humi_1[len(self.past_point_humi_1) - 2] < 100):
                YPosition4_1_HumiLast = (self.past_point_humi_1[len(self.past_point_humi_1) - 2]) * HumiCoef
            elif self.past_point_humi_1[len(self.past_point_humi_1) - 2] > 100:
                YPosition4_1_HumiLast = 100 * HumiCoef
            else:
                YPosition4_1_HumiLast = 0 * HumiCoef
            if self.past_point_humi_1[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_1_HumiNew = (self.past_point_humi_1[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_1_HumiNew = 0 * HumiCoef
            if self.past_point_temp_1[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_1_TempLast = ((self.past_point_temp_1[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_1_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_1[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_1_TempNew = ((self.past_point_temp_1[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_1_TempNew = (0 * TempCoef) + 25

            XPosition4_2_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_2_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_2[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_2_HumiLast = (self.past_point_humi_2[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_2_HumiLast = 0 * HumiCoef
            if self.past_point_humi_2[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_2_HumiNew = (self.past_point_humi_2[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_2_HumiNew = 0 * HumiCoef
            if self.past_point_temp_2[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_2_TempLast = ((self.past_point_temp_2[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_2_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_2[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_2_TempNew = ((self.past_point_temp_2[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_2_TempNew = (0 * TempCoef) + 25

            XPosition4_3_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_3_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_3[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_3_HumiLast = (self.past_point_humi_3[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_3_HumiLast = 0 * HumiCoef
            if self.past_point_humi_3[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_3_HumiNew = (self.past_point_humi_3[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_3_HumiNew = 0 * HumiCoef
            if self.past_point_temp_3[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_3_TempLast = ((self.past_point_temp_3[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_3_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_3[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_3_TempNew = ((self.past_point_temp_3[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_3_TempNew = (0 * TempCoef) + 25

            XPosition4_4_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_4_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_4[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_4_HumiLast = (self.past_point_humi_4[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_4_HumiLast = 0 * HumiCoef
            if self.past_point_humi_4[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_4_HumiNew = (self.past_point_humi_4[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_4_HumiNew = 0 * HumiCoef
            if self.past_point_temp_4[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_4_TempLast = ((self.past_point_temp_4[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_4_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_4[len(self.past_point_temp_4) - 1] > -50:
                YPosition4_4_TempNew = ((self.past_point_temp_4[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_4_TempNew = (0 * TempCoef) + 25

            XPosition4_5_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_5_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_5[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_5_HumiLast = (self.past_point_humi_5[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_5_HumiLast = 0 * HumiCoef
            if self.past_point_humi_5[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_5_HumiNew = (self.past_point_humi_5[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_5_HumiNew = 0 * HumiCoef
            if self.past_point_temp_5[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_5_TempLast = ((self.past_point_temp_5[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_5_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_5[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_5_TempNew = ((self.past_point_temp_5[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_5_TempNew = (0 * TempCoef) + 25

            XPosition4_6_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_6_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_6[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_6_HumiLast = (self.past_point_humi_6[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_6_HumiLast = 0 * HumiCoef
            if self.past_point_humi_6[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_6_HumiNew = (self.past_point_humi_6[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_6_HumiNew = 0 * HumiCoef
            if self.past_point_temp_6[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_6_TempLast = ((self.past_point_temp_6[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_6_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_6[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_6_TempNew = ((self.past_point_temp_6[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_6_TempNew = (0 * TempCoef) + 25

            XPosition4_7_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_7_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_7[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_7_HumiLast = (self.past_point_humi_7[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_7_HumiLast = 0 * HumiCoef
            if self.past_point_humi_7[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_7_HumiNew = (self.past_point_humi_7[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_7_HumiNew = 0 * HumiCoef
            if self.past_point_temp_7[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_7_TempLast = ((self.past_point_temp_7[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_7_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_7[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_7_TempNew = ((self.past_point_temp_7[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_7_TempNew = (0 * TempCoef) + 25

            XPosition4_8_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_8_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_8[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_8_HumiLast = (self.past_point_humi_8[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_8_HumiLast = 0 * HumiCoef
            if self.past_point_humi_8[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_8_HumiNew = (self.past_point_humi_8[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_8_HumiNew = 0 * HumiCoef
            if self.past_point_temp_8[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_8_TempLast = ((self.past_point_temp_8[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_8_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_8[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_8_TempNew = ((self.past_point_temp_8[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_8_TempNew = (0 * TempCoef) + 25

            XPosition4_9_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_9_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_9[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_9_HumiLast = (self.past_point_humi_9[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_9_HumiLast = 0 * HumiCoef
            if self.past_point_humi_9[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_9_HumiNew = (self.past_point_humi_9[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_9_HumiNew = 0 * HumiCoef
            if self.past_point_temp_9[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_9_TempLast = ((self.past_point_temp_9[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_9_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_9[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_9_TempNew = ((self.past_point_temp_9[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_9_TempNew = (0 * TempCoef) + 25

            XPosition4_10_Last = ((int(self.timeData[len(self.timeData) - 2].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 2].split(':')[2])) * TimeCoef
            XPosition4_10_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            if self.past_point_humi_10[len(self.past_point_humi_1) - 2] > 0:
                YPosition4_10_HumiLast = (self.past_point_humi_10[len(self.past_point_humi_1) - 2]) * HumiCoef
            else:
                YPosition4_10_HumiLast = 0 * HumiCoef
            if self.past_point_humi_10[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_10_HumiNew = (self.past_point_humi_10[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_10_HumiNew = 0 * HumiCoef
            if self.past_point_temp_10[len(self.past_point_temp_1) - 2] > -50:
                YPosition4_10_TempLast = ((self.past_point_temp_10[len(self.past_point_temp_1) - 2]) * TempCoef) + 25
            else:
                YPosition4_10_TempLast = (0 * TempCoef) + 25
            if self.past_point_temp_10[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_10_TempNew = ((self.past_point_temp_10[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_10_TempNew = (0 * TempCoef) + 25
        else:
            XPosition4_1_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_1_Last = XPosition4_1_New - 3
            if self.past_point_humi_1[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_1_HumiNew = (self.past_point_humi_1[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_1_HumiNew = 0 * HumiCoef
            if self.past_point_temp_1[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_1_TempNew = ((self.past_point_temp_1[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_1_TempNew = (0 * TempCoef) + 25
            YPosition4_1_HumiLast = YPosition4_1_HumiNew
            YPosition4_1_TempLast = YPosition4_1_TempNew

            XPosition4_2_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_2_Last = XPosition4_2_New - 3
            if self.past_point_humi_2[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_2_HumiNew = (self.past_point_humi_2[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_2_HumiNew = 0 * HumiCoef
            if self.past_point_temp_2[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_2_TempNew = ((self.past_point_temp_2[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_2_TempNew = (0 * TempCoef) + 25
            YPosition4_2_HumiLast = YPosition4_2_HumiNew
            YPosition4_2_TempLast = YPosition4_2_TempNew

            XPosition4_3_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_3_Last = XPosition4_3_New - 3
            if self.past_point_humi_3[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_3_HumiNew = (self.past_point_humi_3[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_3_HumiNew = 0 * HumiCoef
            if self.past_point_temp_3[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_3_TempNew = ((self.past_point_temp_3[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_3_TempNew = (0 * TempCoef) + 25
            YPosition4_3_HumiLast = YPosition4_3_HumiNew
            YPosition4_3_TempLast = YPosition4_3_TempNew

            XPosition4_4_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_4_Last = XPosition4_4_New - 3
            if self.past_point_humi_4[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_4_HumiNew = (self.past_point_humi_4[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_4_HumiNew = 0 * HumiCoef
            if self.past_point_temp_4[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_4_TempNew = ((self.past_point_temp_4[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_4_TempNew = (0 * TempCoef) + 25
            YPosition4_4_HumiLast = YPosition4_4_HumiNew
            YPosition4_4_TempLast = YPosition4_4_TempNew

            XPosition4_5_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_5_Last = XPosition4_5_New - 3
            if self.past_point_humi_5[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_5_HumiNew = (self.past_point_humi_5[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_5_HumiNew = 0 * HumiCoef
            if self.past_point_temp_5[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_5_TempNew = ((self.past_point_temp_5[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_5_TempNew = (0 * TempCoef) + 25
            YPosition4_5_HumiLast = YPosition4_5_HumiNew
            YPosition4_5_TempLast = YPosition4_5_TempNew

            XPosition4_6_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_6_Last = XPosition4_6_New - 3
            if self.past_point_humi_6[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_6_HumiNew = (self.past_point_humi_6[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_6_HumiNew = 0 * HumiCoef
            if self.past_point_temp_6[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_6_TempNew = ((self.past_point_temp_6[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_6_TempNew = (0 * TempCoef) + 25
            YPosition4_6_HumiLast = YPosition4_6_HumiNew
            YPosition4_6_TempLast = YPosition4_6_TempNew

            XPosition4_7_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_7_Last = XPosition4_7_New - 3
            if self.past_point_humi_7[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_7_HumiNew = (self.past_point_humi_7[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_7_HumiNew = 0 * HumiCoef
            if self.past_point_temp_7[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_7_TempNew = ((self.past_point_temp_7[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_7_TempNew = (0 * TempCoef) + 25
            YPosition4_7_HumiLast = YPosition4_7_HumiNew
            YPosition4_7_TempLast = YPosition4_7_TempNew

            XPosition4_8_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_8_Last = XPosition4_8_New - 3
            if self.past_point_humi_8[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_8_HumiNew = (self.past_point_humi_8[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_8_HumiNew = 0 * HumiCoef
            if self.past_point_temp_8[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_8_TempNew = ((self.past_point_temp_8[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_8_TempNew = (0 * TempCoef) + 25
            YPosition4_8_HumiLast = YPosition4_8_HumiNew
            YPosition4_8_TempLast = YPosition4_8_TempNew

            XPosition4_9_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_9_Last = XPosition4_9_New - 3
            if self.past_point_humi_9[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_9_HumiNew = (self.past_point_humi_9[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_9_HumiNew = 0 * HumiCoef
            if self.past_point_temp_9[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_9_TempNew = ((self.past_point_temp_9[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_9_TempNew = (0 * TempCoef) + 25
            YPosition4_9_HumiLast = YPosition4_9_HumiNew
            YPosition4_9_TempLast = YPosition4_9_TempNew

            XPosition4_10_New = ((int(self.timeData[len(self.timeData) - 1].split(':')[1]) * 60) + int(self.timeData[len(self.timeData) - 1].split(':')[2])) * TimeCoef
            XPosition4_10_Last = XPosition4_10_New - 3
            if self.past_point_humi_10[len(self.past_point_humi_1) - 1] > 0:
                YPosition4_10_HumiNew = (self.past_point_humi_10[len(self.past_point_humi_1) - 1]) * HumiCoef
            else:
                YPosition4_10_HumiNew = 0 * HumiCoef
            if self.past_point_temp_10[len(self.past_point_temp_1) - 1] > -50:
                YPosition4_10_TempNew = ((self.past_point_temp_10[len(self.past_point_temp_1) - 1]) * TempCoef) + 25
            else:
                YPosition4_10_TempNew = (0 * TempCoef) + 25
            YPosition4_10_HumiLast = YPosition4_10_HumiNew
            YPosition4_10_TempLast = YPosition4_10_TempNew

        painter = QtGui.QPainter()
        painter.begin(self.label_sensor.pixmap())

        pen = QtGui.QPen(QtCore.Qt.yellow, 2, QtCore.Qt.SolidLine)  # for temp
        painter.setPen(pen)
        painter.drawLine(XPosition4_1_Last + 20, 72 - YPosition4_1_HumiLast, XPosition4_1_New + 20, 72 - YPosition4_1_HumiNew)
        painter.drawLine(XPosition4_2_Last + 20, 127 - YPosition4_2_HumiLast, XPosition4_2_New + 20, 127 - YPosition4_2_HumiNew)
        painter.drawLine(XPosition4_3_Last + 20, 182 - YPosition4_3_HumiLast, XPosition4_3_New + 20, 182 - YPosition4_3_HumiNew)
        painter.drawLine(XPosition4_4_Last + 20, 237 - YPosition4_4_HumiLast, XPosition4_4_New + 20, 237 - YPosition4_4_HumiNew)
        painter.drawLine(XPosition4_5_Last + 20, 292 - YPosition4_5_HumiLast, XPosition4_5_New + 20, 292 - YPosition4_5_HumiNew)
        painter.drawLine(XPosition4_6_Last + 20, 347 - YPosition4_6_HumiLast, XPosition4_6_New + 20, 347 - YPosition4_6_HumiNew)
        painter.drawLine(XPosition4_7_Last + 20, 402 - YPosition4_7_HumiLast, XPosition4_7_New + 20, 402 - YPosition4_7_HumiNew)
        painter.drawLine(XPosition4_8_Last + 20, 457 - YPosition4_8_HumiLast, XPosition4_8_New + 20, 457 - YPosition4_8_HumiNew)
        painter.drawLine(XPosition4_9_Last + 20, 512 - YPosition4_9_HumiLast, XPosition4_9_New + 20, 512 - YPosition4_9_HumiNew)
        painter.drawLine(XPosition4_10_Last + 20, 567 - YPosition4_10_HumiLast, XPosition4_10_New + 20, 567 - YPosition4_10_HumiNew)

        pen = QtGui.QPen(QtCore.Qt.blue, 2, QtCore.Qt.SolidLine)  # for humid
        painter.setPen(pen)
        painter.drawLine(XPosition4_1_Last + 20, 72 - YPosition4_1_TempLast, XPosition4_1_New + 20, 72 - YPosition4_1_TempNew)
        painter.drawLine(XPosition4_2_Last + 20, 127 - YPosition4_2_TempLast, XPosition4_2_New + 20, 127 - YPosition4_2_TempNew)
        painter.drawLine(XPosition4_3_Last + 20, 182 - YPosition4_3_TempLast, XPosition4_3_New + 20, 182 - YPosition4_3_TempNew)
        painter.drawLine(XPosition4_4_Last + 20, 237 - YPosition4_4_TempLast, XPosition4_4_New + 20, 237 - YPosition4_4_TempNew)
        painter.drawLine(XPosition4_5_Last + 20, 292 - YPosition4_5_TempLast, XPosition4_5_New + 20, 292 - YPosition4_5_TempNew)
        painter.drawLine(XPosition4_6_Last + 20, 347 - YPosition4_6_TempLast, XPosition4_6_New + 20, 347 - YPosition4_6_TempNew)
        painter.drawLine(XPosition4_7_Last + 20, 402 - YPosition4_7_TempLast, XPosition4_7_New + 20, 402 - YPosition4_7_TempNew)
        painter.drawLine(XPosition4_8_Last + 20, 457 - YPosition4_8_TempLast, XPosition4_8_New + 20, 457 - YPosition4_8_TempNew)
        painter.drawLine(XPosition4_9_Last + 20, 512 - YPosition4_9_TempLast, XPosition4_9_New + 20, 512 - YPosition4_9_TempNew)
        painter.drawLine(XPosition4_10_Last + 20, 567 - YPosition4_10_TempLast, XPosition4_10_New + 20, 567 - YPosition4_10_TempNew)

    def func_auto_scroll(self):
        if self.flag_auto_scroll == 1:
            self.flag_auto_scroll = 0
        else:
            self.flag_auto_scroll = 1

    def func_show_log(self):
        if self.flag_show_log == 1:
            self.flag_show_log = 0
        else:
            self.flag_show_log = 1

    def func_clean_log(self):
        self.log_output.clear()

    def func_write_log(self, string):
        print('len(self.log_output.toPlainText())  ' + str(len(self.log_output.toPlainText())))
        if len(self.log_output.toPlainText()) > 20000:
            self.log_output.clear()
            self.text_rec.clear()

        temp = str(datetime.now())
        if self.flag_show_log == 1:
            if 'SEND' in string:
                self.log_output.setTextColor(QtGui.QColor('red'))
            elif 'GET' in string:
                self.log_output.setTextColor(QtGui.QColor('blue'))
            elif 'STORE' in string:
                self.log_output.setTextColor(QtGui.QColor('green'))
            elif '  DEVICE DISCONNECT !!!' in string:
                self.log_output.setTextColor(QtGui.QColor('red'))
            else:
                self.log_output.setTextColor(QtGui.QColor('black'))

            if '  DEVICE DISCONNECT !!!' in string:
                if self.count_disconnect == 0:
                    self.log_output.append('')
                self.log_output.append(temp + string)
                self.count_disconnect += 1
                if self.count_disconnect == 2:
                    self.log_output.append('')
                    self.count_disconnect = 0
            elif 'TURN ON THE DEVICE' in string:
                # self.log_output.append('')
                self.log_output.append(temp + string)
                self.log_output.append('')
            elif 'CONNECT THE WIRE TO THE DEVICE' in string:
                self.log_output.append(temp + string)
                self.log_output.append('')
            else:
                self.log_output.append(temp + string)

        if self.flag_auto_scroll == 1:
            self.log_output.moveCursor(QtGui.QTextCursor.End)

        if 'LONG-TERM_TEST' not in os.listdir('c:\\Users\Public\Documents'):
            # print('NOT')
            os.mkdir('c:\\Users\Public\Documents\LONG-TERM_TEST')
        else:
            pass
            # print('IS')

        name_log_file = 'c:\\Users\Public\Documents\LONG-TERM_TEST\LOG_%s' % temp.split(' ')[0] + '.log'

        try:
            file = open(name_log_file, 'a')
            file.write(temp + string + '\n')
            file.close()
        except:
            file = open(name_log_file, 'w')
            file.write(temp + string + '\n')
            file.close()

    def func_write_data(self, ID, string):
        temp = str(datetime.now())

        if 'LONG-TERM_TEST' not in os.listdir('c:\\Users\Public\Documents'):
            # print('NOT')
            os.mkdir('c:\\Users\Public\Documents\LONG-TERM_TEST')
        else:
            pass
            # print('IS')

        name_log_file = 'c:\\Users\Public\Documents\LONG-TERM_TEST\DATA_%s' % temp.split(' ')[0] + '_' + ID + '.dat'

        try:
            file = open(name_log_file, 'a')
            file.write(string + '\n')
            file.close()
        except:
            file = open(name_log_file, 'w')
            file.write(string + '\n')
            file.close()

    def func_write_error(self, ID, string):
        temp = str(datetime.now())

        if 'LONG-TERM_TEST' not in os.listdir('c:\\Users\Public\Documents'):
            # print('NOT')
            os.mkdir('c:\\Users\Public\Documents\LONG-TERM_TEST')
        else:
            pass
            # print('IS')

        name_log_file = 'c:\\Users\Public\Documents\LONG-TERM_TEST\ERROR_%s' % temp.split(' ')[0] + '_' + str(ID) + '.err'

        try:
            file = open(name_log_file, 'a')
            file.write(string + '\n')
            file.close()
        except:
            file = open(name_log_file, 'w')
            file.write(string + '\n')
            file.close()

    def func_read_log(self, dateFrom, dateTo, slave):
        name_log_file_from = 0
        name_log_file_to = 0
        isDateFrom = 0
        isDateTo = 0

        flag_first_find = 0
        flag_year = 0
        flag_month = 0
        flag_day = 0

        timeDate = []
        humi_1 = []
        temp_1 = []
        humi_2 = []
        temp_2 = []
        humi_3 = []
        temp_3 = []
        humi_4 = []
        temp_4 = []
        humi_5 = []
        temp_5 = []
        humi_6 = []
        temp_6 = []
        humi_7 = []
        temp_7 = []
        humi_8 = []
        temp_8 = []
        humi_9 = []
        temp_9 = []
        humi_10 = []
        temp_10 = []

        if dateFrom.split('_')[1].split('-')[0] == dateTo.split('_')[1].split('-')[0]:
            flag_year = 1  # 2012 - 29
        if dateFrom.split('_')[1].split('-')[1] == dateTo.split('_')[1].split('-')[1]:
            flag_month = 1
        if dateFrom.split('_')[1].split('-')[2] == dateTo.split('_')[1].split('-')[2]:
            flag_day = 1

        list_dirs = os.listdir('c:\\Users\Public\Documents')
        if 'LONG-TERM_TEST' not in list_dirs:
            print('NOT')

        else:
            print('IS')
            list_logs = os.listdir('c:\\Users\Public\Documents\LONG-TERM_TEST')

            if flag_year == 1 and flag_month == 1 and flag_day == 1:
                print('screenplay 1')

                self.ScreenPlay_1(list_logs, dateFrom, name_log_file_from, slave)
                self.detected_archive_slave(slave)

            elif flag_year == 1 and flag_month == 1 and flag_day == 0:
                print('screenplay 2')

                self.ScreenPlay_2(list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave)
                self.detected_archive_slave(slave)

            elif flag_year == 1 and flag_month == 0 and flag_day == 0:
                print('screenplay 3')

                self.ScreenPlay_3(list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave)
                self.detected_archive_slave(slave)

            elif flag_year == 1 and flag_month == 0 and flag_day == 1:
                print('screenplay 4')

                self.ScreenPlay_4(list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave)
                self.detected_archive_slave(slave)


            elif flag_year == 0 and flag_month == 1 and flag_day == 1:
                print('screenplay 5')

                self.ScreenPlay_5(list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave)
                self.detected_archive_slave(slave)

            elif flag_year == 0 and flag_month == 1 and flag_day == 0:
                print('screenplay 6')

                self.ScreenPlay_6(list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave)
                self.detected_archive_slave(slave)

            elif flag_year == 0 and flag_month == 0 and flag_day == 0:
                print('screenplay 7')

                self.ScreenPlay_7(list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave)
                self.detected_archive_slave(slave)

            elif flag_year == 0 and flag_month == 0 and flag_day == 1:
                print('screenplay 8')

                self.ScreenPlay_8(list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave)
                self.detected_archive_slave(slave)

    def ScreenPlay_1(self, list_logs, dateFrom, name_log_file_from, slave):
        for number in range(len(list_logs)):
            print(list_logs[number])
            if '.dat' in list_logs[number]:
                if dateFrom in list_logs[number]:
                    name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

        if name_log_file_from:
            log_data = 0
            try:
                file = open(name_log_file_from, 'r')
            except:
                print('Can\'t read file  ->  ' + name_log_file_from)
            else:
                log_data = file.readlines()
                file.close()
                print(log_data)
                print(len(log_data))

            if log_data:
                self.slave_hum = []
                self.slave_tem = []
                self.slave_err = []
                self.slave_dat = []
                self.slave_tim = []
                for number_data_slave in range(len(log_data)):

                    data_slave = log_data[number_data_slave].split(slave)[1].split('*')[0]
                    self.slave_hum.append(data_slave.split(',')[0])
                    self.slave_tem.append(data_slave.split(',')[1])

        else:
            print('File not found !!!')

    def ScreenPlay_2(self, list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave):
        self.slave_hum = []
        self.slave_tem = []
        self.slave_err = []
        self.slave_dat = []
        self.slave_tim = []

        days = int(dateTo.split('_')[1].split('-')[2]) - int(dateFrom.split('_')[1].split('-')[2])
        if days < 0:
            print('wrong format date !!!')
        else:
            for number in range(len(list_logs)):
                print(list_logs[number])
                if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                    if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                        flag_first_find = 1

                    elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (dateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                        flag_first_find = 1

                    elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                    if name_log_file_from:
                        try:
                            file = open(name_log_file_from, 'r')
                        except:
                            print('Can\'t read file  ->  ' + name_log_file_from)
                            name_log_file_from = 0
                        else:
                            log_data = file.readlines()
                            file.close()
                            print(log_data)
                            name_log_file_from = 0

                        if log_data:

                            for number_data_slave in range(len(log_data)):

                                data_slave = log_data[number_data_slave].split(slave)[1].split('*')[0]
                                self.slave_hum.append(data_slave.split(',')[0])
                                self.slave_tem.append(data_slave.split(',')[1])

                    else:
                        print('File not found !!!')
                        name_log_file_from = 0

    def ScreenPlay_3(self, list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave):
        month = int(dateTo.split('_')[1].split('-')[1]) - int(dateFrom.split('_')[1].split('-')[1])
        if month < 0:
            print('wrong format month !!!')
        else:
            for number_month in range(month + 1):
                temp = (int(dateFrom.split('_')[1].split('-')[0]) - 2012) / 4
                if temp > 0:
                    if dateFrom.split('_')[1].split('-')[1] != dateTo.split('_')[1].split('-')[1]:
                        if temp == int(temp):
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                        else:
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                    else:
                        tempDateTo = dateTo
                        print(dateFrom)
                        print(tempDateTo)

                    for number in range(len(list_logs)):
                        print(list_logs[number])
                        if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                            if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (tempDateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                            if name_log_file_from:
                                try:
                                    file = open(name_log_file_from, 'r')
                                except:
                                    print('Can\'t read file  ->  ' + name_log_file_from)
                                    name_log_file_from = 0
                                else:
                                    log_data = file.readlines()
                                    file.close()
                                    print(log_data)
                                    name_log_file_from = 0
                            else:
                                print('File not found !!!')
                                name_log_file_from = 0

                    # read files

                    temp_month = int(dateFrom.split('_')[1].split('-')[1]) + 1
                    if temp_month < 10:
                        temp_month = '0' + str(temp_month)
                    else:
                        temp_month = str(temp_month)

                    tempDateFrom = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + temp_month + '-' + '01'
                    dateFrom = tempDateFrom

                else:
                    print('Files empty from this year')

            for number in range(len(list_logs)):
                print(list_logs[number])
                if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                    if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                        flag_first_find = 1

                    elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (dateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                        flag_first_find = 1

                    elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                    if name_log_file_from:
                        try:
                            file = open(name_log_file_from, 'r')
                        except:
                            print('Can\'t read file  ->  ' + name_log_file_from)
                            name_log_file_from = 0
                        else:
                            log_data = file.readlines()
                            file.close()
                            print(log_data)
                            name_log_file_from = 0
                    else:
                        print('File not found !!!')
                        name_log_file_from = 0

    def ScreenPlay_4(self, list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave):
        month = int(dateTo.split('_')[1].split('-')[1]) - int(dateFrom.split('_')[1].split('-')[1])
        if month < 0:
            print('wrong format month !!!')
        else:
            for number_month in range(month + 1):
                temp = (int(dateFrom.split('_')[1].split('-')[0]) - 2012) / 4
                if temp > 0:
                    if dateFrom.split('_')[1].split('-')[1] != dateTo.split('_')[1].split('-')[1]:
                        if temp == int(temp):
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                        else:
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                    else:
                        tempDateTo = dateTo
                        print(dateFrom)
                        print(tempDateTo)

                    for number in range(len(list_logs)):
                        print(list_logs[number])
                        if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                            if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (tempDateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                            if name_log_file_from:
                                try:
                                    file = open(name_log_file_from, 'r')
                                except:
                                    print('Can\'t read file  ->  ' + name_log_file_from)
                                    name_log_file_from = 0
                                else:
                                    log_data = file.readlines()
                                    file.close()
                                    print(log_data)
                                    name_log_file_from = 0
                            else:
                                print('File not found !!!')
                                name_log_file_from = 0

                    # read files

                    temp_month = int(dateFrom.split('_')[1].split('-')[1]) + 1
                    if temp_month < 10:
                        temp_month = '0' + str(temp_month)
                    else:
                        temp_month = str(temp_month)

                    tempDateFrom = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + temp_month + '-' + '01'
                    dateFrom = tempDateFrom

                else:
                    print('Files empty from this year')

            for number in range(len(list_logs)):
                print(list_logs[number])
                if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                    if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                        flag_first_find = 1

                    elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (dateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                        flag_first_find = 1

                    elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                        name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                    if name_log_file_from:
                        try:
                            file = open(name_log_file_from, 'r')
                        except:
                            print('Can\'t read file  ->  ' + name_log_file_from)
                            name_log_file_from = 0
                        else:
                            log_data = file.readlines()
                            file.close()
                            print(log_data)
                            name_log_file_from = 0
                    else:
                        print('File not found !!!')
                        name_log_file_from = 0

    def ScreenPlay_5(self, list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave):
        year = int(dateTo.split('_')[1].split('-')[0]) - int(dateFrom.split('_')[1].split('-')[0])
        if year < 0:
            print('wrong format year !!!')
        else:
            count = 12 - int(dateFrom.split('_')[1].split('-')[1])
            count += int(dateTo.split('_')[1].split('-')[1])
            count += 12 * (year - 1)
            print(count)
            for number_month in range(count + 1):
                temp = (int(dateFrom.split('_')[1].split('-')[0]) - 2012) / 4
                if temp > 0:
                    if dateFrom.split('_')[1].split('-')[0] != dateTo.split('_')[1].split('-')[0]:
                        if temp == int(temp):
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                        else:
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                    else:
                        if dateFrom.split('_')[1].split('-')[1] != dateTo.split('_')[1].split('-')[1]:
                            if temp == int(temp):
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)

                            else:
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)
                        else:
                            tempDateTo = dateTo
                            print(dateFrom)
                            print(tempDateTo)

                    for number in range(len(list_logs)):
                        print(list_logs[number])
                        if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                            if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (tempDateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                            if name_log_file_from:
                                try:
                                    file = open(name_log_file_from, 'r')
                                except:
                                    print('Can\'t read file  ->  ' + name_log_file_from)
                                    name_log_file_from = 0
                                else:
                                    log_data = file.readlines()
                                    file.close()
                                    print(log_data)
                                    name_log_file_from = 0
                            else:
                                print('File not found !!!')
                                name_log_file_from = 0

                    # read files

                    if int(dateFrom.split('_')[1].split('-')[1]) + 1 > 12:
                        temp_year = str(int(dateFrom.split('_')[1].split('-')[0]) + 1)
                        temp_month = 1
                    else:
                        temp_year = dateFrom.split('_')[1].split('-')[0]
                        temp_month = int(dateFrom.split('_')[1].split('-')[1]) + 1

                    if temp_month < 10:
                        temp_month = '0' + str(temp_month)
                    else:
                        temp_month = str(temp_month)

                    tempDateFrom = dateFrom.split('_')[0] + '_' + temp_year + '-' + temp_month + '-' + '01'
                    dateFrom = tempDateFrom

                else:
                    print('Files empty from this year')

    def ScreenPlay_6(self, list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave):
        year = int(dateTo.split('_')[1].split('-')[0]) - int(dateFrom.split('_')[1].split('-')[0])
        if year < 0:
            print('wrong format year !!!')
        else:
            count = 12 - int(dateFrom.split('_')[1].split('-')[1])
            count += int(dateTo.split('_')[1].split('-')[1])
            count += 12 * (year - 1)
            print(count)
            for number_month in range(count + 1):
                temp = (int(dateFrom.split('_')[1].split('-')[0]) - 2012) / 4
                if temp > 0:
                    if dateFrom.split('_')[1].split('-')[0] != dateTo.split('_')[1].split('-')[0]:
                        if temp == int(temp):
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                        else:
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                    else:
                        if dateFrom.split('_')[1].split('-')[1] != dateTo.split('_')[1].split('-')[1]:
                            if temp == int(temp):
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)

                            else:
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)
                        else:
                            tempDateTo = dateTo
                            print(dateFrom)
                            print(tempDateTo)

                    for number in range(len(list_logs)):
                        print(list_logs[number])
                        if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                            if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (tempDateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                            if name_log_file_from:
                                try:
                                    file = open(name_log_file_from, 'r')
                                except:
                                    print('Can\'t read file  ->  ' + name_log_file_from)
                                    name_log_file_from = 0
                                else:
                                    log_data = file.readlines()
                                    file.close()
                                    print(log_data)
                                    name_log_file_from = 0
                            else:
                                print('File not found !!!')
                                name_log_file_from = 0

                    # read files

                    if int(dateFrom.split('_')[1].split('-')[1]) + 1 > 12:
                        temp_year = str(int(dateFrom.split('_')[1].split('-')[0]) + 1)
                        temp_month = 1
                    else:
                        temp_year = dateFrom.split('_')[1].split('-')[0]
                        temp_month = int(dateFrom.split('_')[1].split('-')[1]) + 1

                    if temp_month < 10:
                        temp_month = '0' + str(temp_month)
                    else:
                        temp_month = str(temp_month)

                    tempDateFrom = dateFrom.split('_')[0] + '_' + temp_year + '-' + temp_month + '-' + '01'
                    dateFrom = tempDateFrom

                else:
                    print('Files empty from this year')

    def ScreenPlay_7(self, list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave):
        year = int(dateTo.split('_')[1].split('-')[0]) - int(dateFrom.split('_')[1].split('-')[0])
        if year < 0:
            print('wrong format year !!!')
        else:
            count = 12 - int(dateFrom.split('_')[1].split('-')[1])
            count += int(dateTo.split('_')[1].split('-')[1])
            count += 12 * (year - 1)
            print(count)
            for number_month in range(count + 1):
                temp = (int(dateFrom.split('_')[1].split('-')[0]) - 2012) / 4
                if temp > 0:
                    if dateFrom.split('_')[1].split('-')[0] != dateTo.split('_')[1].split('-')[0]:
                        if temp == int(temp):
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                        else:
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                    else:
                        if dateFrom.split('_')[1].split('-')[1] != dateTo.split('_')[1].split('-')[1]:
                            if temp == int(temp):
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)

                            else:
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)
                        else:
                            tempDateTo = dateTo
                            print(dateFrom)
                            print(tempDateTo)

                    for number in range(len(list_logs)):
                        print(list_logs[number])
                        if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                            if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (tempDateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                            if name_log_file_from:
                                try:
                                    file = open(name_log_file_from, 'r')
                                except:
                                    print('Can\'t read file  ->  ' + name_log_file_from)
                                    name_log_file_from = 0
                                else:
                                    log_data = file.readlines()
                                    file.close()
                                    print(log_data)
                                    name_log_file_from = 0
                            else:
                                print('File not found !!!')
                                name_log_file_from = 0

                    # read files

                    if int(dateFrom.split('_')[1].split('-')[1]) + 1 > 12:
                        temp_year = str(int(dateFrom.split('_')[1].split('-')[0]) + 1)
                        temp_month = 1
                    else:
                        temp_year = dateFrom.split('_')[1].split('-')[0]
                        temp_month = int(dateFrom.split('_')[1].split('-')[1]) + 1

                    if temp_month < 10:
                        temp_month = '0' + str(temp_month)
                    else:
                        temp_month = str(temp_month)

                    tempDateFrom = dateFrom.split('_')[0] + '_' + temp_year + '-' + temp_month + '-' + '01'
                    dateFrom = tempDateFrom

                else:
                    print('Files empty from this year')

    def ScreenPlay_8(self, list_logs, dateFrom, dateTo, name_log_file_from, name_log_file_to, slave):
        year = int(dateTo.split('_')[1].split('-')[0]) - int(dateFrom.split('_')[1].split('-')[0])
        if year < 0:
            print('wrong format year !!!')
        else:
            count = 12 - int(dateFrom.split('_')[1].split('-')[1])
            count += int(dateTo.split('_')[1].split('-')[1])
            count += 12 * (year - 1)
            print(count)
            for number_month in range(count + 1):
                temp = (int(dateFrom.split('_')[1].split('-')[0]) - 2012) / 4
                if temp > 0:
                    if dateFrom.split('_')[1].split('-')[0] != dateTo.split('_')[1].split('-')[0]:
                        if temp == int(temp):
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                        else:
                            tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                            print(dateFrom)
                            print(tempDateTo)

                    else:
                        if dateFrom.split('_')[1].split('-')[1] != dateTo.split('_')[1].split('-')[1]:
                            if temp == int(temp):
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.VYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)

                            else:
                                tempDateTo = dateFrom.split('_')[0] + '_' + dateFrom.split('_')[1].split('-')[0] + '-' + dateFrom.split('_')[1].split('-')[1] + '-' + str(self.NYear[int(dateFrom.split('_')[1].split('-')[1]) - 1])
                                print(dateFrom)
                                print(tempDateTo)
                        else:
                            tempDateTo = dateTo
                            print(dateFrom)
                            print(tempDateTo)

                    for number in range(len(list_logs)):
                        print(list_logs[number])
                        if ('.dat' in list_logs[number]) and (dateFrom.split('_')[1].split('-')[0] == list_logs[number].split('_')[1].split('-')[0]) and (dateFrom.split('_')[1].split('-')[1] == list_logs[number].split('_')[1].split('-')[1]):
                            if dateFrom.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif (dateFrom.split('_')[1].split('-')[2] < list_logs[number].split('_')[1].split('-')[2]) and (tempDateTo.split('_')[1].split('-')[2] > list_logs[number].split('_')[1].split('-')[2]):
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]
                                flag_first_find = 1

                            elif dateTo.split('_')[1].split('-')[2] in list_logs[number].split('_')[1].split('-')[2]:
                                name_log_file_from = 'c:\\Users\Public\Documents\LONG-TERM_TEST\\' + list_logs[number]

                            if name_log_file_from:
                                try:
                                    file = open(name_log_file_from, 'r')
                                except:
                                    print('Can\'t read file  ->  ' + name_log_file_from)
                                    name_log_file_from = 0
                                else:
                                    log_data = file.readlines()
                                    file.close()
                                    print(log_data)
                                    name_log_file_from = 0
                            else:
                                print('File not found !!!')
                                name_log_file_from = 0

                    # read files

                    if int(dateFrom.split('_')[1].split('-')[1]) + 1 > 12:
                        temp_year = str(int(dateFrom.split('_')[1].split('-')[0]) + 1)
                        temp_month = 1
                    else:
                        temp_year = dateFrom.split('_')[1].split('-')[0]
                        temp_month = int(dateFrom.split('_')[1].split('-')[1]) + 1

                    if temp_month < 10:
                        temp_month = '0' + str(temp_month)
                    else:
                        temp_month = str(temp_month)

                    tempDateFrom = dateFrom.split('_')[0] + '_' + temp_year + '-' + temp_month + '-' + '01'
                    dateFrom = tempDateFrom

                else:
                    print('Files empty from this year')

    def detected_archive_slave(self, slave):
        if slave == 'D0:':
            self.detal_info_sensor_1.axes_humidity.clear()
            self.detal_info_sensor_1.axes_temperature.clear()

            # self.detal_info_sensor_1.axes_humidity.grid(True)
            self.detal_info_sensor_1.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_1.axes_temperature.grid(True)
            self.detal_info_sensor_1.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_1.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_1.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_1.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_1.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_1.canvas_humidity.draw()
            self.detal_info_sensor_1.canvas_temperature.draw()
        elif slave == 'D1:':
            self.detal_info_sensor_2.axes_humidity.clear()
            self.detal_info_sensor_2.axes_temperature.clear()

            # self.detal_info_sensor_2.axes_humidity.grid(True)
            self.detal_info_sensor_2.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_2.axes_temperature.grid(True)
            self.detal_info_sensor_2.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_2.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_2.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_2.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_2.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_2.canvas_humidity.draw()
            self.detal_info_sensor_2.canvas_temperature.draw()
        elif slave == 'D2:':
            self.detal_info_sensor_3.axes_humidity.clear()
            self.detal_info_sensor_3.axes_temperature.clear()

            # self.detal_info_sensor_3.axes_humidity.grid(True)
            self.detal_info_sensor_3.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_3.axes_temperature.grid(True)
            self.detal_info_sensor_3.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_3.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_3.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_3.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_3.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_3.canvas_humidity.draw()
            self.detal_info_sensor_3.canvas_temperature.draw()
        elif slave == 'D3:':
            self.detal_info_sensor_4.axes_humidity.clear()
            self.detal_info_sensor_4.axes_temperature.clear()

            # self.detal_info_sensor_4.axes_humidity.grid(True)
            self.detal_info_sensor_4.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_4.axes_temperature.grid(True)
            self.detal_info_sensor_4.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_4.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_4.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_4.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_4.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_4.canvas_humidity.draw()
            self.detal_info_sensor_4.canvas_temperature.draw()
        elif slave == 'D4:':
            self.detal_info_sensor_5.axes_humidity.clear()
            self.detal_info_sensor_5.axes_temperature.clear()

            # self.detal_info_sensor_5.axes_humidity.grid(True)
            self.detal_info_sensor_5.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_5.axes_temperature.grid(True)
            self.detal_info_sensor_5.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_5.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_5.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_5.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_5.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_5.canvas_humidity.draw()
            self.detal_info_sensor_5.canvas_temperature.draw()
        elif slave == 'D5:':
            self.detal_info_sensor_6.axes_humidity.clear()
            self.detal_info_sensor_6.axes_temperature.clear()

            # self.detal_info_sensor_6.axes_humidity.grid(True)
            self.detal_info_sensor_6.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_6.axes_temperature.grid(True)
            self.detal_info_sensor_6.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_6.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_6.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_6.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_6.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_6.canvas_humidity.draw()
            self.detal_info_sensor_6.canvas_temperature.draw()
        elif slave == 'D6:':
            self.detal_info_sensor_7.axes_humidity.clear()
            self.detal_info_sensor_7.axes_temperature.clear()

            # self.detal_info_sensor_7.axes_humidity.grid(True)
            self.detal_info_sensor_7.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_7.axes_temperature.grid(True)
            self.detal_info_sensor_7.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_7.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_7.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_7.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_7.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_7.canvas_humidity.draw()
            self.detal_info_sensor_7.canvas_temperature.draw()
        elif slave == 'D7:':
            self.detal_info_sensor_8.axes_humidity.clear()
            self.detal_info_sensor_8.axes_temperature.clear()

            # self.detal_info_sensor_8.axes_humidity.grid(True)
            self.detal_info_sensor_8.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_8.axes_temperature.grid(True)
            self.detal_info_sensor_8.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_8.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_8.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_8.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_8.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_8.canvas_humidity.draw()
            self.detal_info_sensor_8.canvas_temperature.draw()
        elif slave == 'D8:':
            self.detal_info_sensor_9.axes_humidity.clear()
            self.detal_info_sensor_9.axes_temperature.clear()

            # self.detal_info_sensor_9.axes_humidity.grid(True)
            self.detal_info_sensor_9.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_9.axes_temperature.grid(True)
            self.detal_info_sensor_9.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_9.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_9.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_9.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_9.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_9.canvas_humidity.draw()
            self.detal_info_sensor_9.canvas_temperature.draw()
        elif slave == 'D9:':
            self.detal_info_sensor_10.axes_humidity.clear()
            self.detal_info_sensor_10.axes_temperature.clear()

            # self.detal_info_sensor_10.axes_humidity.grid(True)
            self.detal_info_sensor_10.axes_humidity.set_ylabel('Humidity')
            # self.detal_info_sensor_10.axes_temperature.grid(True)
            self.detal_info_sensor_10.axes_temperature.set_ylabel('Temperature')

            self.detal_info_sensor_10.axes_humidity.set_xticks(range(len(self.slave_hum) + 1))
            self.detal_info_sensor_10.axes_temperature.set_xticks(range(len(self.slave_tem) + 1))

            self.detal_info_sensor_10.axes_humidity.plot(self.slave_hum, '#ffd700', linewidth=1)
            self.detal_info_sensor_10.axes_temperature.plot(self.slave_tem, 'black', linewidth=1)
            self.detal_info_sensor_10.canvas_humidity.draw()
            self.detal_info_sensor_10.canvas_temperature.draw()

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

    def parseRx_handlerSlaveError(self, data):
        # print('HandlerSlaveError  ' + data)
        temp_list = data.split('\r\n')
        # print(temp_list)

        self.draw_error_slave(1, int(temp_list[7].split(',')[2]))
        self.draw_error_slave(2, int(temp_list[8].split(',')[2]))
        self.draw_error_slave(3, int(temp_list[9].split(',')[2]))
        self.draw_error_slave(4, int(temp_list[10].split(',')[2]))
        self.draw_error_slave(5, int(temp_list[11].split(',')[2]))
        self.draw_error_slave(6, int(temp_list[12].split(',')[2]))
        self.draw_error_slave(7, int(temp_list[13].split(',')[2]))
        self.draw_error_slave(8, int(temp_list[14].split(',')[2]))
        self.draw_error_slave(9, int(temp_list[15].split(',')[2]))
        self.draw_error_slave(10, int(temp_list[16].split(',')[2]))

        return '200'

    def parseRx_handlerSlaveData(self, data):
        # print('HandlerSlaveData  ' + data)
        temp_list = data.split('\r\n')
        # print(temp_list)

        self.draw_symbol_graph_slave(temp_list)

    def parseRx_ErrPack(self, pack):
        self.button_gsm_level_central_point.setText('GSM: %s' % pack[9] + '%')
        self.new_bat.setText('Bat: %s' % pack[16] + '%')

        try:
            self.counter_bat_arc.append(int(pack[16]))
        except:
            print('BAT array ERROR')

        try:
            self.counter_gsm_arc.append(int(pack[9]))
        except:
            print('GSM array ERROR')

    def parseRx_DatPack(self, pack):
        self.button_humidity_central_point.setText('Humi.: %s' % pack[18].split(',')[0].split(':')[1].split('.')[0])
        self.button_temperature_central_point.setText('Temp.: %s' % pack[18].split(',')[1].split('.')[0])

        self.counter_hum_arc.append(pack[18].split(',')[0].split(':')[1].split('.')[0])
        self.counter_tem_arc.append(pack[18].split(',')[1].split('.')[0])

    def sensor_label_1_left_clicked(self):
        print('sensor_label_1_left_clicked')
        if self.detal_info_sensor_1.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_1.show()
            self.sensor_label_1.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_1.axes_humidity.clear()
        self.detal_info_sensor_1.axes_temperature.clear()

        # self.detal_info_sensor_1.axes_humidity.grid(True)
        self.detal_info_sensor_1.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_1.axes_temperature.grid(True)
        self.detal_info_sensor_1.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_1.axes_humidity.set_xticks(range(len(self.past_point_humi_1) + 1))
        self.detal_info_sensor_1.axes_temperature.set_xticks(range(len(self.past_point_temp_1) + 1))

        self.detal_info_sensor_1.axes_humidity.plot(self.past_point_humi_1, '#ffd700', linewidth=1)
        self.detal_info_sensor_1.axes_temperature.plot(self.past_point_temp_1, 'black', linewidth=1)
        self.detal_info_sensor_1.canvas_humidity.draw()
        self.detal_info_sensor_1.canvas_temperature.draw()

    def sensor_label_2_left_clicked(self):
        print('sensor_label_2_left_clicked')
        if self.detal_info_sensor_2.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_2.show()
            self.sensor_label_2.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_2.axes_humidity.clear()
        self.detal_info_sensor_2.axes_temperature.clear()

        # self.detal_info_sensor_2.axes_humidity.grid(True)
        self.detal_info_sensor_2.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_2.axes_temperature.grid(True)
        self.detal_info_sensor_2.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_2.axes_humidity.set_xticks(range(len(self.past_point_humi_2) + 1))
        self.detal_info_sensor_2.axes_temperature.set_xticks(range(len(self.past_point_temp_2) + 1))

        self.detal_info_sensor_2.axes_humidity.plot(self.past_point_humi_2, '#ffd700', linewidth=1)
        self.detal_info_sensor_2.axes_temperature.plot(self.past_point_temp_2, 'black', linewidth=1)
        self.detal_info_sensor_2.canvas_humidity.draw()
        self.detal_info_sensor_2.canvas_temperature.draw()

    def sensor_label_3_left_clicked(self):
        print('sensor_label_3_left_clicked')
        if self.detal_info_sensor_3.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_3.show()
            self.sensor_label_3.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_3.axes_humidity.clear()
        self.detal_info_sensor_3.axes_temperature.clear()

        # self.detal_info_sensor_3.axes_humidity.grid(True)
        self.detal_info_sensor_3.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_3.axes_temperature.grid(True)
        self.detal_info_sensor_3.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_3.axes_humidity.set_xticks(range(len(self.past_point_humi_3) + 1))
        self.detal_info_sensor_3.axes_temperature.set_xticks(range(len(self.past_point_temp_3) + 1))

        self.detal_info_sensor_3.axes_humidity.plot(self.past_point_humi_3, '#ffd700', linewidth=1)
        self.detal_info_sensor_3.axes_temperature.plot(self.past_point_temp_3, 'black', linewidth=1)
        self.detal_info_sensor_3.canvas_humidity.draw()
        self.detal_info_sensor_3.canvas_temperature.draw()

    def sensor_label_4_left_clicked(self):
        print('sensor_label_4_left_clicked')
        if self.detal_info_sensor_4.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_4.show()
            self.sensor_label_4.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_4.axes_humidity.clear()
        self.detal_info_sensor_4.axes_temperature.clear()

        # self.detal_info_sensor_4.axes_humidity.grid(True)
        self.detal_info_sensor_4.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_4.axes_temperature.grid(True)
        self.detal_info_sensor_4.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_4.axes_humidity.set_xticks(range(len(self.past_point_humi_4) + 1))
        self.detal_info_sensor_4.axes_temperature.set_xticks(range(len(self.past_point_temp_4) + 1))

        self.detal_info_sensor_4.axes_humidity.plot(self.past_point_humi_4, '#ffd700', linewidth=1)
        self.detal_info_sensor_4.axes_temperature.plot(self.past_point_temp_4, 'black', linewidth=1)
        self.detal_info_sensor_4.canvas_humidity.draw()
        self.detal_info_sensor_4.canvas_temperature.draw()

    def sensor_label_5_left_clicked(self):
        print('sensor_label_5_left_clicked')
        if self.detal_info_sensor_5.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_5.show()
            self.sensor_label_5.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_5.axes_humidity.clear()
        self.detal_info_sensor_5.axes_temperature.clear()

        # self.detal_info_sensor_5.axes_humidity.grid(True)
        self.detal_info_sensor_5.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_5.axes_temperature.grid(True)
        self.detal_info_sensor_5.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_5.axes_humidity.set_xticks(range(len(self.past_point_humi_5) + 1))
        self.detal_info_sensor_5.axes_temperature.set_xticks(range(len(self.past_point_temp_5) + 1))

        self.detal_info_sensor_5.axes_humidity.plot(self.past_point_humi_5, '#ffd700', linewidth=1)
        self.detal_info_sensor_5.axes_temperature.plot(self.past_point_temp_5, 'black', linewidth=1)
        self.detal_info_sensor_5.canvas_humidity.draw()
        self.detal_info_sensor_5.canvas_temperature.draw()

    def sensor_label_6_left_clicked(self):
        print('sensor_label_6_left_clicked')
        if self.detal_info_sensor_6.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_6.show()
            self.sensor_label_6.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_6.axes_humidity.clear()
        self.detal_info_sensor_6.axes_temperature.clear()

        # self.detal_info_sensor_6.axes_humidity.grid(True)
        self.detal_info_sensor_6.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_6.axes_temperature.grid(True)
        self.detal_info_sensor_6.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_6.axes_humidity.set_xticks(range(len(self.past_point_humi_6) + 1))
        self.detal_info_sensor_6.axes_temperature.set_xticks(range(len(self.past_point_temp_6) + 1))

        self.detal_info_sensor_6.axes_humidity.plot(self.past_point_humi_6, '#ffd700', linewidth=1)
        self.detal_info_sensor_6.axes_temperature.plot(self.past_point_temp_6, 'black', linewidth=1)
        self.detal_info_sensor_6.canvas_humidity.draw()
        self.detal_info_sensor_6.canvas_temperature.draw()

    def sensor_label_7_left_clicked(self):
        print('sensor_label_7_left_clicked')
        if self.detal_info_sensor_7.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_7.show()
            self.sensor_label_7.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_7.axes_humidity.clear()
        self.detal_info_sensor_7.axes_temperature.clear()

        # self.detal_info_sensor_7.axes_humidity.grid(True)
        self.detal_info_sensor_7.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_7.axes_temperature.grid(True)
        self.detal_info_sensor_7.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_7.axes_humidity.set_xticks(range(len(self.past_point_humi_7) + 1))
        self.detal_info_sensor_7.axes_temperature.set_xticks(range(len(self.past_point_temp_7) + 1))

        self.detal_info_sensor_7.axes_humidity.plot(self.past_point_humi_7, '#ffd700', linewidth=1)
        self.detal_info_sensor_7.axes_temperature.plot(self.past_point_temp_7, 'black', linewidth=1)
        self.detal_info_sensor_7.canvas_humidity.draw()
        self.detal_info_sensor_7.canvas_temperature.draw()

    def sensor_label_8_left_clicked(self):
        print('sensor_label_8_left_clicked')
        if self.detal_info_sensor_8.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_8.show()
            self.sensor_label_8.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_8.axes_humidity.clear()
        self.detal_info_sensor_8.axes_temperature.clear()

        # self.detal_info_sensor_8.axes_humidity.grid(True)
        self.detal_info_sensor_8.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_8.axes_temperature.grid(True)
        self.detal_info_sensor_8.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_8.axes_humidity.set_xticks(range(len(self.past_point_humi_8) + 1))
        self.detal_info_sensor_8.axes_temperature.set_xticks(range(len(self.past_point_temp_8) + 1))

        self.detal_info_sensor_8.axes_humidity.plot(self.past_point_humi_8, '#ffd700', linewidth=1)
        self.detal_info_sensor_8.axes_temperature.plot(self.past_point_temp_8, 'black', linewidth=1)
        self.detal_info_sensor_8.canvas_humidity.draw()
        self.detal_info_sensor_8.canvas_temperature.draw()

    def sensor_label_9_left_clicked(self):
        print('sensor_label_9_left_clicked')
        if self.detal_info_sensor_9.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_9.show()
            self.sensor_label_9.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_9.axes_humidity.clear()
        self.detal_info_sensor_9.axes_temperature.clear()

        # self.detal_info_sensor_9.axes_humidity.grid(True)
        self.detal_info_sensor_9.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_9.axes_temperature.grid(True)
        self.detal_info_sensor_9.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_9.axes_humidity.set_xticks(range(len(self.past_point_humi_9) + 1))
        self.detal_info_sensor_9.axes_temperature.set_xticks(range(len(self.past_point_temp_9) + 1))

        self.detal_info_sensor_9.axes_humidity.plot(self.past_point_humi_9, '#ffd700', linewidth=1)
        self.detal_info_sensor_9.axes_temperature.plot(self.past_point_temp_9, 'black', linewidth=1)
        self.detal_info_sensor_9.canvas_humidity.draw()
        self.detal_info_sensor_9.canvas_temperature.draw()

    def sensor_label_10_left_clicked(self):
        print('sensor_label_10_left_clicked')
        if self.detal_info_sensor_10.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()

            self.detal_info_sensor_10.show()
            self.sensor_label_10.setStyleSheet(labelStyle_3)

        self.detal_info_sensor_10.axes_humidity.clear()
        self.detal_info_sensor_10.axes_temperature.clear()

        # self.detal_info_sensor_10.axes_humidity.grid(True)
        self.detal_info_sensor_10.axes_humidity.set_ylabel('Humidity')
        # self.detal_info_sensor_10.axes_temperature.grid(True)
        self.detal_info_sensor_10.axes_temperature.set_ylabel('Temperature')

        self.detal_info_sensor_10.axes_humidity.set_xticks(range(len(self.past_point_humi_10) + 1))
        self.detal_info_sensor_10.axes_temperature.set_xticks(range(len(self.past_point_temp_10) + 1))

        self.detal_info_sensor_10.axes_humidity.plot(self.past_point_humi_10, '#ffd700', linewidth=1)
        self.detal_info_sensor_10.axes_temperature.plot(self.past_point_temp_10, 'black', linewidth=1)
        self.detal_info_sensor_10.canvas_humidity.draw()
        self.detal_info_sensor_10.canvas_temperature.draw()

    def show_1_DataFrom(self):
        date_from = self.detal_info_sensor_1.cal.selectedDate()
        print('show_1_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_1.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_1.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_1.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_1.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D0:')

    def show_1_DataTo(self):
        date_from = self.detal_info_sensor_1.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_1.cal2.selectedDate()
        print('show_1_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_1.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_1.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_1.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D0:')

    def show_2_DataFrom(self):
        date_from = self.detal_info_sensor_2.cal.selectedDate()
        print('show_2_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_2.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_2.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_2.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_2.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D1:')

    def show_2_DataTo(self):
        date_from = self.detal_info_sensor_2.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_2.cal2.selectedDate()
        print('show_2_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_2.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_2.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_2.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D1:')

    def show_3_DataFrom(self):
        date_from = self.detal_info_sensor_3.cal.selectedDate()
        print('show_3_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_3.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_3.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_3.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_3.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D2:')

    def show_3_DataTo(self):
        date_from = self.detal_info_sensor_3.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_3.cal2.selectedDate()
        print('show_3_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_3.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_3.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_3.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D2:')

    def show_4_DataFrom(self):
        date_from = self.detal_info_sensor_4.cal.selectedDate()
        print('show_4_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_4.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_4.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_4.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_4.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D3:')

    def show_4_DataTo(self):
        date_from = self.detal_info_sensor_4.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_4.cal2.selectedDate()
        print('show_4_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_4.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_4.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_4.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D3:')

    def show_5_DataFrom(self):
        date_from = self.detal_info_sensor_5.cal.selectedDate()
        print('show_5_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_5.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_5.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_5.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_5.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D4:')

    def show_5_DataTo(self):
        date_from = self.detal_info_sensor_5.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_5.cal2.selectedDate()
        print('show_5_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_5.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_5.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_5.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D4:')

    def show_6_DataFrom(self):
        date_from = self.detal_info_sensor_6.cal.selectedDate()
        print('show_6_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_6.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_6.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_6.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_6.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D5:')

    def show_6_DataTo(self):
        date_from = self.detal_info_sensor_6.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_6.cal2.selectedDate()
        print('show_6_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_6.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_6.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_6.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D5:')

    def show_7_DataFrom(self):
        date_from = self.detal_info_sensor_7.cal.selectedDate()
        print('show_7_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_7.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_7.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_7.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_7.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D6:')

    def show_7_DataTo(self):
        date_from = self.detal_info_sensor_7.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_7.cal2.selectedDate()
        print('show_7_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_7.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_7.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_7.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D6:')

    def show_8_DataFrom(self):
        date_from = self.detal_info_sensor_8.cal.selectedDate()
        print('show_8_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_8.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_8.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_8.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_8.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D7:')

    def show_8_DataTo(self):
        date_from = self.detal_info_sensor_8.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_8.cal2.selectedDate()
        print('show_8_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_8.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_8.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_8.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D7:')

    def show_9_DataFrom(self):
        date_from = self.detal_info_sensor_9.cal.selectedDate()
        print('show_9_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_9.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_9.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_9.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_9.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D8:')

    def show_9_DataTo(self):
        date_from = self.detal_info_sensor_9.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_9.cal2.selectedDate()
        print('show_9_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_9.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_9.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_9.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D8:')

    def show_10_DataFrom(self):
        date_from = self.detal_info_sensor_10.cal.selectedDate()
        print('show_10_DataFrom  ' + str(date_from.toPyDate()))
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_10.cal2.selectedDate()
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateTo = dateFrom
            self.detal_info_sensor_10.cal2.setSelectedDate(date_from)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateTo = dateFrom
                self.detal_info_sensor_10.cal2.setSelectedDate(date_from)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateTo = dateFrom
                    self.detal_info_sensor_10.cal2.setSelectedDate(date_from)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D9:')

    def show_10_DataTo(self):
        date_from = self.detal_info_sensor_10.cal.selectedDate()
        dateFrom = 'DATA_' + str(date_from.toPyDate())  # + id

        date_to = self.detal_info_sensor_10.cal2.selectedDate()
        print('show_10_DataTo  ' + str(date_to.toPyDate()))
        dateTo = 'DATA_' + str(date_to.toPyDate())  # + id

        if int(str(date_from.toPyDate()).split('-')[0]) > int(str(date_to.toPyDate()).split('-')[0]):
            dateFrom = dateTo
            self.detal_info_sensor_10.cal.setSelectedDate(date_to)
        elif int(str(date_from.toPyDate()).split('-')[0]) == int(str(date_to.toPyDate()).split('-')[0]):
            if int(str(date_from.toPyDate()).split('-')[1]) > int(str(date_to.toPyDate()).split('-')[1]):
                dateFrom = dateTo
                self.detal_info_sensor_10.cal.setSelectedDate(date_to)
            elif int(str(date_from.toPyDate()).split('-')[1]) == int(str(date_to.toPyDate()).split('-')[1]):
                if int(str(date_from.toPyDate()).split('-')[2]) > int(str(date_to.toPyDate()).split('-')[2]):
                    dateFrom = dateTo
                    self.detal_info_sensor_10.cal.setSelectedDate(date_to)
                else:
                    self.func_read_log(dateFrom, dateTo, 'D9:')

    def close_all_show(self):
        self.detal_info_sensor_1.hide()
        self.detal_info_sensor_2.hide()
        self.detal_info_sensor_3.hide()
        self.detal_info_sensor_4.hide()
        self.detal_info_sensor_5.hide()
        self.detal_info_sensor_6.hide()
        self.detal_info_sensor_7.hide()
        self.detal_info_sensor_8.hide()
        self.detal_info_sensor_9.hide()
        self.detal_info_sensor_10.hide()

        self.sensor_label_1.setStyleSheet(None)
        self.sensor_label_2.setStyleSheet(None)
        self.sensor_label_3.setStyleSheet(None)
        self.sensor_label_4.setStyleSheet(None)
        self.sensor_label_5.setStyleSheet(None)
        self.sensor_label_6.setStyleSheet(None)
        self.sensor_label_7.setStyleSheet(None)
        self.sensor_label_8.setStyleSheet(None)
        self.sensor_label_9.setStyleSheet(None)
        self.sensor_label_10.setStyleSheet(None)

        self.info_bat.hide()
        self.info_tem.hide()
        self.info_hum.hide()
        self.info_gsm.hide()
        self.info_txb.hide()
        self.info_rxb.hide()

    def bat_info(self):
        print('info BAT')
        self.info_bat.number = 'BAT'
        self.info_bat.label_number.setText(self.info_bat.number)
        if self.info_bat.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()
            self.info_bat.show()

        self.info_bat.axes.clear()
        self.info_bat.axes.set_ylabel(self.info_bat.yText)
        self.info_bat.axes.set_xticks(range(len(self.counter_bat_arc) + 1))
        self.info_bat.axes.plot(self.counter_bat_arc, '#ffd700', linewidth=1)
        self.info_bat.canvas.draw()

    def tep_info(self):
        print('info TEM')
        self.info_tem.number = 'TEMP'
        self.info_tem.label_number.setText(self.info_tem.number)
        if self.info_tem.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()
            self.info_tem.show()

        self.info_tem.axes.clear()
        self.info_tem.axes.set_ylabel(self.info_tem.yText)
        self.info_tem.axes.set_xticks(range(len(self.counter_tem_arc) + 1))
        self.info_tem.axes.plot(self.counter_tem_arc, '#ffd700', linewidth=1)
        self.info_tem.canvas.draw()

    def hum_info(self):
        print('info HUM')
        self.info_hum.number = 'HUM'
        self.info_hum.label_number.setText(self.info_hum.number)
        if self.info_hum.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()
            self.info_hum.show()

        self.info_hum.axes.clear()
        self.info_hum.axes.set_ylabel(self.info_hum.yText)
        self.info_hum.axes.set_xticks(range(len(self.counter_hum_arc) + 1))
        self.info_hum.axes.plot(self.counter_hum_arc, '#ffd700', linewidth=1)
        self.info_hum.canvas.draw()

    def gsm_info(self):
        print('info GSM')
        self.info_gsm.number = 'GSM'
        self.info_gsm.label_number.setText(self.info_gsm.number)
        if self.info_gsm.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()
            self.info_gsm.show()

        self.info_gsm.axes.clear()
        self.info_gsm.axes.set_ylabel(self.info_gsm.yText)
        self.info_gsm.axes.set_xticks(range(len(self.counter_gsm_arc) + 1))
        self.info_gsm.axes.plot(self.counter_gsm_arc, '#ffd700', linewidth=1)
        self.info_gsm.canvas.draw()

    def txb_info(self):
        print('info Tx')
        self.info_txb.number = 'Tx'
        self.info_txb.label_number.setText(self.info_txb.number)
        if self.info_txb.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()
            self.info_txb.show()

        self.info_txb.axes.clear()
        self.info_txb.yText = self.tx_text_bytes
        self.info_txb.axes.set_ylabel(self.info_txb.yText)
        self.info_txb.axes.set_xticks(range(len(self.counter_tx_arc) + 1))
        self.info_txb.axes.plot(self.counter_tx_arc, '#ffd700', linewidth=1)
        self.info_txb.canvas.draw()

    def rxb_info(self):
        print('info Rx')
        self.info_rxb.number = 'Rx'
        self.info_rxb.label_number.setText(self.info_rxb.number)
        if self.info_rxb.isVisible():
            self.close_all_show()
        else:
            self.close_all_show()
            self.info_rxb.show()

        self.info_rxb.axes.clear()
        self.info_rxb.yText = self.rx_text_bytes
        self.info_rxb.axes.set_ylabel(self.info_rxb.yText)
        self.info_rxb.axes.set_xticks(range(len(self.counter_rx_arc) + 1))
        self.info_rxb.axes.set_xticklabels(self.counter_time_arc, rotation=45)
        self.info_rxb.axes.plot(self.counter_rx_arc, '#ffd700', linewidth=1)
        self.info_rxb.canvas.draw()


class Thread4Server(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.conn = 0
        self.addr = 0
        self.flag_run = 0

        self.ip = 0
        self.port = 0

        self.acceptThread = Thread4Accept()
        self.speakThread = []

        self.connect(self.acceptThread, QtCore.SIGNAL("newAccept(QString)"),
                     self.func_connect, QtCore.Qt.QueuedConnection)

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
        self.speakThread.append(Thread4Speak())
        self.connect(self.speakThread[len(self.speakThread) - 1], QtCore.SIGNAL("newM(QString)"),
                     self.func_rec, QtCore.Qt.QueuedConnection)
        self.connect(self.speakThread[len(self.speakThread) - 1], QtCore.SIGNAL("newClose(QString)"),
                     self.func_close_session, QtCore.Qt.QueuedConnection)
        self.speakThread[len(self.speakThread) - 1].conn = self.acceptThread.conn
        self.speakThread[len(self.speakThread) - 1].addr = self.acceptThread.addr

        # self.func_write_log('  ' + str(self.acceptThread.conn))
        # self.func_write_log('  ' + str(self.acceptThread.addr))
        # self.emit(QtCore.SIGNAL("rec(QString)"), '  ' + str(self.acceptThread.conn))
        # self.emit(QtCore.SIGNAL("rec(QString)"), '  ' + str(self.acceptThread.addr))

        self.speakThread[len(self.speakThread) - 1].flag_run = 1
        self.speakThread[len(self.speakThread) - 1].start()

        self.emit(QtCore.SIGNAL("label_clients(QString)"), 'Number of active clients: %s' % str(len(self.speakThread)))
        # self.label_clients.setText('Number of active clients: %s' % str(len(self.speakThread)))

    def func_rec(self, temp):
        # print('func_rec')
        new_time = str(datetime.now())
        # print(new_time)
        # print(temp)
        try:
            file = open('stab_test_1', 'a')
            file.write(new_time + temp + '\n')
            file.close()
        except:
            file = open('stab_test_1', 'w')
            file.write(new_time + temp + '\n')
            file.close()

        self.emit(QtCore.SIGNAL("rec(QString)"), temp)

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


class Thread4Speak(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.conn = 0
        self.addr = 0
        self.flag_run = 0

    def run(self):
        while self.flag_run:
            try:
                data = self.conn.recv(1000000)
            except ConnectionResetError:
                self.emit(QtCore.SIGNAL("newM(QString)"), 'ConnectionResetError')
                print('ConnectionResetError')
                # print(self.addr)
                self.conn.close()
                self.emit(QtCore.SIGNAL("newClose(QString)"), str(self.addr))
                break
            except:
                print('else')
                # print(self.addr)
                self.conn.close()
                self.emit(QtCore.SIGNAL("newClose(QString)"), str(self.addr))
                break
            else:
                if not data:
                    print('No data')
                    # print(self.addr)
                    self.conn.close()
                    self.flag_run = 0
                    self.emit(QtCore.SIGNAL("newClose(QString)"), str(self.addr))
                    break
                elif 'close' in data.decode('cp1251'):
                    self.emit(QtCore.SIGNAL("newClose(QString)"), 'close_ok')
                    print(self.addr)
                    # self.conn.close()

                else:
                    udata = data.decode('cp1251')
                    # print('DATA: ' + udata)
                    # print(self.addr)
                    # self.conn.send(b'And you\n')
                    self.emit(QtCore.SIGNAL("newM(QString)"), udata)

        # conn.close()


class Thread4Accept(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.sock = 0
        self.conn = 0
        self.addr = 0

    def run(self):
        while True:
            try:
                self.conn, self.addr = self.sock.accept()
            except:
                print('Error accept')
                break
            else:
                print(self.conn)
                print(self.addr)
                self.emit(QtCore.SIGNAL("newAccept(QString)"), '0')


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = ServerOnSocket()
    main.show()
    sys.exit(app.exec_())
