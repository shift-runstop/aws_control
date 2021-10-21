#!/usr/bin/env python3
import argparse
import ec2_control
import s3_control

parser=argparse.ArgumentParser()

# ec2 parsing
parser.add_argument("-c-ec2","--create-ec2", dest='cec2', help='create an ec2 instance you will be prompted for an ssh key')
parser.add_argument("-ls-ec2", "--list-ec2", dest='lsec2', help='List all ec2 instances and associated information')

#s3 parsing
parser.add_argument("-c-s3","--create-s3", dest='cs3', help='create an s3 bucket, location default is eu-west-1, requires bucket name')
parser.add_argument("-ls-s3", "--list-s3", dest='ls3k', help='List all s3 buckets')

args=parser.parse_args()

#argument controls
def main():
    if args.cec2:
        ec2_control.create_ec2
    if args.cs3:
        s3_control.create_s3
    if args.ls3k:
        s3_control.list_s3_and_keys()
    if arg.lsec2:
        ec2_control.list_instances()

if __name__ == "__main__":
    main()