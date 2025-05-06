# AWS Auth Handler

A flexible Python package for AWS authentication that supports multiple credential sources and seamlessly integrates with various AWS services.

## Features

- Support for multiple authentication methods:
  - AWS named profiles
  - Environment variables
  - .env files
  - IAM roles (EC2/Lambda)
  - Default credentials
- Easy integration with any AWS service
- Credential management and retrieval
- Type hints for better IDE support

## Installation

```bash
pip install aws-auth-handler
```

## Usage Examples

### Using Named Profile

```python
from aws_auth_handler import AWSAuthenticator

# Initialize with a specific AWS profile
auth = AWSAuthenticator(profile_name='dev')

# Get an S3 client
s3_client = auth.get_client('s3')

# Use the client
buckets = s3_client.list_buckets()
```

### Using Environment Variables

```python
from aws_auth_handler import AWSAuthenticator

# Initialize with .env file
auth = AWSAuthenticator(env_file='.env')

# Get a DynamoDB resource
dynamodb = auth.get_resource('dynamodb')

# Use the resource
table = dynamodb.Table('my-table')
```

### Using Default Credentials

```python
from aws_auth_handler import AWSAuthenticator

# Initialize with default credentials
auth = AWSAuthenticator()

# Get an EC2 client
ec2 = auth.get_client('ec2', region_name='us-west-2')

# Use the client
instances = ec2.describe_instances()
```

### Getting Current Credentials

```python
from aws_auth_handler import AWSAuthenticator

auth = AWSAuthenticator()
credentials = auth.get_credentials()
print(f"Access Key: {credentials['aws_access_key_id']}")
```

## Environment Variables

When using environment variables or .env files, the following variables are supported in order of priority:

1. First Priority - Direct Credentials:
```
AWS_ACCESS_KEY_ID=your_access_key           # Required for direct credential auth
AWS_SECRET_ACCESS_KEY=your_secret_key       # Required for direct credential auth
AWS_SESSION_TOKEN=your_session_token        # Optional
```

2. Second Priority - Named Profile:
```
AWS_PROFILE=your_profile_name               # Optional, used if direct credentials not present
```

3. Additional Configuration:
```
AWS_DEFAULT_REGION=your_region              # Optional
```

The authenticator will first check for AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY, then fall back to AWS_PROFILE if direct credentials are not available.

## Error Handling

```python
from aws_auth_handler import AWSAuthenticator, AWSAuthenticationError

try:
    auth = AWSAuthenticator(profile_name='non-existent-profile')
    s3 = auth.get_client('s3')
except AWSAuthenticationError as e:
    print(f"Authentication failed: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.