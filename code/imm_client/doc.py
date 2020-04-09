#!/usr/bin/env python3

import requests
import util
import random
import datetime
import urllib

def convert_office_format(endpoint, access_key_id, access_key_secret, proj, region_id, bucket, filename, srcType, tgtType):
    params = {
        "Project": "ossdocdefault",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": bucket,
        "Action": "ConvertOfficeFormat",
        "SrcUri": "oss://{}/{}".format(bucket, filename),
        "TgtType": tgtType,  # vector | jpg | png | pdf | text
        "TgtUri": "oss://{}/{}/imm/{}".format(bucket, filename, tgtType),
    }
    if srcType:
        params["srcType"] = srcType
    params = util.make_pop_params("POST", params, access_key_secret)

    res = requests.post(endpoint, params=params)
    print(res.text)


def preview(access_key_id, access_key_secret, proj, region, bucket, filename, sts_token):
    # https://help.aliyun.com/document_detail/74947.html?spm=a2c4g.11186623.2.22.335226c5dUnarR
    params={
        "url": "https://{}.{}.aliyuncs.com/{}/imm/vector".format(bucket, region, filename),
        "accessKeyId": access_key_id,
        "accessKeySecret": access_key_secret,
        "region": region,
        "bucket": bucket
    }
    if sts_token:
        params["stsToken"] = urllib.parse.quote(sts_token)
    res = requests.get("https://preview.imm.aliyuncs.com/index.html", params=params)
    print(urllib.parse.unquote(res.url))


def get_office_preview_url(endpoint, access_key_id, access_key_secret, proj, region_id, bucket, filename):
    # https://help.aliyun.com/document_detail/151008.html?spm=a2c4g.11186623.6.565.438961e3tw4LHs
    params = {
        "Project": proj,
        "Format": "JSON",
        "AccessKeyId": access_key_id,
        "RegionId": region_id,
        "Bucket": bucket,
        "Action": "GetOfficePreviewURL",
        "SrcUri": "oss://{}/{}".format(bucket, filename),
    }
    params = util.make_pop_params("POST", params, access_key_secret)

    res = requests.post(endpoint, params=params)
    print(res.text)
