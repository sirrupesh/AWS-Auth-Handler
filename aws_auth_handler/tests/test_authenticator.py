import unittest
from unittest.mock import patch, MagicMock
import os
from aws_auth_handler import AWSAuthenticator, AWSAuthenticationError

class TestAWSAuthenticator(unittest.TestCase):
    def setUp(self):
        # Clear any environment variables before each test
        for key in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']:
            if key in os.environ:
                del os.environ[key]

    @patch('boto3.Session')
    def test_init_with_profile(self, mock_session):
        """Test initialization with profile name"""
        auth = AWSAuthenticator(profile_name='test-profile')
        mock_session.assert_called_once_with(profile_name='test-profile')

    @patch('boto3.Session')
    def test_init_with_env_vars(self, mock_session):
        """Test initialization with environment variables"""
        os.environ['AWS_ACCESS_KEY_ID'] = 'test-key'
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret'
        
        auth = AWSAuthenticator()
        mock_session.assert_called_once_with(
            aws_access_key_id='test-key',
            aws_secret_access_key='test-secret',
            aws_session_token=None
        )

    @patch('boto3.Session')
    def test_get_client(self, mock_session):
        """Test getting an AWS client"""
        mock_client = MagicMock()
        mock_session.return_value.client.return_value = mock_client
        
        auth = AWSAuthenticator()
        client = auth.get_client('s3', region_name='us-west-2')
        
        mock_session.return_value.client.assert_called_once_with(
            's3', region_name='us-west-2'
        )

    @patch('boto3.Session')
    def test_get_resource(self, mock_session):
        """Test getting an AWS resource"""
        mock_resource = MagicMock()
        mock_session.return_value.resource.return_value = mock_resource
        
        auth = AWSAuthenticator()
        resource = auth.get_resource('dynamodb', region_name='us-west-2')
        
        mock_session.return_value.resource.assert_called_once_with(
            'dynamodb', region_name='us-west-2'
        )

    @patch('boto3.Session')
    def test_get_credentials(self, mock_session):
        """Test getting AWS credentials"""
        mock_credentials = MagicMock()
        mock_credentials.access_key = 'test-key'
        mock_credentials.secret_key = 'test-secret'
        mock_credentials.token = 'test-token'
        
        mock_session.return_value.get_credentials.return_value.get_frozen_credentials.return_value = mock_credentials
        
        auth = AWSAuthenticator()
        credentials = auth.get_credentials()
        
        self.assertEqual(credentials['aws_access_key_id'], 'test-key')
        self.assertEqual(credentials['aws_secret_access_key'], 'test-secret')
        self.assertEqual(credentials['aws_session_token'], 'test-token')

    @patch('boto3.Session')
    def test_credentials_not_found(self, mock_session):
        """Test error handling when no credentials are found"""
        mock_session.return_value.get_credentials.return_value = None
        
        auth = AWSAuthenticator()
        with self.assertRaises(AWSAuthenticationError):
            auth.get_credentials()

if __name__ == '__main__':
    unittest.main()