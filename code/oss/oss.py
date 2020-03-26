#!/usr/bin/env python3

# pip3 install oss2
# pip3 install aliyun-python-sdk-imm

import oss2
import configparser
import os

access_key_id = "see https://usercenter.console.aliyun.com/#/manage/ak"
access_key_secret = "see https://usercenter.console.aliyun.com/#/manage/ak"
endpoint="oss-cn-beijing.aliyuncs.com"

def env():
    global access_key_id
    global access_key_secret
    global endpoint
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser("~"), ".ossutilconfig"))
    access_key_id = config["Credentials"]["accessKeyID"]
    access_key_secret = config["Credentials"]["accessKeySecret"]
    endpoint = config["Credentials"]["endpoint"]

def main():
    env()
    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, 'hatlonely-test-bucket')
    
    key = "hello.txt"
    bucket.put_object(key, 'Ali Baba is a happy youth.')
    bucket.get_object(key).read()

    for object_info in oss2.ObjectIterator(bucket):
        print(object_info.key)


if __name__ == '__main__':
    main()