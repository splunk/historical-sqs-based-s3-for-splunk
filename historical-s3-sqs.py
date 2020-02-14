
import queue_s3_data
import time
import sys

class HandleArgs(object):

    def __init__(self):
        self.usage_str = "NAME:\n\t{} - {}\n\nUSAGE:\n\t{} [{}] [{}...]\n\nOPTIONS:\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}\n\t{}"
        self.usage_args = ["historical-s3-sqs ingest",
            "push object create events from S3 into SQS",
            "historical-s3-sqs ingest",
            "command options",
            "arguments...",
            "--queue value       the queue url to send the events to (required)",
            "--bucket value      the bucket to process events from (required)",
            "--region value      the region both the bucket and the queue are in (required)",
            "--queueurl value    the url of the SQS queue you would like to semd messages to (required)",
            "--startafter value  ingest all records after the specified key in S3.  This can be any key in your bucket.",
            "--prefix value      ingest all records that match the specified prefix",
            "--verbose           Display all names of the files being written (default: false)",
            "--time              Display how long the execution takes to run (default: false)",
            "--help, -h          show help (default: false)"]

        self.valid_args = {"ingest", "verbose", "time", "help"}
        self.required_args = {"ingest"}
        self.valid_kwargs = {
            "queue", 
            "bucket", 
            "queueurl", 
            "startafter", 
            "prefix",
            "region" 
        }
        self.required_kwargs = {
            "queue", 
            "bucket", 
            "queueurl",
            "region"
        }

        self.queue_name = ''
        self.bucket_name = ''
        self.queue_url = ''
        self.startafter = False
        self.prefix = False
        self.verbose = False
        self.time = False
        self.help = False
        
    def print_usage(self):
        print(self.usage_str.format(*self.usage_args))

    def needs_help(self):
        return self.help

    def is_valid_args(self, args):
        num_required_args_met = 0
        for arg in args:
            if arg in self.required_args:
                num_required_args_met += 1
            if arg not in self.valid_args:
                return False
        return num_required_args_met == len(self.required_args)

    def is_valid_kwargs(self, kwargs):
        num_required_kwargs_met = 0
        for key in kwargs.keys():
            if key in self.required_kwargs:
                num_required_kwargs_met += 1
            if key not in self.valid_kwargs:
                return False
        return num_required_kwargs_met == len(self.required_kwargs)

    def process_args(self, args):
        for arg in args:
            if arg == "verbose":
                self.verbose = True
            elif arg == "time":
                self.time = True
            elif arg == "help":
                self.help == True                

    def process_kwargs(self, kwargs):
        for arg, value in kwargs.items():
            if arg == "bucket":
                self.bucket_name = value
            elif arg == "queue":
                self.queue_name = value
            elif arg == "queueurl":
                self.queue_url = value
            elif arg == "startafter":
                self.startafter = value
            elif arg == "prefix":
                self.prefix = value
            elif arg == "region":
                self.region = value

    def ingest(self):
        # queue_name, queue_url, bucket_name, region
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
    print(args, kwargs)
    print(len(sys.argv))
    return
    inst = HandleArgs()
    ready = inst.is_valid_args(args) and inst.is_valid_kwargs(kwargs)
    
    if not ready or inst.needs_help():
        inst.print_usage()
        return
    else:
        inst.ingest()

if __name__ == '__main__':
    main()