#!/bin/bash

# Check if the AWS CLI is already installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Installing..."
    # Install the AWS CLI using pip (Python package manager)
    pip install awscli
fi

echo "Configuring AWS CLI..."

# Configure AWS credentials
if !(grep -q "aws_access_key_id" ~/.aws/credentials); then
    # Configure AWS credentials
    read -p "Enter your AWS Access Key ID: " AWS_ACCESS_KEY_ID
    read -p "Enter your AWS Secret Access Key: " AWS_SECRET_ACCESS_KEY

    aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
    aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
fi

# Configure AWS region
if !(grep -q "region" ~/.aws/config); then
    read -p "Enter your default AWS region (e.g., us-east-1): " AWS_REGION
    aws configure set default.region "$AWS_REGION"
fi

echo -e "AWS CLI has been configured with your credentials and region.\n"