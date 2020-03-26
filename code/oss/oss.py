#!/usr/bin/env python3

# pip3 install oss2
# pip3 install aliyun-python-sdk-imm

import os
import oss2
import util

config = util.load_credential_from_local()
access_key_id = config["accessKeyID"]
access_key_secret = config["accessKeySecret"]
region_id = config["regionID"]
region = config["region"]
endpoint = config["endpoint"]


auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, 'hatlonely-test-bucket')


def put_object(filename):
    bucket.put_object(os.path.basename(filename), open(filename, "rb").read())


def del_object(filename):
    bucket.delete_object(filename)


def list_object():
    for object_info in oss2.ObjectIterator(bucket):
        print(object_info.key)


def main():
    put_object("../asset/test.docx")
    del_object("test.docx")
    list_object()


if __name__ == '__main__':
    main()
