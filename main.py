#!/usr/bin/env python3
import argparse
import os
from ec2_control import ec2
from s3_control import s3

parser=argparse.ArgumentParser()
# ec2 parsing
parser.add_argument("-c-ec2","--create-ec2", dest='cec2', help='create an ec2 instance you will be prompted for an ssh key')
parser.add_argument("-ls-ec2", "--list-ec2", dest='lsec2', help='List all ec2 instances and associated information')
parser.add_argument("-rm-ec2", "--remove-ec2", dest='rmec2', help='Terminate ec2 instance by specifying instance id by passing the id as an argument')
parser.add_argument("-c-ec2-kp", "--create-ec2-keypair", dest='ckp', help='Create RSA key pair for ec2 instance')
#s3 parsing
parser.add_argument("-c-s3","--create-s3", dest='cs3', help='create an s3 bucket, location default is eu-west-1, requires bucket name')
parser.add_argument("-ls-s3", "--list-s3", dest='ls3', help='List all s3 buckets')
parser.add_argument("-rm-s3", "--remove-s3", dest='rms3', help='Empties and deletes all running buckets')

args=parser.parse_args()

#argument controls
def main():

    os.system('clear')

    if args.cec2:
        ec2.create_ec2()
    if args.lsec2:
        ec2.list_instances()
    if args.ckp:
        ec2.create_kp()
    if args.rmec2:
        ec2.terminate_ec2()
    if args.cs3:
        s3.create_s3()
    if args.ls3:
        s3.list_s3()
    if args.rms3:
        s3.delete_buckets()
    
if __name__ == "__main__":
    main()