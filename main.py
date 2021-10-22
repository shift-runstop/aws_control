#!/usr/bin/env python3
import argparse

from ec2_control import ec2
from s3_control import s3

parser=argparse.ArgumentParser()
# ec2 parsing
parser.add_argument("-c-ec2","--create-ec2", dest='cec2', help='create an ec2 instance you will be prompted for an ssh key')
parser.add_argument("-ls-ec2", "--list-ec2", dest='lsec2', help='List all ec2 instances and associated information')
parser.add_argument("-rm-ec2", "--remove-ec2", dest='rmec2', help='Terminate ec2 instance by specifying instance id by passing the id as an argument')
#s3 parsing
parser.add_argument("-c-s3","--create-s3", dest='cs3', help='create an s3 bucket, location default is eu-west-1, requires bucket name')
parser.add_argument("-ls-s3", "--list-s3", dest='ls3k', help='List all s3 buckets')

args=parser.parse_args()

#argument controls
def main():
    if args.cec2:
        ec2.create_ec2()
    if args.lsec2:
        ec2.list_instances()
    if args.rmec2:
        ec2.terminate_ec2()
    if args.cs3:
        s3.create_s3()
    if args.ls3k:
        s3.list_s3_and_keys()
    
if __name__ == "__main__":
    main()