import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='queues3',  
     version='0.1',
     scripts=['queues3'] ,
     author="Skyler Taylor",
     author_email="skylert@splunk.com",
     description="A AWS Add-On for Splunk helper package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
