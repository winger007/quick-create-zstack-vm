#!/usr/bin/env python
# encoding: utf-8
from cluster import *

def create_l2novlan_network(session_uuid, zone_uuid, name, physical_interface):
    content = {"name" : name, "zoneUuid": zone_uuid, "physicalInterface": physical_interface}
    rsp = api_call(session_uuid, "org.zstack.header.network.l2.APICreateL2NoVlanNetworkMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create l2novlan_network: %s" % name
    print rsp
    return rsp['org.zstack.header.network.l2.APICreateL2NetworkEvent']['inventory']['uuid']

def query_l2novlan_network(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.network.l2.APIQueryL2NetworkMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query l2 noVlanNetwork"
    return rsp

def attach_l2_network_to_cluster(session_uuid, cluster_uuid, l2_network_uuid):
    content = {"l2NetworkUuid" : l2_network_uuid, "clusterUuid": cluster_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.network.l2.APIAttachL2NetworkToClusterMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully attache l2 network: %s to cluster: %s" %  (l2_network_uuid, cluster_uuid)
    print rsp
    return rsp['org.zstack.header.network.l2.APIAttachL2NetworkToClusterEvent']['inventory']['uuid']

def update_l2novlan_network(session_uuid, l2novlan_network_uuid, l2novlan_network_name):
    content = {"uuid":l2novlan_network_uuid, "name":l2novlan_network_name}
    rsp = api_call(session_uuid, "org.zstack.header.network.l2.APIUpdateL2NetworkMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update l2novlan_network: %s" % l2novlan_network_uuid

def delete_l2novlan_network(session_uuid, l3novlan_network_uuid):
    content = {"uuid" : l2novlan_network_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.network.l2.APIDeleteL2NetworkMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete l2novlan_network: %s" % l2novlan_network_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, 'zone1')
    l2novlan_network_uuid = create_l2novlan_network(session_uuid, zone_uuid, "l2novlan_network1", "eth0")
    query_l2novlan_network(session_uuid,[])
    update_l2novlan_network(session_uuid, l2novlan_network_uuid, "l2novlan_network2")
    delete_l2novlan_network(session_uuid, l2novlan_network_uuid)
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)