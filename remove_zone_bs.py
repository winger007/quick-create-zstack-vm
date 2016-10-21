#!/usr/bin/env python
# encoding: utf-8

from zone import *
from sftp_backup_storage import *
from instance_offering import *

if __name__ == '__main__':
    session_uuid = login()
    rsp_list = query_zone(session_uuid, [])
    for rsp in rsp_list['org.zstack.header.zone.APIQueryZoneReply']['inventories']:
        print rsp
        zone_uuid = rsp['uuid']
        delete_zone(session_uuid, zone_uuid)

    bs_list = query_backup_storage(session_uuid, [])
    for bs in bs_list['org.zstack.storage.backup.sftp.APIQuerySftpBackupStorageReply']['inventories']:
        print bs
        bs_uuid = bs['uuid']
        delete_backup_storage(session_uuid, bs_uuid)

    instance_offering_list =  query_instance_offering(session_uuid, [])
    for offering in instance_offering_list['org.zstack.header.configuration.APIQueryInstanceOfferingReply']['inventories']:
        print offering
        offering_uuid = offering['uuid']
        delete_instance_offering(session_uuid, offering_uuid)

