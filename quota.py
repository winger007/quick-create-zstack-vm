#!/usr/bin/env python
# encoding: utf-8
from basic_api import *

def query_account(session_uuid, account_name):
    content = {}
    content['conditions'] = [{"name": "name", "value": account_name, "op": "="}]
    rsp = api_call(session_uuid, "org.zstack.header.identity.APIQueryAccountMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully query account: %s" % account_name
    return rsp['org.zstack.header.identity.APIQueryAccountReply']['inventories'][0]['uuid']


def query_quota_by_account(session_uuid, account_uuid):
    content = {"uuid" : account_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.identity.APIGetAccountQuotaUsageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully query quota by account: %s" % account_uuid
    return rsp['org.zstack.header.identity.APIGetAccountQuotaUsageReply']['usages']

if __name__ == '__main__':
    session_uuid = login()
    account_uuid = query_account(session_uuid, "admin")
    query_quota_by_account(session_uuid, account_uuid)
    logout(session_uuid)
