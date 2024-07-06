import datetime
import sys
import json
import time
import random

from core.device import Device
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect
from PyQt5.QtCore import QDateTime, QTimer
from UI.ui_mainwindow import Ui_MainWindow


def create_shadow(blur_radius=0.3, x_offset=0.3, y_offset=0.6):
    """
    创建并返回一个具有阴影效果的 QGraphicsDropShadowEffect 对象。
    :param blur_radius: 模糊半径，控制阴影的模糊程度。
    :param x_offset: 阴影在 x 轴上的偏移量。
    :param y_offset: 阴影在 y 轴上的偏移量。
    :return: 具有指定参数的 QGraphicsDropShadowEffect 对象。
    """
    shadow = QGraphicsDropShadowEffect()  # 创建对象
    shadow.setBlurRadius(blur_radius)  # 设置模糊半径
    shadow.setXOffset(x_offset)  # 设置阴影在 x 轴上的偏移量
    shadow.setYOffset(y_offset)  # 设置阴影在 y 轴上的偏移量
    return shadow


class Devices:
    def __init__(self, file):
        self.devices_info = None
        self.devices = []
        with open(file, 'r') as devices_file:
            self.devices_info = json.load(devices_file)
        self.load_device_info()

    def load_device_info(self):
        for i in range(self.devices_info["deviceNum"]):
            sensor_name = self.devices_info["device_index"][i]
            productKey = self.devices_info[sensor_name]["productKey"]
            deviceName = self.devices_info[sensor_name]["deviceName"]
            deviceSecret = self.devices_info[sensor_name]["deviceSecret"]
            host = self.devices_info[sensor_name]["host"]
            port = self.devices_info[sensor_name]["port"]
            self.devices.append(Device(
                sensorname=sensor_name,
                productkey=productKey,
                devicename=deviceName,
                devicesecret=deviceSecret,
                clientid=deviceName,
                host=host,
                port=port,
                tls_crt="/Users/ppy/study/program/Course_Design/SimDevice/core/root.crt"
            ))

    def get_sensor_name(self, index):
        return self.devices[index].get_sensor_name()

    def is_connected(self, index):
        return self.devices[index].is_connected()

    def get_device(self, index):
        return self.devices[index]


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, dvs: Devices):
        super().__init__()
        self.setupUi(self)
        self.dvs = dvs
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.send_timer = QTimer(self)

        self.setStyleSheet("background-color: rgb(234, 235, 236);")
        self.setWindowTitle("IoT Device Simulator")

        self.sensor_labels = [self.label_1, self.label_2, self.label_3]
        self.status_labels = [self.status_1, self.status_2, self.status_3]
        self.spinbox_labels = [self.doubleSpinBox_1, self.doubleSpinBox_2, self.doubleSpinBox_3]
        self.lcd_labels = [self.lcdNumber_1, self.lcdNumber_2, self.lcdNumber_3]
        self.single_connect_buttons = [
            self.device_1_connect_button,
            self.device_2_connect_button,
            self.device_3_connect_button]
        self.single_disconnect_buttons = [
            self.device_1_disconnect_button,
            self.device_2_disconnect_button,
            self.device_3_disconnect_button]

        self._load_device()

        self.dashboard.setGraphicsEffect(create_shadow())
        # self.panel_window.setGraphicsEffect(create_shadow())
        self.info_board_window.setGraphicsEffect(create_shadow())

        # slot signal function
        self.connect_to_iot_button.clicked.connect(self._connect_to_iot)
        self.check_connection_button.clicked.connect(self._check_connection)
        # self.timer.timeout.connect(self._update_status)
        self.submit_button.clicked.connect(self._submit)
        self.disconnect_button.clicked.connect(self._disconnect)
        self.random_button.clicked.connect(self._random_value)
        self.send_timer.timeout.connect(self._timeout_send)
        for single_connect_button in self.single_connect_buttons:
            single_connect_button.clicked.connect(self._connect_single_slot)
        for i, single_disconnect_button in enumerate(self.single_disconnect_buttons):
            single_disconnect_button.clicked.connect(self._disconnect_single_slot)

    def _timeout_send(self):
        self._random_value()
        self._submit()

    def _load_device(self):
        for i, sensor_label in enumerate(self.sensor_labels):
            device = self.dvs.get_device(i)
            device.on_connect_signal.connect(self._on_connect_slot)
            device.publish_signal.connect(self._publish_message_slot)
            device.disconnect_signal.connect(self._disconnect_slot)
            device.on_message_signal.connect(self._on_message_slot)

            sensor_label.setText(self.dvs.get_sensor_name(i))

        self._add_text2info_board("Device init load success!")
        self.send_timer.start(20 * 1000)
        self._update_status()

    def _update_status(self):
        for i, status_label in enumerate(self.status_labels):
            if self.dvs.is_connected(i):
                status_label.setStyleSheet("background-color: green; border-radius: 10px;")
            else:
                status_label.setStyleSheet("background-color: red; border-radius: 10px;")

    def _on_connect_slot(self, msg):
        self._update_status()
        self._add_text2info_board(msg)

    def _publish_message_slot(self, msg):
        self._add_text2info_board(msg)

    def _disconnect_slot(self, msg):
        self._update_status()
        self._add_text2info_board(msg)

    def _on_message_slot(self, device, payload):
        self._add_text2info_board(payload)
        i = self.dvs.devices.index(device)
        msg = json.loads(payload)
        if msg['query'] == 'update':
            self.publish_message(i, self.spinbox_labels[i])

    def _connect_single_slot(self):
        sender = self.sender()
        for i, single_connect_button in enumerate(self.single_connect_buttons):
            if single_connect_button == sender:
                device = self.dvs.get_device(i)
                self._device_connect(device)

    def _disconnect_single_slot(self):
        sender = self.sender()
        for i, single_disconnect_button in enumerate(self.single_disconnect_buttons):
            if single_disconnect_button == sender:
                device = self.dvs.get_device(i)
                device.disconnect()

    def _connect_to_iot(self):
        for device in self.dvs.devices:
            self._device_connect(device)
        # self._update_status()

    def _device_connect(self, device):
        if device.is_connected():
            self._add_text2info_board(f"{device.get_sensor_name()} already connect to Aliyun Iot Service")
            return
        device.connect()
        device.subscribe_topic()
        self.timer.start(500)

    def _random_value(self):
        for i, spinbox_label in enumerate(self.spinbox_labels):
            value = random.uniform(spinbox_label.minimum(), spinbox_label.maximum())
            spinbox_label.setValue(value)

    def _add_text2info_board(self, text):
        datatime = QDateTime().currentDateTime()
        current_time = datatime.toString("yyyy-MM-dd hh:mm:ss")
        self.info_board.append(current_time + ": " + text + '\n')
        self.info_board.verticalScrollBar().setValue(self.info_board.verticalScrollBar().maximum())

    def _check_connection(self):
        self._update_status()
        self._add_text2info_board("Already update device status!")

    def _submit(self):
        # pass
        for i, spinbox_label in enumerate(self.spinbox_labels):
            self.publish_message(i, spinbox_label)
            # self.timer.start(500)
            # time.sleep(5)

    def publish_message(self, index, spinbox_label):
        device = self.dvs.get_device(index)
        info = spinbox_label.value()
        lcd_label = self.lcd_labels[index]
        lcd_label.display(spinbox_label.text())
        msg = {
            "device_name": self.dvs.get_sensor_name(index),
            "Location": 'Nanjing',
            "date": QDateTime.currentDateTime().toString("yyyy-MM-dd-hh-mm-ss"),
            "status": self.dvs.is_connected(index),
            "parameter": info
        }
        msg = json.dumps(msg)
        device.publish_message(msg)


    def _disconnect(self):
        for device in self.dvs.devices:
            device.disconnect()


if __name__ == "__main__":
    devices = Devices(file="device_info.json")
    app = QApplication(sys.argv)
    window = MainWindow(devices)
    window.show()
    sys.exit(app.exec_())
