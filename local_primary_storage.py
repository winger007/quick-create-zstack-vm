#!/usr/bin/env python
# encoding: utf-8
from cluster import *

def add_local_primary_storage(session_uuid, zone_uuid, mount_url, primary_storage_name):
    content = {"name" : primary_storage_name,  "zoneUuid":zone_uuid, "url":mount_url}
    rsp = api_call(session_uuid, "org.zstack.storage.primary.local.APIAddLocalPrimaryStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully add primary_storage: %s" % primary_storage_name
    return rsp['org.zstack.header.storage.primary.APIAddPrimaryStorageEvent']['inventory']['uuid']

def query_primary_storage(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.storage.primary.APIQueryPrimaryStorageMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query primary storage"
    return rsp

def update_primary_storage(session_uuid, primary_storage_uuid, primary_storage_name):
    content = {"uuid":primary_storage_uuid, "name":primary_storage_name}
    rsp = api_call(session_uuid, "org.zstack.header.storage.primary.APIUpdatePrimaryStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update primary_storage: %s" % primary_storage_uuid

def attach_primary_storage_to_cluster(session_uuid, cluster_uuid, primary_storage_uuid):
    content = {"clusterUuid":cluster_uuid, "primaryStorageUuid":primary_storage_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.storage.primary.APIAttachPrimaryStorageToClusterMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully attach primary_storage: %s to cluster: %s" % (primary_storage_uuid, cluster_uuid)

def delete_primary_storage(session_uuid, primary_storage_uuid):
    content = {"uuid" : primary_storage_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.storage.primary.APIDeletePrimaryStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete primary_storage: %s" % primary_storage_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, 'zone1')
    cluster_uuid = create_cluster(session_uuid, zone_uuid, 'cluster1', 'KVM')
    primary_storage_uuid = add_local_primary_storage(session_uuid, zone_uuid, '/ps', "test-ps")
    #query_primary_storage(session_uuid)
    update_primary_storage(session_uuid, primary_storage_uuid, "primary_storage2")
    delete_primary_storage(session_uuid, primary_storage_uuid)
    delete_cluster(session_uuid, cluster_uuid)
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)

def update_primary_storage(session_uuid, primary_storage_uuid, primary_storage_name):
    content = {"uuid":primary_storage_uuid, "name":primary_storage_name}
    rsp = api_call(session_uuid, "org.zstack.header.storage.primary.APIUpdatePrimaryStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update primary_storage: %s" % primary_storage_uuid

def delete_primary_storage(session_uuid, primary_storage_uuid):
    content = {"uuid" : primary_storage_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.storage.primary.APIDeletePrimaryStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete primary_storage: %s" % primary_storage_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, 'zone1')
    cluster_uuid = create_cluster(session_uuid, zone_uuid, 'cluster1', 'KVM')
    primary_storage_uuid = add_local_primary_storage(session_uuid, zone_uuid, '/ps', "test-ps")
    query_primary_storage(session_uuid, [])
    update_primary_storage(session_uuid, primary_storage_uuid, "primary_storage2")
    delete_primary_storage(session_uuid, primary_storage_uuid)
    delete_cluster(session_uuid, cluster_uuid)
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)