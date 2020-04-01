#!/usr/bin/env python3

import argparse
import util
import project
import os
import doc
import sts
import json


def main():
    parser = argparse.ArgumentParser(description="""imm client
    Example:
        python3 imm_client.py -a ListProjects -r hz
        python3 imm_client.py -a ListProjects -r hz -c ~/.ossutilconfig.immtest -e http://imm.hele.aliyuncs.com
    """)
    parser.add_argument("-c", "--config", help="config path", default=os.path.join(os.path.expanduser("~"), ".ossutilconfig"))
    parser.add_argument("-r", "--region", help="region")
    parser.add_argument("-i", "--access-key-id", help="access key id")
    parser.add_argument("-s", "--access-key-secret", help="access key secret")
    parser.add_argument("-a", "--action", help="action")
    parser.add_argument("-p", "--project", help="project")
    parser.add_argument("-b", "--bucket", help="bucket")
    parser.add_argument("-f", "--filename", help="filename")
    parser.add_argument("--src-type", help="src type")
    parser.add_argument("-t", "--tgt-type", help="target type")
    parser.add_argument("--role", help="role", default="test-ram-account")
    parser.add_argument("-u", "--uid", help="user id")
    parser.add_argument("-e", "--endpoint", help="endpoint")
    args = parser.parse_args()

    if args.config:
        config = util.load_credential_from_local(args.config)
        access_key_id = config["accessKeyID"]
        access_key_secret = config["accessKeySecret"]
        region_id = config["regionID"]
    if args.region == "hz":
        region_id = "cn-hangzhou"
    elif args.region == "sh":
        region_id = "cn-shanghai"
    elif args.region == "bj":
        region_id = "cn-beijing"
    region = "oss-" + region_id
    endpoint = "https://imm.{}.aliyuncs.com".format(region_id)
    sts_endpoint = "https://sts.aliyuncs.com"
    if args.endpoint:
        endpoint = args.endpoint

    if args.project:
        proj = args.project
    if args.bucket:
        bucket = args.bucket
    if args.filename:
        filename = args.filename
    src_type = args.src_type
    if args.tgt_type:
        tgt_type = args.tgt_type
    if args.access_key_id:
        access_key_id = args.access_key_id
    if args.access_key_secret:
        access_key_secret = args.access_key_secret
    if args.uid:
        uid = args.uid
    if args.role:
        role = args.role

    if args.action == "AssumeRole":
        print(json.dumps(sts.assume_role(sts_endpoint, access_key_id, access_key_secret, uid, role)))
        return

    security_token = ''
    if args.uid and args.role:
        res = sts.assume_role(sts_endpoint, access_key_id, access_key_secret, uid, role)
        print(json.dumps(res))
        access_key_id = res["Credentials"]["AccessKeyId"]
        access_key_secret = res["Credentials"]["AccessKeySecret"]
        security_token = res["Credentials"]["SecurityToken"]

    if args.action == "ListProjects":
        project.list_projects(endpoint, access_key_id, access_key_secret, security_token, region_id)
    elif args.action == "PutProject":
        project.put_project(endpoint, access_key_id, access_key_secret, security_token, proj, region_id)
    elif args.action == "GetProject":
        project.get_project(endpoint, access_key_id, access_key_secret, security_token, proj, region_id)
    elif args.action == "DelProject":
        project.del_project(endpoint, access_key_id, access_key_secret, security_token, proj, region_id)
    elif args.action == "ConvertOfficeFormat":
        doc.convert_office_format(endpoint, access_key_id, access_key_secret, proj, region_id, bucket, filename, src_type, tgt_type)
    elif args.action == "preview":
        doc.preview(access_key_id, access_key_secret, proj, region, bucket, filename)
    elif args.action == "GetOfficePreviewURL":
        doc.get_office_preview_url(endpoint, access_key_id, access_key_secret, proj, region_id, bucket, filename)

if __name__ == "__main__":
    main()
