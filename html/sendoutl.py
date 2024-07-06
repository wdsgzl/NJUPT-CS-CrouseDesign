# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import json
import os
import sys
import configuration
from typing import List
import base64
import time
import sqlite3
from alibabacloud_iot20180120.client import Client as Iot20180120Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_iot20180120 import models as iot_20180120_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Iot20180120Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=configuration.os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=configuration.os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Iot
        config.endpoint = f'iot.cn-shanghai.aliyuncs.com'
        return Iot20180120Client(config)

    @staticmethod
    def main(
            args: List[str],
    ) -> None:
        msg = {"query": "update"}
        client = Sample.create_client()
        pub_request = iot_20180120_models.PubRequest(
            iot_instance_id='iot-06z00emwrpwm0x1',
            product_key='k1ggwFGtvcl',
            device_name='Light',
            topic_full_name='/k1ggwFGtvcl/Light/user/get',
            message_content=base64.b64encode(bytes((json.dumps(msg)), encoding="utf8"))
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.pub_with_options(pub_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        msg = {"query": "update"}
        client = Sample.create_client()
        pub_request = iot_20180120_models.PubRequest(
            iot_instance_id='iot-06z00emwrpwm0x1',
            product_key='k1ggwFGtvcl',
            device_name='Light',
            topic_full_name='/k1ggwFGtvcl/Light/user/get',
            message_content=base64.b64encode(bytes((json.dumps(msg)), encoding="utf8"))
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.pub_with_options_async(pub_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    conn = sqlite3.connect('../mytest/db.sqlite3')  # 连接数据库
    cur = conn.cursor()
    cur.execute("select * from Lig order by time desc limit 1")
    for row in cur.fetchall():  # 以一条记录为元组单位返回结果给row
        past_l = row[1]

    
    conn.close()
    Sample.main(sys.argv[1:])
    time.sleep(1)


    conn = sqlite3.connect('../mytest/db.sqlite3')  # 连接数据库
    cur = conn.cursor()

    cur.execute("select * from Lig order by time desc limit 1")
    for row in cur.fetchall():  # 以一条记录为元组单位返回结果给row
        current_l = row[1]
    if past_l == current_l:
        cur.execute("insert into Lig Values('光照','{data}','{light}','{status}')".format(
            data=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), light=float(0), status='False'))


    conn.commit()
    conn.close()

