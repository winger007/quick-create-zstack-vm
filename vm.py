#!/usr/bin/env python
# encoding: utf-8
from basic_api import *

def create_zone(session_uuid, zone_name):
    content = {"name" : zone_name}
    rsp = api_call(session_uuid, "org.zstack.header.zone.APICreateZoneMsg", content)
    error_if_fail(rsp)
    print "successfully create zone: %s" % zone_name
    return rsp['org.zstack.header.zone.APICreateZoneEvent']['inventory']['uuid']

#def query_zone(session_uuid):
#    rsp = api_call(session_uuid, "org.zstack.header.zone.APIQueryZoneMsg")
#    error_if_fail(rsp)
#    print rsp

def update_zone(session_uuid, zone_uuid, zone_name):
    content = {"uuid":zone_uuid, "name":zone_name}
    rsp = api_call(session_uuid, "org.zstack.header.zone.APIUpdateZoneMsg", content)
    error_if_fail(rsp)
    print "successfully update zone: %s" % zone_uuid

def delete_zone(session_uuid, zone_uuid):
    content = {"uuid" : zone_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.zone.APIDeleteZoneMsg", content)
    error_if_fail(rsp)
    print "successfully delete zone: %s" % zone_uuid


def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)

    print "successfully logout"


session_uuid = login()
zone_uuid = create_zone(session_uuid, "zone1")
#query_zone(session_uuid)
update_zone(session_uuid, zone_uuid, "zone2")
delete_zone(session_uuid, zone_uuid)
logout(session_uuid)