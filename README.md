# better-sam

This project aims to make it easier to separate large AWS SAM template files and script assembly using AWS SAM CLI. 

## Prerequisites

Before running the `better-sam.py` script, make sure you have the following installed:

- Python 3.x
- AWS CLI
- AWS SAM CLI


## Motivation

When working with large AWS SAM templates, it can be challenging to manage all the resources in a single file. This project aims to make it easier to split large SAM templates into multiple files and script assembly using the AWS SAM CLI.

I like feature in __serverless Framework__ or __terraform__ where you can split your resources into multiple files and then just reference them in the main file. This is very useful when you have a large number of resources in your SAM template and want to keep things organized. But unfortunately, AWS SAM does not support this feature out of the box. So, I created this project to help you split your SAM templates into multiple files and script assembly using the AWS SAM CLI.

Faced with the same problem, I decided to create a simple Python script that can be used to split a large AWS SAM template into multiple files and generate a single output file that can be used with the AWS SAM CLI. This script is called `better-sam.py` and is available in this repository.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/chapimenge3/better-sam.git
    ```

    or just download the `better-sam.py` file.

2. Install the required dependencies:

    - No dependencies are required for this project.

## Usage

To use `better-sam.py`, follow these steps:

1. Place your template files in the `better-templates.yaml` directory.

2. Modify the `better-templates.yaml` with the following Rule.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: "AWS::Serverless-2016-10-31"
Description: >
  Main template for ServerlessBlogApp, including nested stacks for various resources.

Resources:
  Include:
    - "./infra/api.yaml"
    - "./infra/auth.yaml"
    - "./infra/databases.yaml"
    - "./infra/events.yaml"
    - "./infra/storage.yaml"
    - "./infra/users-pool.yaml"
    - "./functions/functions.yaml"
  
  # define any resource as you would in a normal SAM template file
  HelloWorldFunction:
    Type: "AWS::Serverless::Function"
    Properties:
      CodeUri: "src/"
      Handler: "hello-world.handler"
      Runtime: "nodejs12.x"
      Events:
        HelloWorld:
          Type: "Api"
          Properties:
            Path: "/hello"
            Method: "get"

Outputs:
  BlogApiUrl:
    Description: "API Gateway endpoint URL for Prod stage for Blog application"
    Value: !Sub "https://${ApiResources}.execute-api.${AWS::Region}.amazonaws.com/Prod/"
    Export:
      Name: BlogApiUrl
```

Now Make sure to define the files you mentioned in the `Include` section. like the below example.

`./infra/storage.yaml`
```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: serverless-blog-post-images

  RedisCluster:
    Type: AWS::ElastiCache::CacheCluster
    Properties:
      CacheNodeType: cache.t2.micro
      Engine: redis
      NumCacheNodes: 1
```

NOTICE: We used `Resource` again inside of the `storage.yaml` file, this is because nothing but random thoughts. the script is very simple so feel free to modify it as you like. **BUT PLEASE MAKE SURE TO USE THE SAME FORMAT AS THE EXAMPLE ABOVE** unless you know what you are doing.

3. Run the script:

```bash
python better-sam.py better-templates.yaml output/template.yaml

# or with default values better-templates.yaml and template.yaml
python better-sam.py
```

4. The assembled SAM template will be generated in the output file you mentioned.

- if you run the script like `python better-sam.py better-templates.yaml output/template.yaml` the output will be in the `output/template.yaml` file
- if your run the script like `python better-sam.py` the output will be in the `template.yaml` file so you can use it directly with the `sam` cli.

5. Deploy the assembled SAM template using the AWS SAM CLI:

```bash
sam build -t template.yaml # or sam build -t output/template.yaml
sam deploy -t template.yaml --guided # or sam deploy -t output/template.yaml --guided
```

### Make your life more easier using the `Makefile` like below

```makefile
build:
  python better-sam.py better-templates.yaml output/template.yaml
  sam build -t output/template.yaml

deploy:
  sam deploy -t output/template.yaml --guided

build-prod:
  python better-sam.py better-templates.yaml output/template.yaml
  sam build -t output/template.yaml --config-env prod # if you are using the `samconfig.toml` file

deploy-prod:
  sam deploy -t output/template.yaml --guided --config-env prod # if you are using the `samconfig.toml` file
```

## Contributing

Contributions are welcome! I know this script is a very minimal but i am looking forward to make large SAM templates more easier to manage. Feel free to open an issue to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE).**