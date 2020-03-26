#!/usr/bin/env python3

import requests
import random
import util
import datetime

config = util.load_credential_from_local()
access_key_id = config["accessKeyID"]
access_key_secret = config["accessKeySecret"]
region_id = config["regionID"]
region = config["region"]

random.seed()


def put_project(proj):
    # https://help.aliyun.com/document_detail/63496.html?spm=a2c4g.11186623.6.590.50973185xj3uaK
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": "hatlonely-test-bucket",
        "Version": "2017-09-06",
        "Timestamp": datetime.datetime.utcnow().isoformat(),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": random.randint(0, 2**63-1),
        "Action": "PutProject",
        "BillingType": "ByUsage",  # ByUsage | ByCU
        "Type": "DocStarter",   # DocStarter | PhotoStarter | VideoStarter
    }
    params["Signature"] = util.signature("POST", params, access_key_secret)

    res = requests.post(
        "https://imm.{}.aliyuncs.com".format(region_id), params=params)
    print(res.text)


def get_project(proj):
    # https://help.aliyun.com/document_detail/63498.html?spm=a2c4g.11186623.6.591.20133185jVF6ul
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": "hatlonely-test-bucket",
        "Version": "2017-09-06",
        "Timestamp": datetime.datetime.utcnow().isoformat(),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": random.randint(0, 2**63-1),
        "Action": "GetProject",
    }
    params["Signature"] = util.signature("POST", params, access_key_secret)

    res = requests.post(
        "https://imm.{}.aliyuncs.com".format(region_id), params=params)
    print(res.text)


def del_project(proj):
    # https://help.aliyun.com/document_detail/63497.html?spm=a2c4g.11186623.6.592.16913185dB5ieF
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": "hatlonely-test-bucket",
        "Version": "2017-09-06",
        "Timestamp": datetime.datetime.utcnow().isoformat(),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": random.randint(0, 2**63-1),
        "Action": "DeleteProject",
    }
    params["Signature"] = util.signature("POST", params, access_key_secret)

    res = requests.post(
        "https://imm.{}.aliyuncs.com".format(region_id), params=params)
    print(res.text)


def list_project():
    # https://help.aliyun.com/document_detail/63905.html?spm=a2c4g.11186623.6.593.4e7e2b5ayHpqNx
    params = {
        "Project": "imm-proj-test",
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": "hatlonely-test-bucket",
        "Version": "2017-09-06",
        "Timestamp": datetime.datetime.utcnow().isoformat(),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": random.randint(0, 2**63-1),
        "Action": "ListProjects",
    }
    params["Signature"] = util.signature("POST", params, access_key_secret)

    res = requests.post(
        "https://imm.{}.aliyuncs.com".format(region_id), params=params)
    print(res.text)


def update_project(proj, new_cu):
    # https://help.aliyun.com/document_detail/92530.html?spm=a2c4g.11186623.6.594.1cb72ca9pocYey
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": "hatlonely-test-bucket",
        "Version": "2017-09-06",
        "Timestamp": datetime.datetime.utcnow().isoformat(),
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": random.randint(0, 2**63-1),
        "Action": "UpdateProject",
        "NewCU": new_cu,
    }
    params["Signature"] = util.signature("POST", params, access_key_secret)

    res = requests.post(
        "https://imm.{}.aliyuncs.com".format(region_id), params=params)
    print(res.text)


def main():
    put_project("imm-proj-test")
    update_project("imm-proj-test", 15)
    get_project("imm-proj-test")
    del_project("imm-proj-test")
    list_project()


if __name__ == "__main__":
    main()
