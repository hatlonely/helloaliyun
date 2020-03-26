#!/usr/bin/env python3

import os
import configparser
import urllib.parse
import hmac
import base64
import unittest


def load_credential_from_local():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser("~"), ".ossutilconfig"))
    access_key_id = config["Credentials"]["accessKeyID"]
    access_key_secret = config["Credentials"]["accessKeySecret"]
    return {
        "access_key_id": config["Credentials"]["accessKeyID"],
        "access_key_secret": config["Credentials"]["accessKeySecret"],
        "endpoint": config["Credentials"]["endpoint"],
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
