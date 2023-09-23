#!/bin/bash

AMI_ID="ami-051f7e7f6c2f40dc1" # TODO: Adjust AMI and Instance type to suit user needs
REGION=$(aws configure get region)
INSTANCE_NAME="MyInstance"

# Check if the instance is already running
CURRENT_STATE=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=$INSTANCE_NAME" \
  --query "Reservations[0].Instances[0].State.Name" \
  --output text 2>/dev/null)

if [ "$CURRENT_STATE" == None  ]; then
    # Launch EC2 instance
    INSTANCE_ID=$(aws ec2 run-instances \
      --region $REGION \
      --image-id $AMI_ID \
      --key-name $KEY_NAME \
      --security-group-ids $SECURITY_GROUP_ID \
      --query 'Instances[0].InstanceId' \
      --output text)

    # Wait for the instance to be in the 'running' state
    aws ec2 wait instance-running --region $REGION --instance-ids $INSTANCE_ID

    # Add a name tag to the instance for easy identification
    aws ec2 create-tags --region $REGION --resources $INSTANCE_ID --tags Key=Name,Value="$INSTANCE_NAME"

    # Print the instance ID and public IP address
    echo "EC2 instance $INSTANCE_ID created successfully."
else
    INSTANCE_ID=$(aws ec2 describe-instances \
      --filters "Name=tag:Name,Values=$INSTANCE_NAME" \
      --query "Reservations[0].Instances[0].InstanceId" \
      --output text 2>/dev/null)
      
    if [ "$CURRENT_STATE" == "stopped"  ]; then
        # Start EC2 instance
        aws ec2 start-instances --instance-ids $INSTANCE_ID
        
        # Wait for the instance to be in the 'running' state
        aws ec2 wait instance-running --region $REGION --instance-ids $INSTANCE_ID
    fi
fi

# Get the public IP address of the instance
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

# SSH into the instance
echo "SSHing into the instance..."
ssh -i my-key-pair.pem ec2-user@"$PUBLIC_IP"
