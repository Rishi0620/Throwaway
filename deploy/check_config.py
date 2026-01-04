#!/usr/bin/env python3
"""
Configuration checker for Trading Scripts Web App
Verifies AWS setup and configuration before deployment
"""

import os
import sys
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from pathlib import Path

# Colors for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if os.path.exists(filepath):
        print_success(f"{description} exists: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    print_header("Checking Environment Configuration")

    env_path = Path(__file__).parent.parent / "backend" / ".env"

    if not check_file_exists(env_path, ".env file"):
        print_warning("Run: cp backend/.env.example backend/.env")
        return False

    # Load and check required variables
    required_vars = ['S3_BUCKET', 'EC2_KEY_PAIR', 'EC2_SECURITY_GROUP', 'EC2_IAM_ROLE']
    missing_vars = []

    with open(env_path) as f:
        env_content = f.read()
        for var in required_vars:
            if var not in env_content or f'{var}=your-' in env_content or f'{var}=sg-0123456789' in env_content:
                missing_vars.append(var)

    if missing_vars:
        print_error(f"Please set these variables in .env: {', '.join(missing_vars)}")
        return False
    else:
        print_success("All required environment variables are set")
        return True

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    print_header("Checking AWS Credentials")

    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print_success(f"AWS credentials configured")
        print(f"  Account: {identity['Account']}")
        print(f"  User: {identity['Arn']}")
        return True
    except NoCredentialsError:
        print_error("AWS credentials not found")
        print_warning("Run: aws configure")
        return False
    except Exception as e:
        print_error(f"AWS credentials check failed: {e}")
        return False

def check_s3_access(bucket_name='trading-models-automation-1761354723'):
    """Check if S3 bucket is accessible"""
    print_header("Checking S3 Access")

    try:
        s3 = boto3.client('s3', region_name='us-east-1')

        # Check if bucket exists
        try:
            s3.head_bucket(Bucket=bucket_name)
            print_success(f"S3 bucket accessible: {bucket_name}")
        except ClientError:
            print_warning(f"Bucket {bucket_name} not found, will be created during setup")
            return True

        # Check if scripts directory exists
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix='scripts/', MaxKeys=1)
        if 'Contents' in response:
            print_success("Scripts directory exists in S3")
        else:
            print_warning("Scripts directory empty (run setup.sh to upload)")

        return True

    except Exception as e:
        print_error(f"S3 access check failed: {e}")
        return False

def check_ec2_permissions():
    """Check if EC2 permissions are available"""
    print_header("Checking EC2 Permissions")

    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')

        # Check describe permissions
        ec2.describe_regions()
        print_success("EC2 describe permissions OK")

        # Check spot instance request permissions (this will fail if no permission, succeed if permission exists)
        try:
            ec2.describe_spot_instance_requests(MaxResults=1)
            print_success("EC2 spot instance permissions OK")
        except ClientError as e:
            if 'UnauthorizedOperation' in str(e):
                print_error("No permission to manage spot instances")
                return False

        return True

    except Exception as e:
        print_error(f"EC2 permissions check failed: {e}")
        return False

def check_key_pair(key_name=None):
    """Check if EC2 key pair exists"""
    if not key_name:
        print_warning("Skipping key pair check (not configured yet)")
        return True

    print_header("Checking EC2 Key Pair")

    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')
        response = ec2.describe_key_pairs(KeyNames=[key_name])

        if response['KeyPairs']:
            print_success(f"Key pair exists: {key_name}")
            return True
        else:
            print_error(f"Key pair not found: {key_name}")
            return False

    except ClientError as e:
        if 'InvalidKeyPair.NotFound' in str(e):
            print_error(f"Key pair not found: {key_name}")
            print_warning(f"Create it with: aws ec2 create-key-pair --key-name {key_name}")
        else:
            print_error(f"Key pair check failed: {e}")
        return False

