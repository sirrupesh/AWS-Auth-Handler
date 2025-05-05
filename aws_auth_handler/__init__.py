from .authenticator import AWSAuthenticator
from .exceptions import AWSAuthenticationError

__version__ = '1.0.0'
__all__ = ['AWSAuthenticator', 'AWSAuthenticationError']