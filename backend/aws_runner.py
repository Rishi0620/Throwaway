"""
AWS EC2 Spot Instance Launcher
Launches spot instances to run trading scripts and auto-terminates them
"""

import boto3
import base64
import os
from datetime import datetime

class SpotInstanceRunner:
    def __init__(self):
        # Initialize AWS client with credentials from environment
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')

        if aws_access_key and aws_secret_key:
            self.ec2_client = boto3.client(
                'ec2',
                region_name=aws_region,
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key
            )
        else:
            # Fall back to default credentials
            self.ec2_client = boto3.client('ec2', region_name=aws_region)

        self.s3_bucket = os.getenv('S3_BUCKET', 'trading-models-automation-1761354723')

    def create_user_data_script(self, script_name, user_email):
        """
        Create the user data script that will run on the EC2 instance
        This script:
        1. Downloads the original trading scripts from S3
        2. Downloads the wrapper script
        3. Runs the wrapper with user's email
        4. Terminates the instance when done
        """

        user_data = f'''#!/bin/bash
# Don't exit on errors - we want to see all output and upload logs even if scripts fail
exec > >(tee /var/log/user-data.log)
exec 2>&1

echo "========== TRADING SCRIPT STARTING =========="
date

# Update system (Amazon Linux 2023)
yum update -y

# Install Python 3.11 and pip
yum install -y python3.11 python3.11-pip git

# Set python3.11 as default
alternatives --set python3 /usr/bin/python3.11 || true

# Create working directory
mkdir -p /home/ec2-user/trading-models
cd /home/ec2-user/trading-models

# Download webapp-modified scripts from S3
echo "Downloading scripts from S3..."
aws s3 cp s3://{self.s3_bucket}/scripts/india_daily_webapp.py ./ || echo "india_daily.py not needed"
aws s3 cp s3://{self.s3_bucket}/scripts/us_rolling_weekly_webapp.py ./ || echo "us_rolling_weekly.py not needed"
aws s3 cp s3://{self.s3_bucket}/scripts/india_weekly_fno_webapp.py ./ || echo "india_weekly_fno.py not needed"
aws s3 cp s3://{self.s3_bucket}/scripts/india_weekly_nse500_webapp.py ./ || echo "india_weekly_nse500.py not needed"
aws s3 cp s3://{self.s3_bucket}/scripts/us_pairs_15_webapp.py ./ || echo "us_pairs_15.py not needed"
aws s3 cp s3://{self.s3_bucket}/scripts/garman_klass_volatility_target_sl.py ./ || true

# Download requirements
aws s3 cp s3://{self.s3_bucket}/scripts/requirements.txt ./

# Install dependencies (ignore conflicts with system packages)
echo "Installing Python dependencies..."
python3.11 -m pip install -r requirements.txt --ignore-installed || echo "Pip install completed with warnings (non-fatal)"

# Set email credentials
export SENDER_EMAIL="signals@plutusadvisors.ai"
export SENDER_PASSWORD="Plutus!23@advisors"

# Run the modified script directly (no wrapper needed)
echo "Running {script_name}..."
python3.11 {script_name}_webapp.py

echo "========== TRADING SCRIPT COMPLETE =========="
date

# Terminate this instance
echo "Terminating instance..."
INSTANCE_ID=$(ec2-metadata --instance-id | cut -d " " -f 2)
echo "Instance ID: $INSTANCE_ID"
aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region us-east-1 || echo "Failed to terminate instance (will timeout and terminate via spot pricing)"

'''
        return base64.b64encode(user_data.encode()).decode()

    def launch_spot_instance(self, script_name, user_email):
        """
        Launch an EC2 spot instance to run the trading script
        Returns: Instance ID
        """

        # Determine instance size based on script
        instance_config = {
            'india_daily': {'type': 't3.large', 'timeout': 60},
            'us_rolling_weekly': {'type': 't3.xlarge', 'timeout': 90},
            'india_weekly_fno': {'type': 't3.large', 'timeout': 60},
            'india_weekly_nse500': {'type': 't3.large', 'timeout': 60},
            'us_pairs_15': {'type': 't3.medium', 'timeout': 45}
        }

        config = instance_config.get(script_name, {'type': 't3.medium', 'timeout': 60})

        user_data_b64 = self.create_user_data_script(script_name, user_email)

        # Get configuration from environment
        key_pair = os.getenv('EC2_KEY_PAIR', 'example')
        security_group = os.getenv('EC2_SECURITY_GROUP', 'sg-08b848ee7c691a9f3')
        iam_role = os.getenv('EC2_IAM_ROLE', 'TradingModelsEC2Role')

        # Launch spot instance
        try:
            response = self.ec2_client.request_spot_instances(
                SpotPrice='0.10',  # Max price we're willing to pay
                InstanceCount=1,
                Type='one-time',
                LaunchSpecification={
                    'ImageId': 'ami-07d1f1c6865c6b0e7',  # Amazon Linux 2023 in us-east-1
                    'InstanceType': config['type'],
                    'KeyName': key_pair,
                    'UserData': user_data_b64,
                    'IamInstanceProfile': {
                        'Name': iam_role
                    },
                    'SecurityGroupIds': [security_group],
                    'BlockDeviceMappings': [
                        {
                            'DeviceName': '/dev/sda1',
                            'Ebs': {
                                'VolumeSize': 20,
                                'VolumeType': 'gp3',
                                'DeleteOnTermination': True
                            }
                        }
                    ]
                }
            )

            spot_request_id = response['SpotInstanceRequests'][0]['SpotInstanceRequestId']

            print(f"Spot instance request created: {spot_request_id}")

            # Wait for spot request to be fulfilled (optional, with timeout)
            waiter = self.ec2_client.get_waiter('spot_instance_request_fulfilled')

            try:
                waiter.wait(
                    SpotInstanceRequestIds=[spot_request_id],
                    WaiterConfig={'Delay': 5, 'MaxAttempts': 24}  # Wait up to 2 minutes
                )

                # Get the instance ID
                spot_request = self.ec2_client.describe_spot_instance_requests(
                    SpotInstanceRequestIds=[spot_request_id]
                )
                instance_id = spot_request['SpotInstanceRequests'][0].get('InstanceId')

                # Tag the instance
                if instance_id:
                    try:
                        self.ec2_client.create_tags(
                            Resources=[instance_id],
                            Tags=[
                                {'Key': 'Name', 'Value': f'webapp-{script_name}-{datetime.now().strftime("%Y%m%d-%H%M%S")}'},
                                {'Key': 'Script', 'Value': script_name},
                                {'Key': 'UserEmail', 'Value': user_email},
                                {'Key': 'Source', 'Value': 'webapp'},
                                {'Key': 'AutoTerminate', 'Value': 'true'}
                            ]
                        )
                        print(f"Instance tagged: {instance_id}")
                    except Exception as tag_error:
                        print(f"Warning: Failed to tag instance: {tag_error}")

                return {
                    'success': True,
                    'spot_request_id': spot_request_id,
                    'instance_id': instance_id,
                    'message': f'Spot instance launched successfully for {script_name}'
                }

            except Exception as wait_error:
                print(f"Spot request created but not yet fulfilled: {wait_error}")
                return {
                    'success': True,
                    'spot_request_id': spot_request_id,
                    'instance_id': None,
                    'message': f'Spot instance request submitted for {script_name}, waiting for fulfillment'
                }

        except Exception as e:
            print(f"Error launching spot instance: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_instance_status(self, instance_id):
        """Check the status of a running instance"""
        try:
            response = self.ec2_client.describe_instances(InstanceIds=[instance_id])
            if response['Reservations']:
                instance = response['Reservations'][0]['Instances'][0]
                return {
                    'state': instance['State']['Name'],
                    'launch_time': instance.get('LaunchTime'),
                    'public_ip': instance.get('PublicIpAddress')
                }
        except Exception as e:
            return {'error': str(e)}
