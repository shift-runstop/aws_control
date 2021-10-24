#!/usr/bin/env python3

import boto3 as b3
import sys
import os
import subprocess
import webbrowser
import time

from termcolor import colored


class ec2:
    
    os.system('clear')
      
    def create_ec2():
        try:
            #key = ec2_client.keyPair('web-server-key-key')
            ec2 = b3.resource('ec2')
            print('Creating ec2 instance')
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
                        sudo yum install -y httpd
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
            print('Uploading monitoring')
            subprocess.run("scp -o StrictHostKeyChecking=no -i web-server-key-key.pem monitor.sh ec2-user@" + ec2_ip + ":.", shell=True)
            print('Accessing permissions')
            subprocess.run("ssh -o StrictHostKeyChecking=no -i web-server-key-key.pem ec2-user@" + ec2_ip + " 'chmod 700 monitor.sh'", shell=True)
            print('Running script now')
            subprocess.run("ssh -o StrictHostKeyChecking=no -i web-server-key-key.pem ec2-user@" + ec2_ip + " ' ./monitor.sh'", shell=True)
            
            print('Opening in browser')
            instance[0].reload()
            # ec2_client = b3.client('ec2')
            # waiter = ec2_client.get_waiter('instance_status_ok')
            # waiter.wait(InstanceIds=[instance[0].instance_id])
            webbrowser.open_new_tab('http://'+ec2_ip)

        except Exception as e:
            print('Error on monitoring')#
            print(e)

    def create_kp():
        ec2 = b3.resource('ec2')
        try:
            KEY_PAIR_NAME = input('Name of new key: ')
            key = ec2.create_key_pair(KeyName=KEY_PAIR_NAME)
            key_file = open(KEY_PAIR_NAME + ".pem", "w")
            key_file.write(key.key_material)
            key_file.close()
        except Exception as error:
            print('key pair creation error: ', error)

    def terminate_ec2():
        ec2 = b3.resource('ec2')
        try:
            for inst in ec2.instances.all():
                if inst.state['Name'] != 'terminated':
                    inst.terminate()
                    print('Instance', inst.instance_id, 'deleted.')

        except Exception as error:
            print('Error deleting instances')
            print(error)
        print('No more instances to delete')

    def list_instances():
        # https://github.com/suhaibchishti/sample_scripts/blob/master/aws_list_ec2.py
        ec2 = b3.resource('ec2')
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

            print("--------------------")