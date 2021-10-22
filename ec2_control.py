#!/usr/bin/env python3

import boto3 as b3
import sys
from termcolor import colored
import subprocess
import webbrowser
import time
import os

# set-up

os.system('clear')
ec2 = b3.resource('ec2')
ec2_client = b3.client('ec2')

def create_ec2():
    try:
        #key = ec2_client.keyPair('web-server-key-key')
        instance = ec2.create_instances(
            ImageId= 'ami-0d1bf5b68307103c2',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.nano',
            SecurityGroupIds = [
                'sg-08c878eeead2e48a9'       
            ],
            KeyName='web-server-key-key',

            UserData = 
                    ''' 
                    #!/bin/bash
                    sudo apt-get update
                    sudo yum install httpd -y
                    sudo systemctl enable httpd 
                    sudo systemctl start httpd 
                    echo '<html>' > index.html
                    echo 'Private IP address: ' >> index.html
                    curl -s http://169.254.169.254/latest/meta-data/local-ipv4>> index.html
                    echo 'Public IP address: ' >> index.html 
                    curl -s http://169.254.169.254/latest/meta-data/public-ipv4 >> index.html
                    echo 'Instance type: ' >> index.html
                    curl -s http://169.254.169.254/latest/meta-data/instance-type >> index.html
                    echo 'Instance ID: ' >> index.html
                    curl -s http://169.254.169.254/latest/meta-data/instance-id >> index.html
                    cp index.html /var/www/html/index.html
                    ''',
                    TagSpecifications = [
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                'Key': 'Name',
                                'Value': 'Assignment Instance'
                                }
                            ]
                        }
                    ]
        )

        instance[0].wait_until_running()            
    except Exception as error:
        print('(ノ°Д°）ノ︵ ┻━┻')
        print(error)

    try:
        instance[0].reload()
        ec2_ip = instance[0].public_ip_address

        print('Uploading monitoring...')

        waiter = ec2_client.get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=[instance[0].instance_id])
        subprocess.run("scp -o StrictHostKeyChecking=no -i web-server-key-key.pem monitor.sh ec2-user@" + ec2_ip + ":.", shell=True)
        subprocess.run("ssh -o StrictHostKeyChecking=no -i web-server-key-key.pem ec2-user@" + ec2_ip + " 'chmod 700 monitor.sh'", shell=True)
        subprocess.run("ssh -o StrictHostKeyChecking=no -i web-server-key-key.pem ec2-user@" + ec2_ip + " ' ./monitor.sh'", shell=True)

        print('Opening in browser: ')
        webbrowser.open_new_tab(ec2_ip)

    except Exception as e:
        print('An error occurred while setting up monitoring.')#
        print(e)

def create_kpc():
    resp = input('do you wish to use the default key (Y/N)') 
    if resp == 'Y':
        key = 'web-server-key-key.pem'
    elif resp == 'N':
        KEY_PAIR_NAME = input('Name of new key: ')
        key = ec2.create_key_pair(keyName=KEY_PAIR_NAME)
        key_file = open(KEY_PAIR_NAME + ".pem", "w")
        key_file.write(key.key_material)
        key_file.close()
    else:
     print('not a valid option')

def terminate_ec2():
    for instance_id in sys.argv[1]:
        instance = ec2.instance(instance_id)
        response = instance.terminate()
        print(response)


def list_instances():
    for i in ec2.instances.all():
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
        # print(i.console_output()['Output'])
        print("--------------------")