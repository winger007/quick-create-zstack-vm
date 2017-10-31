#!/usr/bin/env python
# encoding: utf-8
from instance_offering import *
from l3network import *
from image import *
from host import *
from local_primary_storage import *
import os


image_path = "file:///opt/zstack-dvd/zstack-image-1.4.qcow2"
#add host will add local host as compute node
host_ip = os.system("ip a | grep \"inet \" | grep -v 127 | awk -F \" \" '{print $2}' | awk -F \"/\" '{print $1}'")
l3_start_ip = "192.168.0.100" 
l3_end_ip = "192.168.0.200"
l3_net_mask = "255.255.255.0"
l3_gw_ip = "192.168.0.1"

if host_ip is None:
        print "host ip %s is illeage" % host_ip
        sys.exit(1)

def create_vm(session_uuid, vm_name, instance_offering_uuid, image_uuid, l3_network_uuids):
    content = {"name" : vm_name, "instanceOfferingUuid":instance_offering_uuid, "imageUuid":image_uuid,
               "l3NetworkUuids":l3_network_uuids}
    rsp = api_call(session_uuid, "org.zstack.header.vm.APICreateVmInstanceMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully create vm: %s" % vm_name
    return rsp['org.zstack.header.vm.APICreateVmInstanceEvent']['inventory']['uuid']

def query_vm(session_uuid, conditions):
    content = {'conditions':conditions}
    rsp = api_call(session_uuid, "org.zstack.header.vm.APIQueryVmInstanceMsg", content)
    error_if_fail(rsp)
    print rsp
    print "\nsuccessfully query vm"
    return rsp

def update_vm(session_uuid, vm_uuid, vm_name):
    content = {"uuid":vm_uuid, "name":vm_name}
    rsp = api_call(session_uuid, "org.zstack.header.vm.APIUpdateVmInstanceMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully update vm: %s" % vm_uuid

def stop_vm(session_uuid, vm_uuid):
    content = {"uuid":vm_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.vm.APIStopVmInstanceMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully stop vm: %s" % vm_uuid

def destroy_vm(session_uuid, vm_uuid):
    content = {"uuid" : vm_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.vm.APIDestroyVmInstanceMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully destroy vm: %s" % vm_uuid

def expunge_vm(session_uuid, vm_uuid):
    content = {"uuid" : vm_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.vm.APIExpungeVmInstanceMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully expunge vm: %s" % vm_uuid

def get_console_access(session_uuid, vm_uuid):
    content = {"vmInstanceUuid": vm_uuid}
    rsp = api_call(session_uuid, "org.zstack.header.console.APIRequestConsoleAccessMsg", content)
    error_if_fail(rsp)
    print "\nsuccessfully get vm console access info: %s" % vm_uuid

if __name__ == '__main__':
    session_uuid = login()
    zone_uuid = create_zone(session_uuid,"zone1")
    cluster_uuid = create_cluster(session_uuid,zone_uuid,"cluster1","KVM")
    primary_storage_uuid = add_local_primary_storage(session_uuid, zone_uuid, '/ps', "test-ps")
    attach_primary_storage_to_cluster(session_uuid, cluster_uuid, primary_storage_uuid)
    host_uuid = add_host(session_uuid, cluster_uuid, host_ip,"test-host", "root", "password", "22")
    backup_storage_uuids = []
    backup_storage_uuid = add_imagestore_backup_storage(session_uuid,"/bs","imagestore_bs",host_ip,"root","password")
    attach_backup_storage_to_zone(session_uuid, zone_uuid, backup_storage_uuid)
    backup_storage_uuids.append(backup_storage_uuid)
    image_uuid = add_image(session_uuid, backup_storage_uuids, "test-image", image_path, "qcow2", "Linux")
    l2novlan_network_uuid = create_l2novlan_network(session_uuid,zone_uuid,"l2_no_vlan","eth0")
    attach_l2_network_to_cluster(session_uuid, cluster_uuid, l2novlan_network_uuid)
    l3_network_uuid = create_l3_network(session_uuid,l2novlan_network_uuid,"l3")

    service_provider = query_service_provider(session_uuid,[])
    network_service_uuid = service_provider['inventories'][3]['uuid']
    network_services= {network_service_uuid: ["Eip", "DHCP", "Userdata"]}
    attach_network_service_to_l3_network(session_uuid,l3_network_uuid,network_services)

    instance_offering_uuid = create_instance_offering(session_uuid, "instance_offering1", 1, 1, 128*1024*1024)
    instance_offering_uuid_v2 = create_instance_offering(session_uuid, "instance_offering1", 2, 1, 128*1024*1024)
    l3_network_uuids = []
    l3_network_uuids.append(l3_network_uuid)
    add_ip_range(session_uuid, l3_network_uuid, "test-ip-range", l3_start_ip, l3_end_ip, l3_net_mask, l3_gw_ip)
    vm_uuid = create_vm(session_uuid,"vm1", instance_offering_uuid, image_uuid, l3_network_uuids)
    #get_console_access(session_uuid, vm_uuid)
    #change_instance_offering(session_uuid,instance_offering_uuid_v2,vm_uuid)
    #query_vm(session_uuid,[])
    #update_vm(session_uuid, vm_uuid, "vm2")
    #stop_vm(session_uuid, vm_uuid)
    #destroy_vm(session_uuid, vm_uuid)
    #expunge_vm(session_uuid, vm_uuid)
    #delete_image(session_uuid, image_uuid)
    #delete_backup_storage(session_uuid, backup_storage_uuid)
    #delete_zone(session_uuid, zone_uuid)
    #logout(session_uuid)
