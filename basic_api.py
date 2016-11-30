#!/usr/bin/env python
# encoding: utf-8

import httplib
import json
import time
import hashlib

# return a dict containing API return value
def api_call(session_uuid, api_id, api_content):
    conn = httplib.HTTPConnection("localhost", 8080)
    headers = {"Content-Type": "application/json"}

    if session_uuid:
        api_content["session"] = {"uuid": session_uuid}

    api_body = {api_id: api_content}

    conn.request("POST", "/zstack/api", json.dumps(api_body))
    response = conn.getresponse()

    if response.status != 200:
        raise Exception("failed to make an API call, %s, %s" % (response.status, response.reason))

    rsp_body = response.read()
    print rsp_body

    rsp = json.loads(rsp_body)

    if rsp["state"] == "Done":
        print json.loads(rsp["result"])
        return json.loads(rsp["result"])

    job_uuid = rsp["uuid"]
    def query_until_done():
        conn.request("GET", "/zstack/api/result/%s" % job_uuid)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("failed to query API result, %s, %s" % (response.status, response.reason))

        rsp_body = response.read()
        rsp = json.loads(rsp_body)
        if rsp["state"] == "Done":
            print json.loads(rsp["result"])
            return json.loads(rsp["result"])

        time.sleep(1)
        print "Job[uuid:%s] is still in processing" % job_uuid
        return query_until_done()

    return query_until_done()



def error_if_fail(rsp):
    success = rsp.values()[0]["success"]
    if not success:
        error = rsp.values()[0]["error"]
        raise Exception("failed to login, %s" % json.dumps(error))

def login(account_name='admin', password='password'):

    sha512_password = hashlib.sha512(password).hexdigest()
    print sha512_password
    content = {
            "accountName": account_name,
            "password":  sha512_password
    }
    rsp = api_call(None, "org.zstack.header.identity.APILogInByAccountMsg", content)
    error_if_fail(rsp)

    session_uuid = rsp.values()[0]["inventory"]["uuid"]

    print "\nsuccessfully login, session uuid is: %s" % session_uuid
    return session_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"