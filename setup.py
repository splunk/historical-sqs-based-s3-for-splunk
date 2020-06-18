import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="historical-sqs-based-s3-for-splunk-skylert", # Replace with your own username
    version="0.0.1",
    author="Skyler Taylor",
    author_email="skylert@splunk.com",
    description="Crawls S3 buckets and puts ingest notifications on the SQS queue",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/splunk/historical-s3-sqs-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)