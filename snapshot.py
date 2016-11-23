from vm import *

def create_volume_snapshot(session_uuid, volume_snapshot_name, volume_uuid):
    content = {"name":volume_snapshot_name , "volumeUuid":volume_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.volume.APICreateVolumeSnapshotMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create volume snapshot: %s" % volume_snapshot_name
    return rsp['org.zstack.header.volume.APICreateVolumeSnapshotEvent']['inventory']['uuid']

def update_volume_snapshot(session_uuid, volume_snapshot_name, volume_snapshot_uuid):
    content = {"uuid":volume_snapshot_uuid, "name":volume_snapshot_name}
    rsp = api_call(session_uuid, "org.zstack.header.storage.snapshot.APIUpdateVolumeSnapshotMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update volume snapshot: %s" % volume_snapshot_uuid

def query_volume_snapshot(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.storage.snapshot.APIQueryVolumeSnapshotMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query volume snapshot"

def delete_volume_snapshot(session_uuid, volume_snapshot_uuid):
    content = {"uuid" : volume_snapshot_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.storage.snapshot.APIDeleteVolumeSnapshotMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully delete volume snapshot: %s" % volume_snapshot_uuid

def revert_volume_from_snapshot(session_uuid, volume_snapshot_uuid):
    content = {"uuid" : volume_snapshot_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.storage.snapshot.APIRevertVolumeFromSnapshotMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully revert volume snapshot: %s" % volume_snapshot_uuid

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid,"zone1")
    cluster_uuid = create_cluster(session_uuid,zone_uuid,"cluster1","KVM")
    primary_storage_uuid = add_local_primary_storage(session_uuid, zone_uuid, '/ps', "test-ps")
    attach_primary_storage_to_cluster(session_uuid, cluster_uuid, primary_storage_uuid)
    host_uuid = add_host(session_uuid, cluster_uuid, "127.0.0.1","test-host", "root", "linux123", "22")
    backup_storage_uuids = []
    backup_storage_uuid = add_sftp_backup_storage(session_uuid,"/bs","sftp_bs","127.0.0.1","root","linux123")
    attach_backup_storage_to_zone(session_uuid, zone_uuid, backup_storage_uuid)
    backup_storage_uuids.append(backup_storage_uuid)
    image_uuid = add_image(session_uuid, backup_storage_uuids, "test-image", "file:///root/zstack-image-1.4.qcow2", "qcow2", "Linux")
    l2novlan_network_uuid = create_l2novlan_network(session_uuid,zone_uuid,"l2_no_vlan","eth0")
    attach_l2_network_to_cluster(session_uuid, cluster_uuid, l2novlan_network_uuid)
    l3_network_uuid = create_l3_network(session_uuid,l2novlan_network_uuid,"l3")

    service_provider = query_service_provider(session_uuid,[])
    network_service_uuid = service_provider['inventories'][2]['uuid']
    network_services= {network_service_uuid: ["Eip", "DHCP", "Userdata"]}
    attach_network_service_to_l3_network(session_uuid,l3_network_uuid,network_services)

    instance_offering_uuid = create_instance_offering(session_uuid, "instance_offering1", 1, 1, 128*1024*1024)
    l3_network_uuids = []
    l3_network_uuids.append(l3_network_uuid)
    add_ip_range(session_uuid, l3_network_uuid, "test-ip-range", "172.20.60.200", "172.20.60.210", "255.255.0.0", "172.20.0.1")
    vm_uuid = create_vm(session_uuid,"vm1", instance_offering_uuid, image_uuid, l3_network_uuids)
    query_vm(session_uuid, [])
    update_vm(session_uuid, vm_uuid, "vm2")
    volume_uuid = query_vm(session_uuid,[])['org.zstack.header.vm.APIQueryVmInstanceReply']['inventories'][0]['allVolumes'][0]['uuid']
    volume_snapshot_uuid = create_volume_snapshot(session_uuid, "vm2-snapshot", volume_uuid)
    update_volume_snapshot(session_uuid,"vm2-snapshot-2", volume_snapshot_uuid)
    query_volume_snapshot(session_uuid,[])
    stop_vm(session_uuid, vm_uuid)
    revert_volume_from_snapshot(session_uuid,volume_snapshot_uuid)
    delete_volume_snapshot(session_uuid,volume_snapshot_uuid)
    destroy_vm(session_uuid, vm_uuid)
    expunge_vm(session_uuid, vm_uuid)
    delete_image(session_uuid, image_uuid)
    delete_backup_storage(session_uuid, backup_storage_uuid)
    delete_zone(session_uuid, zone_uuid)
    logout(session_uuid)