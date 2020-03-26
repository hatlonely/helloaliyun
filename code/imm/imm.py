#!/usr/bin/env python3

import requests
import urllib
import datetime
import random
import hmac
import base64
import os
import configparser


access_key_id = "see https://usercenter.console.aliyun.com/#/manage/ak"
access_key_secret = "see https://usercenter.console.aliyun.com/#/manage/ak"

def env():
    global access_key_id
    global access_key_secret
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser("~"), ".ossutilconfig"))
    access_key_id = config["Credentials"]["accessKeyID"]
    access_key_secret = config["Credentials"]["accessKeySecret"]

# https://help.aliyun.com/document_detail/74947.html?spm=a2c4g.11186623.2.22.335226c5dUnarR
def preview():
    res = requests.get("https://preview.imm.aliyuncs.com/index.html", params={
        "url": "https://hatlonely-test-bucket.oss-cn-beijing.aliyuncs.com/hello.docx/imm",
        "accessKeyId": access_key_id,
        "accessKeySecret": access_key_secret,
        "region": "oss-cn-beijing",
        "bucket": "hatlonely-test-bucket"
    })
    print(urllib.parse.unquote(res.url))

def encode(message):
    return urllib.parse.quote(str(message), safe='', encoding="utf-8").replace("+", "%20").replace("*", "%2A").replace("%7E", "~")

def convert():
    random.seed()
    params = {
        "Project": "ossdocdefault",
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": "cn-beijing",
        "Bucket": "hatlonely-test-bucket",
        "Version": "2017-09-06",
        "Timestamp": datetime.datetime.utcnow().isoformat(),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": random.randint(0, 2**63-1),
        "Action": "ConvertOfficeFormat",
        "SrcUri": "oss://hatlonely-test-bucket/hello.docx",
        "TgtType": "vector",
        "TgtUri": "oss://hatlonely-test-bucket/hello.docx/imm"
    }

    kvs = "&".join(["{}={}".format(encode(i), encode(params[i])) for i in sorted(params)])
    to_sign = "POST" + "&" + encode("/") + "&" + "" + encode(kvs)
    params["Signature"] = base64.b64encode(hmac.new((access_key_secret + '&').encode(), to_sign.encode(), digestmod='sha1').digest())

    res = requests.post("https://imm.cn-beijing.aliyuncs.com", params=params)
    print(res)
    print(res.content)


def test_sign():
    # http://imm.cn-shanghai.aliyuncs.com/?Project=test-project&RegionId=cn-shanghai&AccessKeyId=testid&Format=JSON&SignatureMethod=HMAC-SHA1&SignatureVersion=1.0&SignatureNonce=d1ac7371108dc53541c9d0f29e5396c7&Timestamp=2019-02-22T09%3A30%3A54Z&Action=GetProject&Version=2017-09-06
    params = {
        "Project": "test-project",
        "RegionId": "cn-shanghai",
        "AccessKeyId": "testid",
        "Format": "JSON",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": "d1ac7371108dc53541c9d0f29e5396c7",
        "Timestamp": "2019-02-22T09:30:54Z",
        "Action": "GetProject",
        "Version": "2017-09-06",
    }

    kvs = "&".join(["{}={}".format(encode(i), encode(params[i])) for i in sorted(params)])
    to_sign = "POST" + "&" + encode("/") + "&" + "" + encode(kvs)
    params["Signature"] = to_sign

    print(to_sign)
    print(base64.b64encode(hmac.new(b"testsecret&", to_sign.encode(), digestmod='sha1').digest()))

    to_sign = "POST&%2F&AccessKeyId%3Dtestid&Action%3DGetProject&Format%3DJSON&Project%3Dtest-project&RegionId%3Dcn-shanghai&SignatureMethod%3DHMAC-SHA1&SignatureNonce%3Dd1ac7371108dc53541c9d0f29e5396c7&SignatureVersion%3D1.0&Timestamp%3D2019-02-22T09%253A30%253A54Z&Version%3D2017-09-06"
    print(to_sign)
    print(base64.b64encode(hmac.new(b"testsecret&", to_sign.encode(), digestmod='sha1').digest()))


def main():
    env()
    # convert()
    preview()
    # test_sign()

if __name__ == "__main__":
    main()

