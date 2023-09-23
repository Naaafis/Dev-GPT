#!/bin/bash

# AWS Configuration
KEY_NAME="my-key-pair"

# Check if the private key file already exists
PRIVATE_KEY_FILE="$PWD/${KEY_NAME}.pem"

if [ -f "$PRIVATE_KEY_FILE" ]; then
    echo -e "Private key file already exists: $PRIVATE_KEY_FILE\n"
else
    # Retrieve the private key material
    PRIVATE_KEY_MATERIAL=$(aws ec2 create-key-pair --key-name "$KEY_NAME" --query 'KeyMaterial' --output text)

    # Save the private key material to a file
    echo "$PRIVATE_KEY_MATERIAL" > "$PRIVATE_KEY_FILE"

    # Set appropriate permissions on the private key file
    chmod 400 "$PRIVATE_KEY_FILE"

    echo -e "Private key for key pair '$KEY_NAME' saved to '$PRIVATE_KEY_FILE'. Keep it secure.\n"
fi
