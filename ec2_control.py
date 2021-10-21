#!/usr/bin/env python3

import boto3 as b3
import sys
from termcolor import colored
import os

# set-up

os.system('clear')

def create_key_pair():
    KEY_PAIR_NAME = input('Name of new key: ')
    ec2=b3.client('ec2')
    key = ec2.create_key_pair(keyName=KEY_PAIR_NAME)
    key_file = open(KEY_PAIR_NAME + ".pem", "w")
    key_file.write(key.key_material)
    key_file.close()


def create_ec2():
    resp = input('do you wish to use the default key (Y/N)') 
    if resp == 'Y':
        key = 'web-server-key-key.pem'
        ec2_run()
    elif resp == 'N':
        key = create_key_pair()
        ec2_run()
    else:
     print('not a valid option')
     create_ec2()


def ec2_run(key):
    ec2 = b3.resource('ec2')
    ec2.create_instances(
            ImageId= 'ami-0d1bf5b68307103c2',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.nano',
            ecurityGroupIds=['sg-2a07095e4e3fda0c2'],
            KeyName=key
    )
    ec2.wait_until_running()
    ec2.reload()


def terminate_ec2():
    ec2 = b3.resource('ec2')
    for instance_id in sys.argv[1:]:
        instance = ec2.instance(instance_id)
        response = instance.terminate()
        print(response)


def list_instances():
    for i in ec2.instances.all():
        ec2_list = []
        print("Id: {0}\tState: {1}\tLaunched: {2}\tRoot Device Name: {3}".format(
            colored(i.id, 'cyan'),
            colored(i.state['Name'], 'green'),
            colored(i.launch_time, 'cyan'),
            colored(i.root_device_name, 'cyan')
        ))

        print("\tArch: {0}\tHypervisor: {1}".format(
            colored(i.architecture, 'cyan'),
            colored(i.hypervisor, 'cyan')
        ))

        print("\tPriv. IP: {0}\tPub. IP: {1}".format(
            colored(i.private_ip_address, 'red'),
            colored(i.public_ip_address, 'green')
        ))

        print("\tPriv. DNS: {0}\tPub. DNS: {1}".format(
            colored(i.private_dns_name, 'red'),
            colored(i.public_dns_name, 'green')
        ))

        print("\tSubnet: {0}\tSubnet Id: {1}".format(
            colored(i.subnet, 'cyan'),
            colored(i.subnet_id, 'cyan')
        ))

        print("\tKernel: {0}\tInstance Type: {1}".format(
            colored(i.kernel_id, 'cyan'),
            colored(i.instance_type, 'cyan')
        ))

        print("\tRAM Disk Id: {0}\tAMI Id: {1}\tPlatform: {2}\t EBS Optimized: {3}".format(
            colored(i.ramdisk_id, 'cyan'),
            colored(i.image_id, 'cyan'),
            colored(i.platform, 'cyan'),
            colored(i.ebs_optimized, 'cyan')
        ))

        print("\tBlock Device Mappings:")
        for idx, dev in enumerate(i.block_device_mappings, start=1):
            print("\t- [{0}] Device Name: {1}\tVol Id: {2}\tStatus: {3}\tDeleteOnTermination: {4}\tAttachTime: {5}".format(
                idx,
                colored(dev['DeviceName'], 'cyan'),
                colored(dev['Ebs']['VolumeId'], 'cyan'),
                colored(dev['Ebs']['Status'], 'green'),
                colored(dev['Ebs']['DeleteOnTermination'], 'cyan'),
                colored(dev['Ebs']['AttachTime'], 'cyan')
            ))

        print("\tTags:")
        for idx, tag in enumerate(i.tags, start=1):
            print("\t- [{0}] Key: {1}\tValue: {2}".format(
                idx,
                colored(tag['Key'], 'cyan'),
                colored(tag['Value'], 'cyan')
            ))

        print("\tProduct codes:")
        for idx, details in enumerate(i.product_codes, start=1):
            print("\t- [{0}] Id: {1}\tType: {2}".format(
                idx,
                colored(details['ProductCodeId'], 'cyan'),
                colored(details['ProductCodeType'], 'cyan')
            ))

        print("Console Output:")
        # Commented out because this creates a lot of clutter..
        # print(i.console_output()['Output'])

        print("--------------------")
