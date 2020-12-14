import sys

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QLCDNumber, QFileDialog, QDesktopWidget
from deviceinfoV2 import *
from signal import *
import os
import re
import recordtool


# class RecordThread(QThread):  # 步骤1.创建一个线程实例
#     def __init__(self):
#         super(RecordThread, self).__init__()
#         self.rdy = False
#         self.input_id = -1
#         self.output_id = -1
#         self.signal_pattern = 0
#         self.rec_path = -1
#         self.fs = 48e3
#         self.channels = 1
#
#     def set_params(self, input_device_id, output_device_id, signal, rec_file_path, fs, rec_file_channels):
#         self.input_id = input_device_id
#         self.output_id = output_device_id
#         self.signal_pattern = signal
#         self.rec_path = rec_file_path
#         self.fs = fs
#         self.channels = rec_file_channels
#         self.rdy = True
#
#     def run(self):
#         if self.rdy:
#             try:
#                 play_and_record(self.input_id, self.output_id, self.signal_pattern, self.rec_path, self.fs,
#                                 self.channels)
#             except:
#                 print("Unexpected error:", sys.exc_info()[0])
#         else:
#             print("未设置参数")


class MyLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


def get_device_id(text):
    did = -1
    m = re.match(r'(.*):(.*)', text)
    if m:
        did = m.group(1)
    return int(did)


