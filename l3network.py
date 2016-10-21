#!/usr/bin/env python
# encoding: utf-8
from l2network import *

def create_l3_network(session_uuid, l2_network_uuid, name):
    content = {"name":name, "l2NetworkUuid":l2_network_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.network.l3.APICreateL3NetworkMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create l3_network: %s" % name
    print rsp
    return rsp['org.zstack.header.network.l3.APICreateL3NetworkEvent']['inventory']['uuid']

def add_ip_range(session_uuid, l3_network_uuid, name, start_ip, end_ip, netmask, gateway):
    content = {"name":name, "l3NetworkUuid": l3_network_uuid, "startIp":start_ip, "endIp":end_ip, "netmask":netmask, "gateway":gateway}
    rsp = api_call(session_uuid, "org.zstack.header.network.l3.APIAddIpRangeMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create ip range from %s to %s " %  (start_ip, end_ip)
    return rsp['org.zstack.header.network.l3.APIAddIpRangeEvent']['inventory']['uuid']

def query_l3_network(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.network.l3.APIQueryL3NetworkMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query l3 network"
    return rsp

def attach_network_service_to_l3_network(session_uuid, l3_network_uuid, network_services):
    content = {"l3NetworkUuid":l3_network_uuid, "networkServices": network_services}
    rsp = api_call(session_uuid, "org.zstack.header.network.service.APIAttachNetworkServiceToL3NetworkMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create l3_network: %s" %  l3_network_uuid
    print rsp
    return rsp['org.zstack.header.network.service.APIAttachNetworkServiceToL3NetworkEvent']['inventory']['uuid']

def query_service_provider(session_uuid,conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.network.service.APIQueryNetworkServiceProviderMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully query service provider"
    print rsp['org.zstack.header.network.service.APIQueryNetworkServiceProviderReply']
    return rsp['org.zstack.header.network.service.APIQueryNetworkServiceProviderReply']


def update_l3_network(session_uuid, l3_network_uuid, l3_network_name):
    content = {"uuid":l3_network_uuid, "name":l3_network_name}
    rsp = api_call(session_uuid, "org.zstack.header.network.l3.APIUpdateL3NetworkMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update l3_network: %s" % l3_network_uuid

def delete_l3_network(session_uuid, l3novlan_network_uuid):
    content = {"uuid" : l3_network_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.network.l3.APIDeleteL3NetworkMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete l3_network: %s" % l3_network_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, 'zone1')
    l2novlan_network_uuid = create_l2novlan_network(session_uuid,zone_uuid,"test-l2","eth0")
    l3_network_uuid = create_l3_network(session_uuid, l2novlan_network_uuid, "l3_network1")
    query_l3_network(session_uuid, [])
    update_l3_network(session_uuid, l3_network_uuid, "l3_network2")
    add_ip_range(session_uuid, l3_network_uuid, "test-ip-range", "172.20.60.200", "172.20.60.210", "255.255.0.0", "172.20.0.1")
    service_provider = query_service_provider(session_uuid,[])
    network_service_uuid = service_provider['inventories'][1]['uuid']
    network_services= {network_service_uuid: ["Eip", "DHCP", "Userdata"]}
    attach_network_service_to_l3_network(session_uuid,l3_network_uuid,network_services)
    delete_l3_network(session_uuid, l3_network_uuid)
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)