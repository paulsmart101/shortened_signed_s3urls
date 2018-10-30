#!/bin/python
import boto3
import requests
import os
import sys
sys.path.append('../')
import bitly_api

# Variables
access_token = "1234"
bucket = '<bucket>'
keys = ["ACF Presentation Files 1.0.9 BR.zip",
"ACF Presentation Files 1.0.9 ES.zip",
"ACF Presentation Files 1.0.11 EN.zip",
"ACF Presentation Files 1.0.9 JP.zip",
"CF Presentation Files 1.0.9 CN.zip",
"CA Presentation Files 3.1.13 EN.zip"]

# Create the service clients
s3 = boto3.client('s3',region_name='eu-west-2')
bitly = bitly_api.Connection(access_token=access_token)

def GenerateUrl(bucket,key):
    # Generate the URL to get 'key-name' from 'bucket-name'
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        },ExpiresIn=604800
    )
    return url

def GenerateBitly(longurl,title):
    data = bitly.shorten(longurl)
    assert data is not None
    edit = bitly.user_link_edit(data['url'],edit='title',title=title)
    return data

print "________________________________________________________"
for key in keys:
    longurl = GenerateUrl(bucket,key)
    shorturl = GenerateBitly(longurl,key)
    print key
    print shorturl['url']
    print "________________________________________________________"

