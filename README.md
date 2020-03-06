# Title
AWS S3 can be configured to submit a message to SQS whenever an object is added to a bucket.  Splunk uses SQS to intelligently ingest new filse from sources such as S3 without having to query S3 directly. This saves precious CPU cycles since Splunk no longer has to maintain a list of ingested files so that there are no duplicates. The downside to this method is that in order for a message about an object in S3 to be automatically added to SQS, it has to be added to the bucket.  While new items added to the bucket will automatically be ingested since messages are created on object upload, historical assets will not be ingested since SQS was configured after the items were added to the bucket.

This command line tool fixes this problem by crawling an AWS bucket you specify and adding events to SQS so Splunk can properly ingest them.

## Getting Started
### Requirements (optional)
What things you need to have installed to run installation smoothly. Add also details on how to install them.

### Installation
For now git clone https://gitlab.com/splunk-fdse/other/query-s3-data.git

### Usage
python -m main

### Tests (optional)
TBD

## Example(s)
Add here examples of usages. Another good place to include screenshots or gifs.

## Contributing
Explain here how users can contribute. For example:
* make a PR,
* create an issue,
* branch the code,
* use [gitflow](https://jeffkreeftmeijer.com/git-flow/),
* etc

If very long, consider adding `CONTRIBUTING.md` to the repository for details on code of conduct, the process for submitting pull requests, etc.

## References & Takeaway (optional)
List encountered challenges and what contributed to their resolution by providing relevant links. 

## Credits & Acknowledgements (optional)
Give proper credits. This could be a link to any repo which inspired you to build this project, any blogposts or links to people who contributed in this project.

## License
Short snippet linking to `LICENSE.md`
