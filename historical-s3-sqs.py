
import queue_s3_data
import time
import sys
import argparse
import inquirer
import boto3
import pprint

class GUIArgs(object):

    def __init__(self):
        self.queue_name = ''
        self.bucket = ''
        self.queueurl = ''
        self.region = ''
        self.start_after = False
        self.prefix = False
        self.verbose = False
        self.time = False

        self.s3 = boto3.client('s3')
        self.sqs = boto3.client('sqs')

        response = self.s3.list_buckets()
        self.buckets = [bucket for bucket in response['Buckets']]
        response = self.sqs.list_queues()

        self.queue_urls = [queue for queue in response['QueueUrls']]

        self.questions = {
            'queueurl': inquirer.List(name='queueurl', message='the url of the SQS queue you would like to send messages to (required)', choices=self.queue_urls),
            'bucket': inquirer.List(name='bucket', message='the bucket to process events from (required)', choices=[bucket['Name'] for bucket in self.buckets]),
            
        }

        for key, question in self.questions.items():
            res = inquirer.prompt([question])
            if key == 'bucket':
                self.bucket = res[key]
                self.region = self.s3.get_bucket_location(Bucket=self.bucket)['LocationConstraint']
            self.key = res[key]



class HandleArgs(object):

    def __init__(self):

        self.queue_name = ''
        self.bucket_name = ''
        self.queue_url = ''
        self.region = ''
        self.start_after = False
        self.prefix = False
        self.verbose = False
        self.time = False

        self.parser = argparse.ArgumentParser(description='Process aws options')

        self.parser.add_argument('queueurl', help='the url of the SQS queue you would like to send messages to (required)')
        self.parser.add_argument('bucket', help='the bucket to process events from (required)')
        self.parser.add_argument('region', help='the region both the bucket and the queue are in (required)')
        self.parser.add_argument('--startafter', help='ingest all records after the specified key in S3.  This can be any key in your bucket.')
        self.parser.add_argument('--prefix', help='ingest all records that match the specified prefix')
        self.parser.add_argument('--verbose', help='Display all names of the files being written (default: false)', action="store_true")
        self.parser.add_argument('--time', help='Display how long the execution takes to run (default: false)', action="store_true")

        args = self.parser.parse_args()

        try:
            self.queue_url = args.queueurl.split("=")[1]
            self.bucket_name = args.bucket.split("=")[1]
            self.region = args.region.split("=")[1]
            self.queue_name = self.queue_url.split('/')[-1]

            if args.startafter:
                self.start_after = args.startafter

            if args.prefix:
                self.prefix = args.prefix
            
            if args.verbose:
                self.verbose = True

            if args.time:
                self.time = True
            #print("RE",self.queue_name)
        except:
            raise SyntaxError('Invalid syntax. your positional arguments should be in the form queue=myqueuename bucket=mybucketname')

    def ingest(self):
        inst = queue_s3_data.QueueS3Data(self.queue_name, self.queue_url, self.bucket_name, self.region)

        if self.time:
            start = self.__timeit()

        num_events = inst.process_s3()

        if self.time:
            end = self.__timeit()
            total_time = end - start
            print("{} events added to {} in {} seconds".format(num_events, self.queue_url, total_time))

        else:
            print("Done")

    def __timeit(self):
        return time.time()


def main(*args, **kwargs):
    # try:
    #     inst = HandleArgs()
    # except SyntaxError as e:
    #     print(e)
    #     return

    # try:
    #     inst.ingest()

    # except ValueError:
    #     print('Error! check your queue url and bucket name')

    inst = GUIArgs()

if __name__ == '__main__':
    main()