#!/usr/bin/env python
# encoding: utf-8
from zone import *

def create_cluster(session_uuid, zone_uuid, cluster_name, hypervisor_type):
    content = {"name" : cluster_name, "zoneUuid": zone_uuid, "hypervisorType": hypervisor_type}
    rsp = api_call(session_uuid, "org.zstack.header.cluster.APICreateClusterMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create cluster: %s" % cluster_name
    return rsp['org.zstack.header.cluster.APICreateClusterEvent']['inventory']['uuid']

def query_cluster(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.cluster.APIQueryClusterMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query zone"
    return rsp

def update_cluster(session_uuid, cluster_uuid, cluster_name):
    content = {"uuid":cluster_uuid, "name":cluster_name}
    rsp = api_call(session_uuid, "org.zstack.header.cluster.APIUpdateClusterMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update cluster: %s" % cluster_uuid

def delete_cluster(session_uuid, cluster_uuid):
    content = {"uuid" : cluster_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.cluster.APIDeleteClusterMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete cluster: %s" % cluster_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, 'zone1')
    cluster_uuid = create_cluster(session_uuid, zone_uuid, "cluster1", "KVM")
    query_cluster(session_uuid, [])
    update_cluster(session_uuid, cluster_uuid, "cluster2")
    delete_cluster(session_uuid, cluster_uuid)
    logout(session_uuid)