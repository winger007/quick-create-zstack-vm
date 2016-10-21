#!/usr/bin/env python
# encoding: utf-8
from sftp_backup_storage import *

def add_image(session_uuid, backup_storage_uuids, name, url, format, platform ):
    content = {"name":name, "url":url, "format":format, "platform":platform, "backupStorageUuids":backup_storage_uuids}
    rsp = api_call(session_uuid, "org.zstack.header.image.APIAddImageMsg", content)
    print rsp
    error_if_fail(rsp)
    print "\nsuccessfully add image: %s" % name
    return rsp['org.zstack.header.image.APIAddImageEvent']['inventory']['uuid']

def query_image(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.image.APIQueryImageMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query image"
    return rsp

def update_image(session_uuid, image_uuid, image_name):
    content = {"uuid":image_uuid, "name":image_name}
    rsp = api_call(session_uuid, "org.zstack.header.image.APIUpdateImageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update image: %s" % image_uuid

def delete_image(session_uuid, image_uuid):
    content = {"uuid" : image_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.image.APIDeleteImageMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete image: %s" % image_uuid

def logout(session_uuid):
    content = {"sessionUuid": session_uuid}
    rsp = api_call(None, "org.zstack.header.identity.APILogOutMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully logout"

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid, 'zone1')
    cluster_uuid = create_cluster(session_uuid, zone_uuid, 'cluster1', 'KVM')
    backup_storage_uuids = []
    backup_storage_uuid = add_sftp_backup_storage(session_uuid,"/bs","bs-test","127.0.0.1","root","linux123")
    backup_storage_uuids.append(backup_storage_uuid)

    image_uuid = add_image(session_uuid, backup_storage_uuids, "test-image", "file:///root/zstack-image-1.4.qcow2", "qcow2", "Linux")
    query_image(session_uuid, [])
    update_image(session_uuid, image_uuid, "image2")
    delete_image(session_uuid, image_uuid)
    delete_backup_storage(session_uuid, backup_storage_uuid)
    delete_cluster(session_uuid, cluster_uuid)
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)