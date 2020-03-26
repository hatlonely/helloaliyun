#!/usr/bin/env python3

import os
import configparser
import urllib.parse
import hmac
import base64
import unittest

region_to_endpoint = {
    "oss-cn-hangzhou": "oss-cn-hangzhou.aliyuncs.com",
    "oss-cn-shanghai": "oss-cn-shanghai.aliyuncs.com",
    "oss-cn-qingdao": "oss-cn-qingdao.aliyuncs.com",
    "oss-cn-beijing": "oss-cn-beijing.aliyuncs.com",
    "oss-cn-zhangjiakou": "oss-cn-zhangjiakou.aliyuncs.com",
    "oss-cn-huhehaote": "oss-cn-huhehaote.aliyuncs.com",
    "oss-cn-shenzhen": "oss-cn-shenzhen.aliyuncs.com",
    "oss-cn-heyuan": "oss-cn-heyuan.aliyuncs.com",
    "oss-cn-chengdu": "oss-cn-chengdu.aliyuncs.com",
    "oss-cn-hongkong": "oss-cn-hongkong.aliyuncs.com",
    "oss-us-west-1": "oss-us-west-1.aliyuncs.com",
    "oss-us-east-1": "oss-us-east-1.aliyuncs.com",
    "oss-ap-southeast-1": "oss-ap-southeast-1.aliyuncs.com",
    "oss-ap-southeast-2": "oss-ap-southeast-2.aliyuncs.com",
    "oss-ap-southeast-3": "oss-ap-southeast-3.aliyuncs.com",
    "oss-ap-southeast-5": "oss-ap-southeast-5.aliyuncs.com",
    "oss-ap-northeast-1": "oss-ap-northeast-1.aliyuncs.com",
    "oss-ap-south-1": "oss-ap-south-1.aliyuncs.com",
    "oss-eu-central-1": "oss-eu-central-1.aliyuncs.com",
    "oss-eu-west-1": "oss-eu-west-1.aliyuncs.com",
    "oss-me-east-1": "oss-me-east-1.aliyuncs.com",
}


def endpoint_to_region(endpoint):
    for region in region_to_endpoint:
        if endpoint == region_to_endpoint[region]:
            return region
    return None


def load_credential_from_local():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser("~"), ".ossutilconfig"))
    return {
        "accessKeyID": config["Credentials"]["accessKeyID"],
        "accessKeySecret": config["Credentials"]["accessKeySecret"],
        "endpoint": config["Credentials"]["endpoint"],
        "region": endpoint_to_region(config["Credentials"]["endpoint"]),
        "regionID": endpoint_to_region(config["Credentials"]["endpoint"])[4:],
    }


def encode(message):
    return urllib.parse.quote(str(message), safe='', encoding="utf-8").replace("+", "%20").replace("*", "%2A").replace("%7E", "~")


def signature(methods, params, access_key_secret):
    kvs = "&".join(["{}={}".format(encode(i), encode(params[i]))
                    for i in sorted(params)])
    to_sign = methods + "&" + encode("/") + "&" + "" + encode(kvs)
    return base64.b64encode(hmac.new((access_key_secret + '&').encode(), to_sign.encode(), digestmod='sha1').digest()).decode()


class TestUtil(unittest.TestCase):
    def test_signature(self):
        self.assertEqual(
            signature("POST", {
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
            }, "testsecret"),
            "NPzJnV5HAdj4jkShTWKa9WwOZxU="
        )


if __name__ == '__main__':
    unittest.main()
