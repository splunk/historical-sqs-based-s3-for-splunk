import unittest
import boto3
from botocore.exceptions import (ClientError,
                                ParamValidationError,
                                NoCredentialsError,
                                EndpointConnectionError)

class TestConnection(unittest.TestCase):

    # Test aws S3 connection
    def test_s3_connection(self):
        try:
            client = boto3.client('s3')
            response = client.list_buckets()
        except (
                    ClientError,
                    ParamValidationError,
                    NoCredentialsError,
                    EndpointConnectionError
               )  as e:
            raise AssertionError(e)

    # Test aws SQS connection
    def test_sqs_connection(self):
        try:
            client = boto3.client('sqs')
            response = client.list_queues()
        except (
                    ClientError,
                    ParamValidationError,
                    NoCredentialsError,
                    EndpointConnectionError
               )  as e:
            raise AssertionError(e)

if __name__ == '__main__':
    unittest.main()