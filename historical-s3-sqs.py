
import queue_s3_data
import time
import sys
import argparse

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
        self.parse_errors = False

        self.parser = argparse.ArgumentParser(description='Process aws options')
        self.parser.add_argument('queue', help='the queue url to send the events to (required)')
        self.parser.add_argument('bucket', help='the bucket to process events from (required)')
        self.parser.add_argument('region', help='the region both the bucket and the queue are in (required)')
        self.parser.add_argument('queueurl', help='the url of the SQS queue you would like to send messages to (required)')
        self.parser.add_argument('--startafter', help='ingest all records after the specified key in S3.  This can be any key in your bucket.')
        self.parser.add_argument('--prefix', help='ingest all records that match the specified prefix')
        self.parser.add_argument('--verbose', help='Display all names of the files being written (default: false)', action="store_true")
        self.parser.add_argument('--time', help='Display how long the execution takes to run (default: false)', action="store_true")

        args = self.parser.parse_args()
        try:
            self.queue_name = args.queue.split("=")[1]
        except:
            print("Invalid syntax. your positional arguments should be in the form queue=myqueuename bucket=mybucketname\n")
            self.parser.print_help()
            self.parse_errors = True
            return 

        try:
            self.bucket_name = args.bucket.split("=")[1]
        except:
            print("Invalid syntax. your positional arguments should be in the form queue=myqueuename bucket=mybucketname\n")
            self.parser.print_help()
            self.parse_errors = True
            return 

        try:
            self.region = args.region.split("=")[1]
        except:
            print("Invalid syntax. Your positional arguments should be in the form queue=myqueuename bucket=mybucketname\n")
            self.parser.print_help()
            self.parse_errors = True
            return 

        try:
            self.queue_url = args.queueurl.split("=")[1]
        except:
            print("Invalid syntax. your positional arguments should be in the form queue=myqueuename bucket=mybucketname\n")
            self.parser.print_help()
            self.parse_errors = True
            return 

        if args.startafter:
            self.start_after = args.startafter

        if args.prefix:
            self.prefix = args.prefix
        
        if args.verbose:
            self.verbose = True

        if args.time:
            self.time = True

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
    inst = HandleArgs()
    
    if inst.parse_errors:
        return
    inst.ingest()

if __name__ == '__main__':
    main()