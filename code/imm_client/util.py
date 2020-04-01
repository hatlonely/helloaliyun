#!/usr/bin/env python3

import os
import configparser
import urllib.parse
import hmac
import base64
import unittest
import datetime
import random

def load_credential_from_local(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        "accessKeyID": config["Credentials"]["accessKeyID"],
        "accessKeySecret": config["Credentials"]["accessKeySecret"],
        "endpoint": config["Credentials"]["endpoint"],
        "region": config["Credentials"]["endpoint"].split(".")[0],
        "regionID": config["Credentials"]["endpoint"].split(".")[0][4:],
    }


def encode(message):
    return urllib.parse.quote(str(message), safe='', encoding="utf-8").replace("+", "%20").replace("*", "%2A").replace("%7E", "~")


def signature(methods, params, access_key_secret):
    kvs = "&".join([
        "{}={}".format(encode(i), encode(params[i])) for i in sorted(params)
    ])
    to_sign = methods + "&" + encode("/") + "&" + "" + encode(kvs)
    return base64.b64encode(hmac.new((access_key_secret + '&').encode(), to_sign.encode(), digestmod='sha1').digest()).decode()


def make_pop_params(methods, params, access_key_secret):
    if "Version" not in params:
        params["Version"] = "2017-09-06"
    if "Timestamp" not in params:
        params["Timestamp"] = datetime.datetime.utcnow().isoformat()
    if "SignatureMethod" not in params: 
        params["SignatureMethod"] = "HMAC-SHA1"
    if "SignatureVersion" not in params:
        params["SignatureVersion"] = "1.0"
    if "SignatureNonce" not in params:
        params["SignatureNonce"] = random.randint(0, 2**63-1)
    params["Signature"] = signature(methods, params, access_key_secret)
    return params


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
