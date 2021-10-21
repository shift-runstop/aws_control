#!/usr/bin/env python3

import boto3 as b3
import sys

def create_s3():
    s3 = b3.resource("s3")
    for bucket_name in sys.argv[1:]:
        try:
            response = s3.create_bucket(Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
            print (response)
        except Exception as error:
            print (error)

def list_s3_and_keys():
    s3 = b3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)
        print ('---')
        for item in bucket.objects.all():
            print("\t%s" % item.key)

def delete_bucket_contents():
    s3 = b3.resource('s3')
    for bucket_name in sys.argv[1:]:
        bucket = s3.Bucket(bucket_name)
        for key in bucket.objects.all():
            try:
                response = key.delete()
                print (response)
            except Exception as error:
                print (error)