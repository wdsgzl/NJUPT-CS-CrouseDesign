from linkkit import linkkit

lk = linkkit.LinkKit(
    host_name="cn-shanghai",
    product_key="k1ggv82Lho8",
    device_name="test",
    device_secret="64d13b09ece823189ec1dae98a0ed746")          
lk.config_mqtt(endpoint="iot-06z00i0sutigtd7.mqtt.iothub.aliyuncs.com")
lk.config_mqtt(port=1883, protocol="MQTTv311", transport="TCP",
            secure="TLS", keep_alive=60, clean_session=True,
            max_inflight_message=20, max_queued_message=0,
            auto_reconnect_min_sec=1,
            auto_reconnect_max_sec=60,
            check_hostname=True,   
            cadata=None)

def on_connect(session_flag, rc, userdata):
    print("on_connect:%d,rc:%d,userdata:" % (session_flag, rc))
    pass
def on_disconnect(rc, userdata):
    print("on_disconnect:rc:%d,userdata:" % rc)
lk.on_connect = on_connect
lk.on_disconnect = on_disconnect
lk.connect_async()
# lk.start_worker_loop()
# try:
#     # rc, mid = lk.subscribe_topic(lk.to_full_topic("user/test"))
#     rc, mid = lk.publish_topic(lk.to_full_topic("user/pub"), "123")
#     if rc == 0:
#         print("publish topic success:%r, mid:%r" % (rc, mid))
#     else:
#         print("publish topic fail:%d" % rc)
# except:
#     print("connect failure")