import os
import boto3
from dotenv import load_dotenv
from typing import Optional, Any, Dict
from .exceptions import AWSAuthenticationError

class AWSAuthenticator:
    def __init__(self, profile_name: Optional[str] = None, env_file: Optional[str] = None):
        """
        Initialize AWS authenticator with optional profile name or environment file.
        
        Args:
            profile_name (str, optional): AWS profile name to use
            env_file (str, optional): Path to .env file containing AWS credentials
        """
        self.profile_name = profile_name
        if env_file:
            load_dotenv(env_file)
        
        self.session = self._create_session()

    def _create_session(self) -> boto3.Session:
        """Create an AWS session using available credentials."""
        try:
            # If profile name is provided, use it
            if self.profile_name:
                return boto3.Session(profile_name=self.profile_name)
            
            # Check for explicit credentials in environment
            if all(key in os.environ for key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']):
                return boto3.Session(
                    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                    aws_session_token=os.environ.get('AWS_SESSION_TOKEN')
                )
            # Check for explicit credentials in environment variables
            if 'AWS_PROFILE' in os.environ:
                return boto3.Session(profile_name=os.environ['AWS_PROFILE'])
            # Fall back to default credentials (EC2/Lambda role, default profile, etc.)
            return boto3.Session()
            
        except Exception as e:
            raise AWSAuthenticationError(f"Failed to create AWS session: {str(e)}")

    def get_client(self, service_name: str, region_name: Optional[str] = None) -> Any:
        """
        Get a boto3 client for the specified AWS service.
        
        Args:
            service_name (str): Name of the AWS service (e.g., 's3', 'dynamodb', 'ec2')
            region_name (str, optional): AWS region name
            
        Returns:
            boto3.client: Authenticated client for the specified service
        """
        try:
            return self.session.client(service_name, region_name=region_name)
        except Exception as e:
            raise AWSAuthenticationError(f"Failed to create client for {service_name}: {str(e)}")

    def get_resource(self, service_name: str, region_name: Optional[str] = None) -> Any:
        """
        Get a boto3 resource for the specified AWS service.
        
        Args:
            service_name (str): Name of the AWS service (e.g., 's3', 'dynamodb', 'ec2')
            region_name (str, optional): AWS region name
            
        Returns:
            boto3.resource: Authenticated resource for the specified service
        """
        try:
            return self.session.resource(service_name, region_name=region_name)
        except Exception as e:
            raise AWSAuthenticationError(f"Failed to create resource for {service_name}: {str(e)}")

    def get_credentials(self) -> Dict[str, str]:
        """
        Get the current AWS credentials.
        
        Returns:
            dict: Dictionary containing AWS credentials
        """
        try:
            credentials = self.session.get_credentials()
            if credentials is None:
                raise AWSAuthenticationError("No AWS credentials found")
            
            frozen_credentials = credentials.get_frozen_credentials()
            return {
                'aws_access_key_id': frozen_credentials.access_key,
                'aws_secret_access_key': frozen_credentials.secret_key,
                'aws_session_token': frozen_credentials.token
            }
        except Exception as e:
            raise AWSAuthenticationError(f"Failed to retrieve credentials: {str(e)}")