class RecordUI(QWidget):
    def __init__(self):
        super().__init__()
        self._running = False
        self.drivers = get_drivers()
        # ui
        self.input_lb = QLabel("Input", self)
        self.output_lb = QLabel("Output", self)
        self.input_driver_lb = QLabel('Driver', self)
        self.output_driver_lb = QLabel('Driver', self)
        self.input_device_lb = QLabel('Device', self)
        self.output_device_lb = QLabel('Device', self)
        self.signal_lb = QLabel('Signal', self)

        self.save_dir = MyLineEdit(self)
        self.dir1 = QLineEdit(self)
        self.dir2 = QLineEdit(self)
        self.filename = QLineEdit(self)

        self.input_driver = QComboBox()
        self.output_driver = QComboBox()
        self.input_device = QComboBox()
        self.output_device = QComboBox()
        self.signal = QComboBox()

        self.start = QPushButton('Start', self)
        self.stop = QPushButton('Stop', self)

        self.time = QLCDNumber()
        self.time.setMinimumHeight(100)
        self.time.setDigitCount(5)
        self.time.setMode(QLCDNumber.Dec)
        self.time.setSegmentStyle(QLCDNumber.Flat)
        self.time.display("00:00")

        self.record_thread = recordtool.Record(self.time)

        self.initUI()

    def initUI(self):
        # 全局vbox
        vbox = QVBoxLayout()
        # 输入输出设备选择初始化
        input_box, output_box = self.init_audio_io()
        vbox.addWidget(self.input_lb)
        vbox.addLayout(input_box)
        vbox.addWidget(self.output_lb)
        vbox.addLayout(output_box)
        # 信号选择初始化
        singal_box = self.init_signal()
        vbox.addLayout(singal_box)
        # 存储路径初始化
        sf_box = self.init_save_file()
        vbox.addLayout(sf_box)
        # 开始结束按键初始化
        ss_box = self.init_button()
        vbox.addLayout(ss_box)

        vbox.addWidget(self.time)

        self.setLayout(vbox)
        self.resize(800, 320)
        self.center()
        self.setWindowTitle('Gesture Recorder')
        self.show()

    def center(self):
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_audio_io(self):
        input_box = QHBoxLayout()
        input_box.addWidget(self.input_driver_lb)
        input_box.addWidget(self.input_driver)
        input_box.addWidget(self.input_device_lb)
        input_box.addWidget(self.input_device)
        self.input_driver.addItems([driver['name'] for driver in self.drivers])
        self.input_driver.activated[str].connect(self.on_input_drive_selected)

        output_box = QHBoxLayout()
        output_box.addWidget(self.output_driver_lb)
        output_box.addWidget(self.output_driver)
        output_box.addWidget(self.output_device_lb)
        output_box.addWidget(self.output_device)
        self.output_driver.addItems([driver['name'] for driver in self.drivers])
        self.output_driver.activated[str].connect(self.on_output_drive_selected)
        return input_box, output_box

    def on_input_drive_selected(self, driver):
        input_devices = get_devices(self.drivers, kind='Input', driver=driver)
        self.input_device.clear()
        self.input_device.addItems([f"{device['id']}:{device['name']}" for device in input_devices])

    def on_output_drive_selected(self, driver):
        output_devices = get_devices(self.drivers, kind='Output', driver=driver)
        self.output_device.clear()
        self.output_device.addItems([f"{device['id']}:{device['name']}" for device in output_devices])

    def init_signal(self):
        signal_box = QHBoxLayout()
        signal_box.addWidget(self.signal_lb)
        signal_box.addWidget(self.signal)
        self.signal.addItems(signal_types)
        return signal_box

    def init_save_file(self):
        signal_box = QHBoxLayout()
        signal_box.addWidget(self.save_dir)
        self.save_dir.setFocusPolicy(Qt.NoFocus)
        self.save_dir.setText(os.getcwd())
        self.save_dir.clicked.connect(self.show_dir_dialogue)
        signal_box.setStretchFactor(self.save_dir, 4)

        signal_box.addWidget(QLabel('/'))
        signal_box.addWidget(self.dir1)
        self.dir1.setText('0')
        signal_box.setStretchFactor(self.dir1, 1)

        signal_box.addWidget(QLabel('/'))
        signal_box.addWidget(self.dir2)
        self.dir2.setText('0')
        signal_box.setStretchFactor(self.dir2, 1)

        signal_box.addWidget(QLabel('/'))
        signal_box.addWidget(self.filename)
        self.filename.setText('0')
        signal_box.setStretchFactor(self.filename, 1)
        signal_box.addWidget(QLabel('.wav'))

        return signal_box

    def show_dir_dialogue(self):
        dir_name = QFileDialog.getExistingDirectory(self, directory=os.getcwd())
        self.save_dir.setText(dir_name)

    def init_button(self):
        ss_box = QHBoxLayout()
        self.start.setStyleSheet("background-color:lightgreen")
        self.start.clicked.connect(self.start_playrec)
        ss_box.addWidget(self.start)
        self.stop.setStyleSheet("background-color:#CD2626")
        self.stop.clicked.connect(self.stop_playrec)
        ss_box.addWidget(self.stop)
        return ss_box

    def start_playrec(self):
        if not self._running:
            input_id = get_device_id(self.input_device.currentText())
            output_id = get_device_id(self.output_device.currentText())
            if input_id == -1 or output_id == -1:
                self.setWindowTitle("请选择输入/输出设备")
                return
            signal_pattern = get_signal_by_type(self.signal.currentText())
            rec_path = self.create_save_path()

            in_d = p.get_device_info_by_index(input_id)
            self.record_thread.set_param(input_id, output_id, in_d['maxInputChannels'], rec_path)
            try:
                self.record_thread.play_and_record(signal_pattern)
            except:
                self.setWindowTitle("Unexpected error:" + sys.exc_info()[0])
            self._running = True
            self.setWindowTitle("正在录制中...")
        else:
            self.setWindowTitle("已经开始录制")

    def stop_playrec(self):
        if self._running:
            try:
                self.record_thread.stop()
                self.setWindowTitle("停止录制")
            except:
                self.setWindowTitle("Unexpected error:"+sys.exc_info()[0])
            finally:
                self._running = False
            try:
                num = int(self.filename.text())
                num = num + 1
                self.filename.setText(str(num))
            except:
                pass
        else:
            self.setWindowTitle("还没开始录制")

    def create_save_path(self):
        path1 = os.path.join(self.save_dir.text(), self.dir1.text())
        if not os.path.exists(path1):
            os.mkdir(path1)
        path2 = os.path.join(path1, self.dir2.text())
        if not os.path.exists(path2):
            os.mkdir(path2)

        return os.path.join(path2, f'{self.filename.text()}.wav')

    # 按键录制 ese
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            if self._running:
                self.stop_playrec()
            else:
                self.start_playrec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RecordUI()
    sys.exit(app.exec_())