def check_security_group(sg_id=None):
    """Check if security group exists"""
    if not sg_id or sg_id == 'sg-0123456789abcdef0':
        print_warning("Skipping security group check (not configured yet)")
        return True

    print_header("Checking Security Group")

    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')
        response = ec2.describe_security_groups(GroupIds=[sg_id])

        if response['SecurityGroups']:
            sg = response['SecurityGroups'][0]
            print_success(f"Security group exists: {sg_id}")
            print(f"  Name: {sg['GroupName']}")
            print(f"  VPC: {sg.get('VpcId', 'N/A')}")

            # Check if it has outbound rules
            if sg['IpPermissionsEgress']:
                print_success("Outbound rules configured")
            else:
                print_warning("No outbound rules (may cause issues)")

            return True
        else:
            print_error(f"Security group not found: {sg_id}")
            return False

    except ClientError as e:
        if 'InvalidGroup.NotFound' in str(e):
            print_error(f"Security group not found: {sg_id}")
        else:
            print_error(f"Security group check failed: {e}")
        return False

def check_iam_role(role_name=None):
    """Check if IAM role exists"""
    if not role_name or role_name == 'TradingModelsEC2Role':
        print_warning("Skipping IAM role check (may not exist yet)")
        return True

    print_header("Checking IAM Role")

    try:
        iam = boto3.client('iam')
        role = iam.get_role(RoleName=role_name)

        print_success(f"IAM role exists: {role_name}")

        # Check instance profile
        try:
            profile = iam.get_instance_profile(InstanceProfileName=role_name)
            print_success(f"Instance profile exists: {role_name}")
        except ClientError:
            print_warning(f"Instance profile not found for role: {role_name}")
            print_warning(f"Create it with: aws iam create-instance-profile --instance-profile-name {role_name}")

        return True

    except ClientError as e:
        if 'NoSuchEntity' in str(e):
            print_error(f"IAM role not found: {role_name}")
            print_warning("See QUICKSTART.md for creation instructions")
        else:
            print_error(f"IAM role check failed: {e}")
        return False

def check_trading_scripts():
    """Check if trading scripts exist in parent directory"""
    print_header("Checking Trading Scripts")

    parent_dir = Path(__file__).parent.parent.parent
    scripts = [
        'india_daily.py',
        'us_rolling_weekly.py',
        'india_weekly_fno.py',
        'india_weekly_nse500.py',
        'us_pairs_15.py',
        'requirements.txt'
    ]

    all_exist = True
    for script in scripts:
        script_path = parent_dir / script
        if script_path.exists():
            print_success(f"{script} found")
        else:
            print_warning(f"{script} not found (optional)")
            if script == 'requirements.txt':
                all_exist = False

    return all_exist

def main():
    print(f"\n{BLUE}Trading Scripts Web App - Configuration Checker{RESET}\n")

    results = {
        'Environment': check_env_file(),
        'AWS Credentials': check_aws_credentials(),
        'S3 Access': check_s3_access(),
        'EC2 Permissions': check_ec2_permissions(),
        'Trading Scripts': check_trading_scripts(),
    }

    # Load env variables for additional checks
    env_path = Path(__file__).parent.parent / "backend" / ".env"
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)

        key_pair = os.getenv('EC2_KEY_PAIR')
        sg_id = os.getenv('EC2_SECURITY_GROUP')
        iam_role = os.getenv('EC2_IAM_ROLE')

        results['Key Pair'] = check_key_pair(key_pair)
        results['Security Group'] = check_security_group(sg_id)
        results['IAM Role'] = check_iam_role(iam_role)

    # Summary
    print_header("Configuration Check Summary")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for check, result in results.items():
        if result:
            print_success(check)
        else:
            print_error(check)

    print(f"\n{passed}/{total} checks passed\n")

    if passed == total:
        print_success("All checks passed! You're ready to run setup.sh")
        return 0
    else:
        print_warning("Some checks failed. Please fix the issues above before proceeding.")
        print_warning("See QUICKSTART.md for detailed setup instructions.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
