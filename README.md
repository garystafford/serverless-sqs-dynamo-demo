# Event-driven, Serverless Architectures with AWS Lambda, SQS, DynamoDB, and API Gateway

Project files for the post, [Event-driven, Serverless Architectures with AWS Lambda, SQS, DynamoDB, and API Gateway
](https://programmaticponderings.com/2019/10/04/event-driven-serverless-architectures-with-aws-lambda-sqs-dynamodb-and-api-gateway/).

In the post, we will explore modern application development using an event-driven, serverless architecture on AWS. To demonstrate this architecture, we will integrate several fully-managed services, all part of the AWS Serverless Computing platform. Serverless AWS offerings include Lambda, API Gateway, SQS, S3, and DynamoDB. The end result will be an application composed of small, easily deployable, loosely coupled serverless components.

## Quick Start

### Prerequisites
The demonstration assumes you already have an AWS account. You will need the latest copy of the AWS CLI, SAM CLI, and Python 3 installed on your development machine.

Additionally, you will need two existing S3 buckets. One bucket will be used to store the packaged project files for deployment. The second bucket is where we will place CSV data files, which in turn, will trigger events that invoke multiple Lambda functions.


### CloudFormation Parameter

Template Parameter
CloudFormation will create and uniquely name the SQS queues and the DynamoDB table. However, to avoid circular references , a common issue, between resources associated with the S3 data bucket, it is easier to use a pre-existing bucket. To start, you will need to change the SAM template’s DataBucketName parameter’s default value to your own S3 bucket name. Again, this bucket is where we will eventually push the CSV data files. Alternately, override the default values using the sam build command, next.
```yaml
Parameters:
  DataBucketName:
    Type: String
    Description: S3 bucket where CSV files are processed
    Default: your-data-bucket-name
```

### Deploying the Project

```bash
# variables
S3_BUILD_BUCKET="your_build_bucket_name"
STACK_NAME="your_stack_name"

# validate
sam validate --template template.yaml

aws cloudformation validate-template \
  --template-body file://template.yaml

# build
sam build --template template.yaml

# package
sam package \
  --output-template-file packaged.yaml \
  --s3-bucket "${S3_BUILD_BUCKET}"

# deploy
sam deploy --template-file packaged.yaml \
  --stack-name "${STACK_NAME}" \
  --capabilities CAPABILITY_IAM \
  --debug
```

---

<i>The contents of this repository represent my viewpoints and not of my past or current employers, including Amazon Web Services (AWS). All third-party libraries, modules, plugins, and SDKs are the property of their respective owners.</i>
