import time
import sys

import argparse
import inquirer
import pprint
import boto3

from bin.queue import QueueS3Data

__author__ = 'Skyler Taylor'
__version__ = '1.0.0'
__email__  = 'skylert@splunk.com'
__maintainer__ = ''
__status__ = 'Prototype'

class CliGUI(object):

    def __init__(self):
        self.bucket = ''
        self.queuename = ''
        self.queueurl = ''
        self.region = ''
        self.start_after = False
        self.prefix = False
        self.verbose = False
        self.time = False

        self.s3 = boto3.client('s3')
        self.sqs = boto3.client('sqs')

        try:
            response = self.s3.list_buckets()
        except:
            raise ValueError('credentials missing or invalid')
        
        try:
            self.buckets = [bucket for bucket in response['Buckets']]
            bucket_choices = [bucket['Name'] for bucket in self.buckets]
        except Exception as e:
            raise e

        try:
            response = self.sqs.list_queues()
            self.queue_urls = [queue for queue in response['QueueUrls']]
        except KeyError:
            raise KeyError('no queues found')

        self.questions = [
            inquirer.List(name='queueurl', message='Enter the url of the SQS queue you would like to send messages to', choices=self.queue_urls),
            inquirer.List(name='bucketname', message='Enter the s3 bucket to process events from', choices=bucket_choices),
            inquirer.Text(name='startafter', message='Ingest all records after the specified key in S3. This can be any key in your bucket. (press enter to skip)'),
            inquirer.Text(name='prefix', message='Ingest all records that match the specified prefix (press enter to skip)'),
            inquirer.Confirm(name='verbose', message='Verbose mode'),
        ]

        res = inquirer.prompt(self.questions)
        res['queuename'] = res['queueurl'].split('/')[-1]
        res['region'] = self.s3.get_bucket_location(Bucket=res['bucketname'])['LocationConstraint']
        self.attrs = res

    def queue(self):
        start = self.__timeit()
        inst = QueueS3Data(**self.attrs)
        num_events = inst.process_s3()
        end = self.__timeit()
        print('{} files added to {} in {} seconds'.format(num_events, self.queueurl, end-start))

    def __timeit(self):
        return time.time()
        
class Cli(object):

    def __init__(self):

        self.queue_name = ''
        self.bucket_name = ''
        self.queue_url = ''
        self.region = ''
        self.start_after = False
        self.prefix = False
        self.verbose = False
        self.time = False

        self.attrs = {}

        self.parser = argparse.ArgumentParser(description='Process aws options')

        self.parser.add_argument('queueurl', help='the url of the SQS queue you would like to send messages to (required)')
        self.parser.add_argument('bucket', help='the bucket to process events from (required)')
        self.parser.add_argument('region', help='the region both the bucket and the queue are in (required)')
        self.parser.add_argument('--startafter', help='ingest all records after the specified key in S3.  This can be any key in your bucket.')
        self.parser.add_argument('--prefix', help='ingest all records that match the specified prefix')
        self.parser.add_argument('--verbose', help='Display all names of the files being written (default: false)', action='store_true')

        args = self.parser.parse_args()

        try:
            self.attrs['queueurl'] = args.queueurl.split('=')[1]
            self.attrs['bucketname'] = args.bucket.split('=')[1]
            self.attrs['region'] = args.region.split('=')[1]
            self.attrs['queuename'] = self.attrs['queueurl'].split('/')[-1]

            if args.startafter:
                self.attrs['startafter'] = args.startafter

            if args.prefix:
                self.attrs['prefix'] = args.prefix
            
            if args.verbose:
                self.attrs['verbose'] = True

        except:
            raise SyntaxError('Invalid syntax. your positional arguments should be in the form queueurl=<myqueueurl> bucket=<mybucketname>')

    def queue(self):
        inst = QueueS3Data(**self.attrs)

        if self.time:
            start = self.__timeit()

        num_events = inst.process_s3()

        if self.time:
            end = self.__timeit()
            total_time = end - start
            print('{} files added to {} in {} seconds'.format(num_events, self.queue_url, total_time))

        else:
            print('Done')

    def __timeit(self):
        return time.time()