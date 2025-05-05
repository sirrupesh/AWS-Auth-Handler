from setuptools import setup, find_packages

setup(
    name="aws-auth-handler",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.26.0",
        "python-dotenv>=0.19.0",
        "botocore>=1.29.0",
    ],
    author="Rupesh Kumar Singh",
    author_email="5126966+sirrupesh@users.noreply.github.com",
    description="A flexible AWS authentication handler supporting multiple credential sources",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sirrupesh/AWS-Auth-Handler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)