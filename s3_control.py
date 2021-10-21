#!/usr/bin/env python3

import boto3 as b3
import sys

s3 = b3.resource("s3")

def create_s3():
    for bucket_name in sys.argv[2]:
        try:
            response = s3.create_bucket(Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
            print (response)
            # Make bucket publicly readble
        except Exception as error:
            print (error)

def list_s3_and_keys():
    for bucket in s3.buckets.all():
        print(bucket.name)
        print ('---')
        for item in bucket.objects.all():
            print("\t%s" % item.key)

def delete_bucket_contents():
    for bucket_name in sys.argv[1:]:
        bucket = s3.Bucket(bucket_name)
        for key in bucket.objects.all():
            try:
                response = key.delete()
                print (response)
            except Exception as error:
                print (error)

def populate_s3():
    bucket_name = sys.argv[1]
    file_name = sys.argv[2]
    try:
        response = s3.Object(bucket_name, file_name).put(Body=open(file_name, 'rb'))
        print(response)
    except Exception as error:
        print(error)

