#!/usr/bin/env python
# encoding: utf-8
from basic_api import *

def create_zone(session_uuid, zone_name):
    content = {"name" : zone_name}
    rsp = api_call(session_uuid, "org.zstack.header.zone.APICreateZoneMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create zone: %s" % zone_name
    return rsp['org.zstack.header.zone.APICreateZoneEvent']['inventory']['uuid']

def update_zone(session_uuid, zone_uuid, zone_name):
    content = {"uuid":zone_uuid, "name":zone_name}
    rsp = api_call(session_uuid, "org.zstack.header.zone.APIUpdateZoneMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update zone: %s" % zone_uuid

def query_zone(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.zone.APIQueryZoneMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully query zone"
    print rsp
    return rsp

def delete_zone(session_uuid, zone_uuid):
    content = {"uuid" : zone_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.zone.APIDeleteZoneMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete zone: %s" % zone_uuid


if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, "zone1")
    query_zone(session_uuid, [])
    update_zone(session_uuid, zone_uuid, "zone2")
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)
