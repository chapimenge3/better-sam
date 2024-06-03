# Example: Running better-sam.py

This is an example project that demonstrates how to run `better-sam.py` for splitting a large AWS SAM template into multiple files. The `better-sam.py` script is used to assemble the SAM template from multiple files and generate a single output file that can be used with the AWS SAM CLI.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- [better-sam.py](https://github.com/chapimenge3/better-sam/blob/main/better-sam.py)

## Usage

To run the `better-sam.py` script, use the following command:

```bash
pyton better-sam.py
```

This will generate a single SAM template file named `template.yaml` in the current directory.

Now you can just use the generated `template.yaml` file with the AWS SAM CLI to deploy your serverless application.

```bash
sam build -t template.yaml
sam deploy -t template.yaml
```

That's it! You have successfully split your AWS SAM template into multiple files using the `better-sam.py` script.

