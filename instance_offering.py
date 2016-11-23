#!/usr/bin/env python
# encoding: utf-8
import sys, os
from basic_api import *

def create_instance_offering(session_uuid, name, cpu_number, cpu_speed, memory_size, system_tags = None):
    '''memory_size unit is bytes and the minimal size is 16MB'''
    if system_tags is not None:
        if type(system_tags) is not list:
            print "systemTags type should be a list like this: ['volumeTotalBandwidth::100000000', 'networkInboundBandwidth::100000000', 'networkOutboundBandwidth::100000000']"
            sys.exit(1)
        content = {"name" : name, "cpuNum": cpu_number, "cpuSpeed":cpu_speed, "memorySize":memory_size, "systemTags":system_tags }
    else:
        content = {"name" : name, "cpuNum": cpu_number, "cpuSpeed":cpu_speed, "memorySize":memory_size}
    rsp = api_call(session_uuid, "org.zstack.header.configuration.APICreateInstanceOfferingMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create instance offering: %s" % name
    return rsp['org.zstack.header.configuration.APICreateInstanceOfferingEvent']['inventory']['uuid']

def query_instance_offering(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.configuration.APIQueryInstanceOfferingMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query instance_offering"
    return rsp

def update_instance_offering(session_uuid, instance_offering_uuid, instance_offering_name):
    content = {"uuid":instance_offering_uuid, "name":instance_offering_name}
    rsp = api_call(session_uuid, "org.zstack.header.configuration.APIUpdateInstanceOfferingMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update instance_offering: %s" % instance_offering_uuid

def change_instance_offering(session_uuid, instance_offering_uuid, instance_uuid):
    '''this api test locate at vm.py'''
    content = {"instanceOfferingUuid":instance_offering_uuid, "vmInstanceUuid":instance_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.vm.APIChangeInstanceOfferingMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully change to instance_offering: %s" % instance_offering_uuid

def delete_instance_offering(session_uuid, instance_offering_uuid):
    content = {"uuid" : instance_offering_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.configuration.APIDeleteInstanceOfferingMsg",content)
    error_if_fail(rsp)
    print "\nsuccessfully delete instance_offering: %s" % instance_offering_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"

if __name__ == '__main__':
    session_uuid = login()
    instance_offering_uuid = create_instance_offering(session_uuid, "instance-offering1", 1, 1, 16*1024*1024)
    query_instance_offering(session_uuid, [])
    update_instance_offering(session_uuid, instance_offering_uuid, "instance_offering2")
    delete_instance_offering(session_uuid, instance_offering_uuid)
    system_tags = ['volumeTotalBandwidth::100000000', 'networkInboundBandwidth::100000000', 'networkOutboundBandwidth::100000000']
    instance_offering_uuid_with_tags = create_instance_offering(session_uuid, "instance-offering1", 1, 1, 16*1024*1024, system_tags)
    delete_instance_offering(session_uuid, instance_offering_uuid_with_tags)
    logout(session_uuid)