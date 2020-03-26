#!/usr/bin/env python3

import requests
import datetime
import random
import util
import urllib

config = util.load_credential_from_local()
access_key_id = config["accessKeyID"]
access_key_secret = config["accessKeySecret"]
region_id = config["regionID"]
region = config["region"]


def preview():
    # https://help.aliyun.com/document_detail/74947.html?spm=a2c4g.11186623.2.22.335226c5dUnarR
    res = requests.get("https://preview.imm.aliyuncs.com/index.html", params={
        "url": "https://hatlonely-test-bucket.{}.aliyuncs.com/hello.docx/imm".format(region),
        "accessKeyId": access_key_id,
        "accessKeySecret": access_key_secret,
        "region": region,
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
        "RegionId": region_id,
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
    params["Signature"] = util.signature("POST", params, access_key_secret)

    res = requests.post(
        "https://imm.{}.aliyuncs.com".format(region_id), params=params)
    print(res)
    print(res.content)


def main():
    convert()
    preview()


if __name__ == "__main__":
    main()
