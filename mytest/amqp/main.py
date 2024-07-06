import json
import time
import sys
import hashlib
import hmac
import base64
import stomp
import ssl
import schedule
import threading
import os
import configuration
import sqlite3
import time


def connect_and_subscribe(conn):
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例使用环境变量获取 AccessKey 的方式进行调用，仅供参考
    accessKey = configuration.os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID']
    accessSecret = configuration.os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
    consumerGroupId = "NcX0syzvdsf3hQsGoW4L000100"
    # iotInstanceId：实例ID。
    iotInstanceId = "iot-06z00emwrpwm0x1"
    clientId = "coursedesign"
    # 签名方法：支持hmacmd5，hmacsha1和hmacsha256。
    signMethod = "hmacsha1"
    timestamp = current_time_millis()
    # userName组装方法，请参见AMQP客户端接入说明文档。
    # 若使用二进制传输，则userName需要添加encode=base64参数，服务端会将消息体base64编码后再推送。具体添加方法请参见下一章节“二进制消息体说明”。
    username = clientId + "|authMode=aksign" + ",signMethod=" + signMethod \
               + ",timestamp=" + timestamp + ",authId=" + accessKey \
               + ",iotInstanceId=" + iotInstanceId \
               + ",consumerGroupId=" + consumerGroupId + "|"
    signContent = "authId=" + accessKey + "&timestamp=" + timestamp
    # 计算签名，password组装方法，请参见AMQP客户端接入说明文档。
    password = do_sign(accessSecret.encode("utf-8"), signContent.encode("utf-8"))

    conn.set_listener('', MyListener(conn))
    conn.connect(username, password, wait=True)
    # 清除历史连接检查任务，新建连接检查任务
    schedule.clear('conn-check')
    schedule.every(1).seconds.do(do_check, conn).tag('conn-check')


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn):
        self.conn = conn

    def on_error(self, frame):
        print('received an error "%s"' % frame.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)
        if frame.body.find("Temperature_sensor")+1:
            dict_frame=json.loads(frame.body)#转换为字典
            #print("Temperature:")
            #print(dict_frame["items"]["CurrentTemperature"]["value"])#寻找对应的输入值
            #print("\n")
            tempera=dict_frame["parameter"]
            status_temperature=dict_frame["status"]
            conn = sqlite3.connect('../db.sqlite3')
            cursor = conn.cursor()
            cursor.execute("insert into Tem Values('温感','{data}','{tem}','{status}')".format(data=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),tem=float(tempera),status=status_temperature))
            conn.commit()
            conn.close()
            print(tempera)

        if frame.body.find("Light_sensor")+1:
            dict_frame = json.loads(frame.body)  # 转换为字典
            # print("Temperature:")
            # print(dict_frame["items"]["CurrentTemperature"]["value"])#寻找对应的输入值
            # print("\n")
            lightness = dict_frame["parameter"]
            status_light = dict_frame["status"]
            conn = sqlite3.connect('../db.sqlite3')
            cursor = conn.cursor()
            cursor.execute("insert into Lig Values('光照','{data}','{light}','{status}')".format(data=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), light=float(lightness),status=status_light))
            conn.commit()
            conn.close()
            print(lightness)

        if frame.body.find("CO2_sensor")+1:
            dict_frame = json.loads(frame.body)  # 转换为字典
            # print("Temperature:")
            # print(dict_frame["items"]["CurrentTemperature"]["value"])#寻找对应的输入值
            # print("\n")
            CCOO = dict_frame["parameter"]
            status_CO = dict_frame["status"]
            conn = sqlite3.connect('../db.sqlite3')
            cursor = conn.cursor()
            cursor.execute("insert into Dio Values('二氧化碳浓度','{data}','{CO}','{status}')".format(data=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), CO=float(CCOO),status=status_CO))
            conn.commit()
            conn.close()
            print(CCOO)


    def on_heartbeat_timeout(self):
        print('on_heartbeat_timeout')

    def on_connected(self, headers):
        print("successfully connected")
        conn.subscribe(destination='/topic/#', id=1, ack='auto')
        print("successfully subscribe")

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)


def current_time_millis():
    return str(int(round(time.time() * 1000)))


def do_sign(secret, sign_content):
    m = hmac.new(secret, sign_content, digestmod=hashlib.sha1)
    return base64.b64encode(m.digest()).decode("utf-8")


# 检查连接，如果未连接则重新建连
def do_check(conn):
    print('check connection, is_connected: %s', conn.is_connected())
    if (not conn.is_connected()):
        try:
            connect_and_subscribe(conn)
        except Exception as e:
            print('disconnected, ', e)


# 定时任务方法，检查连接状态
def connection_check_timer():
    while 1:
        schedule.run_pending()
        time.sleep(10)


#  接入域名，请参见AMQP客户端接入说明文档。这里直接填入域名，不需要带amqps://前缀
conn = stomp.Connection([('iot-06z00emwrpwm0x1.amqp.iothub.aliyuncs.com', 61614)], heartbeats=(0, 300))
conn.set_ssl(for_hosts=[('iot-06z00emwrpwm0x1.amqp.iothub.aliyuncs.com', 61614)], ssl_version=ssl.PROTOCOL_TLS)

try:
    connect_and_subscribe(conn)
except Exception as e:
    print('connecting failed')
    raise e

# 异步线程运行定时任务，检查连接状态
thread = threading.Thread(target=connection_check_timer)
thread.start()

