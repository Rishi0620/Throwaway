#!/bin/bash

# Quick script to upload/update trading scripts to S3
# Usage: ./upload_scripts.sh

set -e

# Load environment variables
if [ -f "../backend/.env" ]; then
    export $(cat ../backend/.env | grep -v '^#' | xargs)
fi

S3_BUCKET=${S3_BUCKET:-"trading-models-automation-1761354723"}

echo "Uploading scripts to s3://$S3_BUCKET/scripts/"
echo ""

# Go to parent directory where original scripts are
cd ../..

# Upload all trading scripts
echo "Uploading trading scripts..."
aws s3 cp india_daily.py s3://$S3_BUCKET/scripts/ && echo "✓ india_daily.py"
aws s3 cp us_rolling_weekly.py s3://$S3_BUCKET/scripts/ && echo "✓ us_rolling_weekly.py"
aws s3 cp india_weekly_fno.py s3://$S3_BUCKET/scripts/ && echo "✓ india_weekly_fno.py"
aws s3 cp india_weekly_nse500.py s3://$S3_BUCKET/scripts/ && echo "✓ india_weekly_nse500.py"
aws s3 cp us_pairs_15.py s3://$S3_BUCKET/scripts/ && echo "✓ us_pairs_15.py"
aws s3 cp garman_klass_volatility_target_sl.py s3://$S3_BUCKET/scripts/ && echo "✓ garman_klass_volatility_target_sl.py"
aws s3 cp requirements.txt s3://$S3_BUCKET/scripts/ && echo "✓ requirements.txt"

# Upload wrapper
cd webapp
aws s3 cp backend/scripts/script_wrapper.py s3://$S3_BUCKET/scripts/ && echo "✓ script_wrapper.py"

echo ""
echo "All scripts uploaded successfully!"
