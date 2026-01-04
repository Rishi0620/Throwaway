#!/bin/bash

# Setup script for Trading Scripts Web App
# This script prepares the environment and uploads necessary files to S3

set -e

echo "================================================"
echo "Trading Scripts Web App - Setup"
echo "================================================"
echo ""

# Check if running from correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "Error: Please run this script from the webapp directory"
    exit 1
fi

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "Error: AWS CLI is not installed"
    echo "Install it from: https://aws.amazon.com/cli/"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Prerequisites check passed"
echo ""

# Load environment variables
if [ -f "backend/.env" ]; then
    export $(cat backend/.env | grep -v '^#' | xargs)
    echo "✓ Loaded environment variables from backend/.env"
else
    echo "Warning: backend/.env not found"
    echo "Creating from .env.example..."
    cp backend/.env.example backend/.env
    echo ""
    echo "Please edit backend/.env and update the following:"
    echo "  - EC2_KEY_PAIR (your AWS key pair name)"
    echo "  - EC2_SECURITY_GROUP (your security group ID)"
    echo "  - EC2_IAM_ROLE (IAM role with S3 and EC2 permissions)"
    echo ""
    read -p "Press Enter after updating backend/.env to continue..."
fi

S3_BUCKET=${S3_BUCKET:-"trading-models-automation-1761354723"}

echo ""
echo "================================================"
echo "Step 1: Upload trading scripts to S3"
echo "================================================"
echo ""

# Create scripts directory in S3
echo "Creating S3 bucket structure..."
aws s3 mb s3://$S3_BUCKET 2>/dev/null || echo "Bucket already exists"

# Upload original trading scripts from parent directory
echo "Uploading original trading scripts..."
cd ..

aws s3 cp india_daily.py s3://$S3_BUCKET/scripts/ || echo "Warning: india_daily.py not found"
aws s3 cp us_rolling_weekly.py s3://$S3_BUCKET/scripts/ || echo "Warning: us_rolling_weekly.py not found"
aws s3 cp india_weekly_fno.py s3://$S3_BUCKET/scripts/ || echo "Warning: india_weekly_fno.py not found"
aws s3 cp india_weekly_nse500.py s3://$S3_BUCKET/scripts/ || echo "Warning: india_weekly_nse500.py not found"
aws s3 cp us_pairs_15.py s3://$S3_BUCKET/scripts/ || echo "Warning: us_pairs_15.py not found"
aws s3 cp garman_klass_volatility_target_sl.py s3://$S3_BUCKET/scripts/ || echo "Warning: garman_klass_volatility_target_sl.py not found"

# Upload wrapper script
cd webapp
echo "Uploading wrapper script..."
aws s3 cp backend/scripts/script_wrapper.py s3://$S3_BUCKET/scripts/

# Upload requirements
echo "Uploading requirements.txt..."
aws s3 cp ../requirements.txt s3://$S3_BUCKET/scripts/ || echo "Warning: requirements.txt not found in parent directory"

echo "✓ Scripts uploaded to S3"

echo ""
echo "================================================"
echo "Step 2: Install backend dependencies"
echo "================================================"
echo ""

cd backend
python3 -m pip install -r requirements.txt
echo "✓ Backend dependencies installed"

echo ""
echo "================================================"
echo "Step 3: Verify AWS permissions"
echo "================================================"
echo ""

# Test S3 access
echo "Testing S3 access..."
aws s3 ls s3://$S3_BUCKET/scripts/ > /dev/null && echo "✓ S3 access confirmed"

# Check EC2 permissions
echo "Testing EC2 access..."
aws ec2 describe-regions --region us-east-1 > /dev/null && echo "✓ EC2 access confirmed"

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Update backend/aws_runner.py with your:"
echo "   - KeyName (line 116)"
echo "   - SecurityGroupIds (line 117)"
echo ""
echo "2. Start the backend server:"
echo "   cd backend"
echo "   python3 app.py"
echo ""
echo "3. Open the frontend:"
echo "   Open frontend/index.html in your browser"
echo "   (for local testing)"
echo ""
echo "4. For production deployment, see README.md"
echo ""
