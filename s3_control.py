#!/usr/bin/env python3

import boto3 as b3
import sys
import os
import uuid
import re
import subprocess
import webbrowser

class s3:

    s3 = b3.resource("s3")

    def create_s3():
        temp = uuid.uuid1()
        bucket_name=re.sub('-','0',str(temp))

        try:
            s3_client = b3.client("s3")

            bucket = s3_client.create_bucket(Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'},
            ACL='public-read'
            )
            print (bucket, 'Bucket{} created successfully'.format(bucket_name))
            
        except Exception as error:
            print ('Something bad happened: ',error)

        option = input('Static Website Configuration (y/n)')
        if option =='y':
            try:
                print('Downloading Files')
                subprocess.run("curl http://devops.witdemo.net/assign1.jpg > assign1.jpg", shell=True)
                subprocess.run("touch index.html", shell=True)
                
                htmlObject = 'index.html'
                print('Sending index.html to bucket')
                s3.Object(bucket_name, htmlObject).put(
                    Body=open(object, 'rb'), 
                    ContentType='text/html',
                    ACL='public-read'
                )

                jpgObject = 'assign1.jpg'
                print('Sending image to bucket')
                s3.Object(bucket_name, jpgObject).put(
                    Body=open(object, 'rb'), 
                    ContentType='image/jpeg',
                    ACL='public-read'
                )

                print('Writing to file')
                subprocess.run("echo '<img src=https://{}.s3.eu-west-1.amazonaws.com/assign1.jpg>'> index.html".format(bucket_name), shell=True) 
                print('Image has been attached to page')
                
            except Exception as error:
                print('Bucket Broken, please fix: ',error)

            try:
                
                s3_client = b3.client("s3")
                s3_client.put_bucket_website(
                    Bucket=bucket_name, 
                    WebsiteConfiguration={
                        'ErrorDocument': {'Key': 'error.html'},
                        'IndexDocument': {'Suffix': 'index.html'},
                    }
                )

                print('Opening in browser')
                webbrowser.open_new_tab('https://{}.s3.eu-west-1.amazonaws.com/index.html'.format(bucket_name))
                
                print('Bucket Success')

            except Exception as error:
                print('Bucket Broke again')
                print(error)
        else:
            os._exit(0)
            

    def list_s3():
        s3 = b3.resource("s3")
        for bucket in s3.buckets.all():
            print(bucket.name)
            print ('----------')
            for item in bucket.objects.all():
                print("\t%s" % item.key)

    def delete_buckets():
        try:
            s3_client = b3.client('s3')
            s3 = b3.resource('s3')

            buckets = s3_client.list_buckets()

            for bucket in buckets['Buckets']:
                s3_bucket = s3.Bucket(bucket['Name'])
                s3_bucket.objects.all().delete()
                print(s3_bucket, ' emptied')
                s3_bucket.delete()
                print(s3_bucket, ' deleted')

        except Exception as error:
            print('No buckets to delete!')
            print(error)
        print('No more buckets to delete')