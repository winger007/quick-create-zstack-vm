#!/usr/bin/env python
# encoding: utf-8
from cluster import *

def add_sftp_backup_storage(session_uuid, url, name, hostname, username, password):
    content = {"name":name,  "url":url, "hostname":hostname, "username":username, "password":password}
    rsp = api_call(session_uuid, "org.zstack.storage.backup.sftp.APIAddSftpBackupStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully add backup_storage: %s" % name
    return rsp['org.zstack.header.storage.backup.APIAddBackupStorageEvent']['inventory']['uuid']

def add_imagestore_backup_storage(session_uuid, url, name, hostname, username, password):
    content = {"name":name,  "url":url, "hostname":hostname, "username":username, "password":password}
    rsp = api_call(session_uuid, "org.zstack.storage.backup.imagestore.APIAddImageStoreBackupStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully add backup_storage: %s" % name
    return rsp['org.zstack.header.storage.backup.APIAddBackupStorageEvent']['inventory']['uuid']


def query_backup_storage(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.storage.backup.APIQueryBackupStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully query backup storage"
    print rsp
    return rsp

def attach_backup_storage_to_zone(session_uuid, zone_uuid, backup_storage_uuid):
    content = {"zoneUuid":zone_uuid, "backupStorageUuid":backup_storage_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.storage.backup.APIAttachBackupStorageToZoneMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully attach backup storage %s to %s" % (backup_storage_uuid, zone_uuid)
    return rsp

def update_backup_storage(session_uuid, backup_storage_uuid, backup_storage_name):
    content = {"uuid":backup_storage_uuid, "name":backup_storage_name}
    rsp = api_call(session_uuid, "org.zstack.storage.backup.sftp.APIUpdateSftpBackupStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update backup_storage: %s" % backup_storage_uuid

def delete_backup_storage(session_uuid, backup_storage_uuid):
    content = {"uuid" : backup_storage_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.storage.backup.APIDeleteBackupStorageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete backup_storage: %s" % backup_storage_uuid

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, 'zone1')
    cluster_uuid = create_cluster(session_uuid, zone_uuid, 'cluster1', 'KVM')
    #backup_storage_uuid = add_sftp_backup_storage(session_uuid,'/bs', 'test-bs', "127.0.0.1", 'root', 'linux123')
    backup_storage_uuid = add_imagestore_backup_storage(session_uuid,'/bs', 'test-bs', "127.0.0.1", 'root', 'linux123')
    query_backup_storage(session_uuid, [])
    update_backup_storage(session_uuid, backup_storage_uuid, "backup_storage2")
    delete_backup_storage(session_uuid, backup_storage_uuid)
    delete_cluster(session_uuid, cluster_uuid)
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)
