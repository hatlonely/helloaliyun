#!/usr/bin/env python3

import util
import datetime
import random
import requests

def put_project(endpoint, access_key_id, access_key_secret, security_token, proj, region_id):
    # https://help.aliyun.com/document_detail/63496.html?spm=a2c4g.11186623.6.590.50973185xj3uaK
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Action": "PutProject",
        "BillingType": "ByUsage",  # ByUsage | ByCU
        "Type": "DocStarter",   # DocStarter | PhotoStarter | VideoStarter
    }
    if security_token:
        params["SecurityToken"] = security_token
    params = util.make_pop_params("POST", params, access_key_secret)

    res = requests.post(endpoint, params=params)
    print(res.text)

def list_projects(endpoint, access_key_id, access_key_secret, security_token, region_id):
    # https://help.aliyun.com/document_detail/63905.html?spm=a2c4g.11186623.6.593.4e7e2b5ayHpqNx
    params = {
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Action": "ListProjects",
    }
    if security_token:
        params["SecurityToken"] = security_token
    params = util.make_pop_params("POST", params, access_key_secret)

    res = requests.post(endpoint, params=params)
    print(res.text)

def get_project(endpoint, access_key_id, access_key_secret, security_token, proj, region_id):
    # https://help.aliyun.com/document_detail/63498.html?spm=a2c4g.11186623.6.591.20133185jVF6ul
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Action": "GetProject",
    }
    if security_token:
        params["SecurityToken"] = security_token
    params = util.make_pop_params("POST", params, access_key_secret)

    res = requests.post(endpoint, params=params)
    print(res.text)


def del_project(endpoint, access_key_id, access_key_secret, security_token, proj, region_id):
    # https://help.aliyun.com/document_detail/63497.html?spm=a2c4g.11186623.6.592.16913185dB5ieF
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Action": "DeleteProject",
    }
    if security_token:
        params["SecurityToken"] = security_token
    params = util.make_pop_params("POST", params, access_key_secret)

    res = requests.post(endpoint, params=params)
    print(res.text)
