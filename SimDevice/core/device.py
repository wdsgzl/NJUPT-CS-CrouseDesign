import json
import time
import paho.mqtt.client as mqtt
from SimDevice.core.MqttSign import AuthIfo
import logging
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

# config log
__log_format = '%(asctime)s-%(process)d-%(thread)d - %(name)s:%(module)s:%(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(format=__log_format)


class Device(QObject):
    # 链接的 signal
    on_connect_signal = pyqtSignal(str)
    publish_signal = pyqtSignal(str)
    disconnect_signal = pyqtSignal(str)
    on_message_signal = pyqtSignal(object, str)

    def __init__(self, sensorname, productkey, devicename, devicesecret, clientid, host, port, tls_crt, keepAlive=300):
        super().__init__()
        # device information
        self.sensorName = sensorname
        self.productKey = productkey
        self.deviceName = devicename
        self.deviceSecret = devicesecret
        self.clientId = clientid
        self.host = host
        self.port = port
        self.tls_crt = tls_crt
        self.keepAlive = keepAlive
        # self.timer = QTimer(self)
        # self.timer.setSingleShot(True)

        self.timeStamp = str((int(round(time.time() * 1000))))
        self.subTopic = "/" + self.productKey + "/" + self.deviceName + "/user/get"
        self.pubTopic = "/" + self.productKey + "/" + self.deviceName + "/user/update"

        self.auto_info = AuthIfo()
        self.auto_info.calculate_sign_time(self.productKey,
                                           self.deviceName, self.deviceSecret, self.clientId, self.timeStamp)

        self.client = mqtt.Client(self.auto_info.mqttClientId)
        self.client.username_pw_set(username=self.auto_info.mqttUsername, password=self.auto_info.mqttPassword)
        self.client.tls_set(self.tls_crt)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # self.client.enable_logger(logging.DEBUG)

    def get_sensor_name(self) -> str:
        return self.sensorName

    def is_connected(self) -> bool:
        return self.client.is_connected()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            msg = f"Connect to {self.sensorName} on Aliyun Iot Cloud Success"
            print(msg)
        else:
            msg = f"Connect to {self.sensorName} failed... error code is {rc}"
            print(msg)
        self.on_connect_signal.emit(msg)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Receive message from {self.sensorName} ---------- topic is: {topic}")
        print(f"Receive message from {self.sensorName} ---------- payload is: {payload}")

        self.on_message_signal.emit(self, payload)
        if "thing/service/property/set" in topic:
            self.on_thing_prop_changed(client, msg.topic, msg.payload)

    def on_thing_prop_changed(self, client, topic, payload):
        post_topic = topic.replace("service", "event").replace("set", "post")
        Msg = json.loads(payload)
        params = Msg['params']
        post_payload = "{\"params\":" + json.dumps(params) + "}"
        print(f"Receive property_set command for {self.deviceName}, need to post ---------- topic is: {post_topic}")
        print(f"Receive property_set command for {self.deviceName}, need to post ---------- payload is: {post_payload}")
        self.client.publish(post_topic, post_payload)

    def connect(self):

        self.client.loop_start()
        self.client.connect(self.host, self.port, self.keepAlive)
        self.client.loop_stop()
        self.client.loop_start()
        # self.client.loop_stop()
        # print(f"Connect {self.deviceName} to iot: {self.client.is_connected()}")
        # self.client.loop_start()
        # self.timer.start(1000)
        # time.sleep(0.5)

    def disconnect(self):
        msg = f"{self.sensorName} disconnect!"
        # self.client.loop_start()
        self.client.disconnect()
        self.client.loop_stop()
        self.disconnect_signal.emit(msg)

    def publish_message(self, message, count=5):
        try:
            if self.client.is_connected():
                self.client.loop_start()
                info = self.client.publish(self.pubTopic, message, qos=0)
                self.client.loop_stop()
                self.client.loop_start()
                if info.is_published():
                    msg = f"{self.sensorName} successfully publish message <{message}>"
                    print(msg)
                else:
                    msg = f"{self.sensorName} fail to publish message <{message}>"
                self.publish_signal.emit(msg)
            else:
                if not self.client.is_connected():
                    msg = f"{self.sensorName} hasn't connect to Aliyun Iot Cloud service"
                self.publish_signal.emit(msg)
        except:
            msg = "Unknown error"
            self.publish_signal.emit(msg)

    def subscribe_topic(self):
        self.client.subscribe(self.subTopic)
        print(f"Subscribe topic for {self.deviceName}: {self.subTopic}")

    def run(self):
        self.connect()
        # a = input("input:")
        self.subscribe_topic()
        self.publish_message(message="ABC")
        while True:
            print(self.client.is_connected())
            time.sleep(1)


if __name__ == "__main__":
    # device_sw = Device(
    #     productkey="k1ggwxWz3Re",
    #     devicename="wendu",
    #     devicesecret="0b08e6ad0e8673271a81983528a746d4",
    #     clientid="test1",
    #     host="iot-06z00emwrpwm0x1.mqtt.iothub.aliyuncs.com",
    #     port=1883,
    #     tls_crt="/Users/ppy/study/program/Course_Design/SimDevice/core/root.crt"
    # )
    device_test = Device(
        sensorname="test",
        productkey="k1ggv82Lho8",
        devicename="test",
        devicesecret="64d13b09ece823189ec1dae98a0ed746",
        clientid="test",
        host="iot-06z00i0sutigtd7.mqtt.iothub.aliyuncs.com",
        port=1883,
        tls_crt="/Users/ppy/study/program/Course_Design/SimDevice/core/root.crt"
    )
    device_test.run()
