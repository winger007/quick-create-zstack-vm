#!/usr/bin/env python
# encoding: utf-8

from zone import *
from vm import *

if __name__ == '__main__':
    session_uuid = login(account_name='admin',password='password')
    rsp_list = query_zone(session_uuid, [])
    for rsp in rsp_list['org.zstack.header.zone.APIQueryZoneReply']['inventories']:
        print rsp
        zone_uuid = rsp['uuid']
        delete_zone(session_uuid, zone_uuid)

    bs_list = query_backup_storage(session_uuid, [])
    print bs_list
    if len(bs_list['org.zstack.header.storage.backup.APIQueryBackupStorageReply']['inventories']) != 0:
        for bs in bs_list['org.zstack.header.storage.backup.APIQueryBackupStorageReply']['inventories']:
            print bs
            bs_uuid = bs['uuid']
            delete_backup_storage(session_uuid, bs_uuid)

    instance_offering_list =  query_instance_offering(session_uuid, [])
    for offering in instance_offering_list['org.zstack.header.configuration.APIQueryInstanceOfferingReply']['inventories']:
        print offering
        offering_uuid = offering['uuid']
        delete_instance_offering(session_uuid, offering_uuid)

    instance_list = query_vm(session_uuid, [])
    for vm in instance_list['org.zstack.header.vm.APIQueryVmInstanceReply']['inventories']:
        print vm
        vm_uuid = vm['uuid']
        expunge_vm(session_uuid,vm_uuid)

