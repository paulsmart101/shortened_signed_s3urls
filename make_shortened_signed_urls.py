#!/bin/python
import boto3
import requests
import json
import bitly_api

# Variables
access_token = "123"
arn = 'arn:aws:sns:eu-west-2:409201224315:email_paul'
bucket = 'bucketname'
keys = ["ACF Presentation Files 1.0.9 BR.zip",
"ACF Presentation Files 1.0.9 ES.zip",
"ACF Presentation Files 1.0.11 EN.zip",
"ACF Presentation Files 1.0.9 JP.zip",
"CF Presentation Files 1.0.9 CN.zip",
"CA Presentation Files 3.1.13 EN.zip"]

# Create the service clients
s3 = boto3.client('s3',region_name='eu-west-2')
sns = boto3.client('sns',region_name='eu-west-2')
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
    return data['url']

def SendEmail(message):
    response = sns.publish(
        TargetArn=arn,
        Message=json.dumps({'default': message}),
        MessageStructure='json'
    )


print "________________________________________________________"
for key in keys:
    longurl = GenerateUrl(bucket,key)
    shorturl = GenerateBitly(longurl,key)
    message = "Key: "+str(key)+"\nLink: "+str(shorturl)
    SendEmail(message)
    print message
    print "________________________________________________________"
