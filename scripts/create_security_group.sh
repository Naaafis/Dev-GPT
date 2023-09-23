#!/bin/bash

# Your desired Security Group name
SECURITY_GROUP_NAME="launch-wizard-1"

# Check if the Security Group exists
echo "Checking if Security Group '$SECURITY_GROUP_NAME' exists..."

SECURITY_GROUP_ID=$(aws ec2 describe-security-groups \
  --filters "Name=group-name,Values=$SECURITY_GROUP_NAME" \
  --query "SecurityGroups[0].GroupId" \
  --output text)

if [ -z "$SECURITY_GROUP_ID" ]; then
  # Security Group doesn't exist; create a new one
  echo "Security Group '$SECURITY_GROUP_NAME' doesn't exist. Creating a new Security Group..."
  SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --region "$AWS_REGION" \
    --group-name "$SECURITY_GROUP_NAME" \
    --description "My Security Group" \
    --output text \
    --query "GroupId")
  # Add rules to the new Security Group
  aws ec2 authorize-security-group-ingress \
    --region "$AWS_REGION" \
    --group-id "$SECURITY_GROUP_ID" \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
  aws ec2 authorize-security-group-ingress \
    --region "$AWS_REGION" \3
    --group-id "$SECURITY_GROUP_ID" \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

  echo "New Security Group created with ID: $SECURITY_GROUP_ID"
else
  # Security Group exists; use the existing one
  echo "Security Group '$SECURITY_GROUP_NAME' already exists with ID: $SECURITY_GROUP_ID"
fi

echo -e "You can now use the SECURITY_GROUP_ID ($SECURITY_GROUP_ID) in your 'run-instances' command.\n"
