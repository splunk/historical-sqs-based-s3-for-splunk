# Title
This project was built to work along with AWS Add-On for Splunk to ingest historical data into splunk via the SQS queue. Because SQS is event based, there is no way to get messages onto the SQS queue about s3 objects that pre-date the queue. This python package will create messages in the SQS queue that will allow the AWS Add-On for Splunk to ingest these s3 objects. 

This package utilizes the boto3 python library for AWS api calls.

## Features (optional)
What makes your project stand out? Highlight relevant features.

## Table of Contents (optional)
Only in case of very long READMEs

## Getting Started
### Requirements (optional)
What things you need to have installed to run installation smoothly. Add also details on how to install them.

### Installation
Tell other users how to install your project locally. Optionally, include a gif to make the process even more clear for other people.

### Usage
Instruct other people on how to use your project after they’ve installed it. This would also be a good place to include screen shots of your project in action.

### Tests (optional)
Explain how to run the automated tests for this system

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
