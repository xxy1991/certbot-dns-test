#!/usr/bin/env python3
# coding:utf-8

import sys
import getopt
import json

import tldextract
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest


class AliyunDNSClient:
    def __init__(self, access_key_id, access_key_secret, domain):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.client = AcsClient(self.access_key_id, self.access_key_secret)
        self.domain = domain

    # 显示所有记录
    def describe_domain_records(self):
        """
        最多只能查询此域名的 500条解析记录
        PageNumber  当前页数，起始值为1，默认为1
        PageSize  分页查询时设置的每页行数，最大值500，默认为20
        :return:
        """
        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')

        request.set_DomainName(self.domain)

        response = self.client.do_action_with_exception(request)
        return json.loads(str(response, encoding='utf-8'))

    # 增加解析记录
    def add_domain_record(self, rr, rs_type, value):
        request = AddDomainRecordRequest()
        request.set_accept_format('json')

        request.set_DomainName(self.domain)
        request.set_RR(rr)
        request.set_Type(rs_type)
        request.set_Value(value)

        response = self.client.do_action_with_exception(request)
        return json.loads(str(response, encoding='utf-8'))

    # 修改解析记录
    def update_domain_record(self, record_id, rr, rs_type, value):
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(record_id)
        request.set_RR(rr)
        request.set_Type(rs_type)
        request.set_Value(value)

        response = self.client.do_action_with_exception(request)
        return json.loads(str(response, encoding='utf-8'))

    # 删除解析记录
    def delete_domain_record(self, record_id):
        request = DeleteDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(record_id)

        response = self.client.do_action_with_exception(request)
        return json.loads(str(response, encoding='utf-8'))


if __name__ == "__main__":
    ACCESS_KEY_ID = ''
    ACCESS_KEY_SECRET = ''
    ACTION = ''
    CERTBOT_DOMAIN = ''
    CERTBOT_VALIDATION = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hk:s:a:d:c:", [
            "help", "key=", "secret=", "action=", "domain=", "code="])
    except getopt.GetoptError:
        print('alydns.py -k <key> -s <secret> -a <action> -d <domain> -c <code>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('alydns.py -k <key> -s <secret> -a <action> -d <domain> -c <code>')
            sys.exit()
        elif opt in ("-k", "--key"):
            ACCESS_KEY_ID = arg
        elif opt in ("-s", "--secret"):
            ACCESS_KEY_SECRET = arg
        elif opt in ("-a", "--action"):
            ACTION = arg
        elif opt in ("-d", "--domain"):
            CERTBOT_DOMAIN = arg
        elif opt in ("-c", "--code"):
            CERTBOT_VALIDATION = arg

    print("域名 API 调用开始")
    domain_full = tldextract.extract(CERTBOT_DOMAIN)
    alyDns = AliyunDNSClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, domain_full.registered_domain)

    acme_challenge = "_acme-challenge"
    if domain_full.subdomain == "":
        record = acme_challenge
    else:
        record = acme_challenge + '.' + domain_full.subdomain

    if ACTION == "add":
        result = (alyDns.add_domain_record(
            record, "TXT", CERTBOT_VALIDATION))
        if "Code" in result:
            print("AlyDNS 域名增加失败-" +
                  result["Code"] + ":" + result["Message"])
            sys.exit(0)
    elif ACTION == "clean":
        data = alyDns.describe_domain_records()
        if "Code" in data:
            print("AlyDNS 域名删除失败-" +
                  data["Code"] + ":" + data["Message"])
            sys.exit(0)
        record_list = data["DomainRecords"]["Record"]
        if record_list:
            for item in record_list:
                if item['RR'] == record:
                    alyDns.delete_domain_record(item['RecordId'])
    print("域名 API 调用结束")
