#!/usr/bin/env python3

import requests
import datetime
import random
import util
import urllib
import oss2
import os

config = util.load_credential_from_local()
access_key_id = config["accessKeyID"]
access_key_secret = config["accessKeySecret"]
region_id = config["regionID"]
region = config["region"]
endpoint = config["endpoint"]
bucket = 'hatlonely-test-bucket'


def put_object(filename):
    auth = oss2.Auth(access_key_id, access_key_secret)
    b = oss2.Bucket(auth, endpoint, bucket)
    b.put_object(os.path.basename(filename), open(filename, "rb").read())


def del_object(filename):
    auth = oss2.Auth(access_key_id, access_key_secret)
    b = oss2.Bucket(auth, endpoint, bucket)
    b.delete_object(filename)


def convert(filename, type):
    random.seed()
    params = {
        "Project": "ossdocdefault",
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": bucket,
        "Version": "2017-09-06",
        "Timestamp": datetime.datetime.utcnow().isoformat(),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": random.randint(0, 2**63-1),
        "Action": "ConvertOfficeFormat",
        "SrcUri": "oss://{}/{}".format(bucket, filename),
        "TgtType": type,  # vector | jpg | png | pdf | text
        "TgtUri": "oss://{}/{}/imm/{}".format(bucket, filename, type)
    }
    params["Signature"] = util.signature("POST", params, access_key_secret)

    res = requests.post(
        "https://imm.{}.aliyuncs.com".format(region_id), params=params)
    print(res)
    print(res.content)


def preview(filename):
    # https://help.aliyun.com/document_detail/74947.html?spm=a2c4g.11186623.2.22.335226c5dUnarR
    res = requests.get("https://preview.imm.aliyuncs.com/index.html", params={
        "url": "https://{}.{}.aliyuncs.com/{}/imm/vector".format(bucket, region, filename),
        "accessKeyId": access_key_id,
        "accessKeySecret": access_key_secret,
        "region": region,
        "bucket": bucket
    })
    print(urllib.parse.unquote(res.url))


def main():
    put_object("../asset/test.docx")
    convert("test.docx", "png")
    convert("test.docx", "jpg")
    convert("test.docx", "text")
    convert("test.docx", "pdf")
    convert("test.docx", "vector")
    preview("test.docx")


if __name__ == "__main__":
    main()
