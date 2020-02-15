import boto3
import concurrent.futures
import multiprocessing
import json
from datetime import date, datetime
import time

class QueueS3Data(object):
    def __init__(self, queue_name, queue_url, bucket_name, region):
        self.sqs = boto3.resource('sqs')
        self.s3 = boto3.resource('s3')
        self.client = boto3.client('s3')
        self.queue_name = queue_name

        try:
            self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        except:
            raise ValueError('Error, check your queue name and aws credentials')
        self.bucket_name = bucket_name

        try:
            self.bucket = self.s3.Bucket(bucket_name)
        except:
            raise ValueError('Error, check your bucket name and aws credentials')
        self.queue_url = queue_url
        self.region = region

        try:
            self.cpu_count = psutil.cpu_count()
        except:
            self.cpu_count = 2

        self.s3_data = list()

    def __enqueue(self, body):
        try:
            response = self.queue.send_message(
                QueueUrl = self.queue_url,
                MessageBody = body
            )
        except:
            print("Error when sending message to SQS queue:", self.queue_url)
        
        return response


    def process_s3(self):

        num_events = 0
        paginator = self.client.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(Bucket=self.bucket_name)
        arn = 'arn:aws:s3:::{}'.format(self.queue_name)
        region = self.region

        print("Processing events..")
        for pageobj in response_iterator:
            page = list()
            for obj in pageobj['Contents']:

                size = obj['Size']
                key = obj['Key']
                last_modified = obj['LastModified']
                etag = obj['ETag']

                json_message = self.__construct_message(key, last_modified, size, arn, region, etag)
                message = json.dumps(json_message, default=self.__serialize_datetime)
                page.append(message)
                num_events += 1
            self.s3_data.append(page)

        print("Sending messages to SQS..")
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.cpu_count*2) as executor:
            for page in self.s3_data:
                future_response = {executor.submit(self.__enqueue, message) for message in page}

        return num_events


    def __serialize_datetime(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        else:
            raise TypeError ("Type %s not serializable" % type(obj))

    def __construct_message(self, key, last_modified, size, arn, region, etag):
        message = {
            "Records": [
                {
                    "eventVersion": "2.1",
                    "eventSource": "aws:s3",
                    "awsRegion": region,
                    "eventTime": last_modified,
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "AWS:AROAIF4JELG3VJGB7GNKM:regionalDeliverySession"
                },
                    "requestParameters": {
                        "sourceIPAddress": "54.92.179.66"
                },
                    "responseElements": {
                        "x-amz-request-id": "9F7C49919622C34A",
                        "x-amz-id-2": "KcSix4Os8A+rHSEGV0B/uvOMly9nJ6eub5+nw/3w13YbmSozv0Tu5RGBqTTGWunxpa/hdlXhnI3qLowAgFMTNxa1nwJSx4Rc"
                },
                "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "MySplunkEventForObjectCreate",
                        "bucket": {
                        "name": self.bucket_name,
                        "ownerIdentity": {
                            "principalId": "A2I92S72CEK8CQ"
                    },
                        "arn": arn
                    },
                        "object": {
                            "key": key,
                            "size": size,
                            "eTag": etag,
                            "sequencer": "005E430DF8DA899339"
                        }
                    }
                }
            ]
        }
        return message


