# Trading Scripts Web App

A simple web application that allows users to run trading signal scripts on-demand via AWS spot instances. Users enter their email and click a button to run any of the available trading scripts. The results are automatically emailed to them when complete.

## Features

- **5 Trading Scripts Available:**
  - India Daily Equity
  - US Rolling Weekly
  - India Weekly F&O
  - India Weekly NSE500
  - US Pairs 15-Min

- **On-Demand Execution:** Run scripts whenever you want, not just on schedule
- **Email Delivery:** Results sent directly to user's email
- **Auto-Scaling:** Uses AWS spot instances that auto-terminate after completion
- **Cost-Effective:** Only pay for compute time when scripts are running
- **Simple UI:** Single-page interface with clear buttons for each script

## Architecture

```
User clicks button → Flask API → AWS Spot Instance → Script runs → Email sent → Instance terminates
```

### Components

1. **Frontend** (`frontend/`): Simple HTML/CSS/JS interface
2. **Backend** (`backend/`): Flask API server
3. **AWS Integration**: Boto3 for EC2 spot instance management
4. **Email**: Office 365 SMTP for sending results
5. **Storage**: S3 for script storage

## Prerequisites

- Python 3.8+
- AWS Account with:
  - EC2 permissions (launch spot instances)
  - S3 permissions (read/write)
  - IAM role for EC2 instances
- AWS CLI configured
- Trading scripts from parent directory

## Setup

### 1. Configure Environment

```bash
cd webapp
cp backend/.env.example backend/.env
```

Edit `backend/.env` and update:
- `EC2_KEY_PAIR`: Your AWS key pair name
- `EC2_SECURITY_GROUP`: Your security group ID
- `S3_BUCKET`: Your S3 bucket name (default: trading-models-automation-1761354723)

### 2. Run Setup Script

```bash
cd deploy
./setup.sh
```

This script will:
- Upload trading scripts to S3
- Upload wrapper script to S3
- Install backend dependencies
- Verify AWS permissions

### 3. Update AWS Configuration

Edit `backend/aws_runner.py` and update:
- Line 116: `KeyName` - your AWS key pair
- Line 117: `SecurityGroupIds` - your security group
- Line 119: `IamInstanceProfile.Name` - your IAM role name

### 4. Start Backend Server

```bash
cd backend
python3 app.py
```

Backend will start on http://localhost:5000

### 5. Open Frontend

For local testing:
```bash
# Open in browser
open frontend/index.html
```

For production, serve frontend with nginx/Apache or use a static hosting service.

## AWS Infrastructure Setup

### IAM Role

Create an IAM role named `TradingModelsEC2Role` with these policies:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::trading-models-automation-1761354723",
        "arn:aws:s3:::trading-models-automation-1761354723/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:TerminateInstances",
        "ec2:DescribeInstances"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "ec2:ResourceTag/AutoTerminate": "true"
        }
      }
    }
  ]
}
```

### Security Group

Create a security group with:
- **Outbound:** Allow all traffic (for downloading packages and sending emails)
- **Inbound:** No inbound rules needed (scripts don't listen on ports)

### EC2 Key Pair

Create or use an existing EC2 key pair for SSH access (if needed for debugging).

## Usage

### Running Scripts

1. Open the web app in your browser
2. Enter your email address
3. Click the button for the script you want to run
4. Wait for confirmation
5. Check your email (30-90 minutes later)

### API Endpoints

#### Get Available Scripts
```bash
GET /api/scripts
```

Response:
```json
{
  "scripts": {
    "india_daily": {
      "name": "India Daily Equity",
      "description": "Daily Indian equity signals (Mon-Thu)",
      "estimated_time": "45-60 min"
    },
    ...
  }
}
```

#### Run Script
```bash
POST /api/run
Content-Type: application/json

{
  "script_name": "india_daily",
  "user_email": "user@example.com"
}
```

Response:
```json
{
  "success": true,
  "message": "Script india_daily started successfully",
  "spot_request_id": "sir-abc123",
  "instance_id": "i-0123456789",
  "estimated_time": "45-60 min"
}
```

#### Health Check
```bash
GET /api/health
```

## Folder Structure

```
webapp/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── aws_runner.py             # Spot instance launcher
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment template
│   └── scripts/
│       └── script_wrapper.py     # Wrapper for running scripts
│
├── frontend/
│   ├── index.html                # Main page
│   ├── style.css                 # Styling
│   └── script.js                 # Frontend logic
│
├── deploy/
│   ├── setup.sh                  # Initial setup script
│   └── upload_scripts.sh         # Upload scripts to S3
│
└── README.md                     # This file
```

## Deployment

### Option 1: Simple VPS Deployment

1. **Deploy to any VPS** (AWS EC2, DigitalOcean, etc.)

```bash
# On server
git clone <your-repo>
cd webapp
./deploy/setup.sh
cd backend
pip install -r requirements.txt

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Serve frontend with nginx**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/webapp/frontend;
        index index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 2: AWS Elastic Beanstalk

1. Create `application.py` in backend:
```python
from app import app as application

if __name__ == "__main__":
    application.run()
```

2. Deploy:
```bash
cd backend
eb init -p python-3.9 trading-scripts-app
eb create trading-scripts-env
```

### Option 3: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY frontend/ /app/static/

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t trading-scripts-app .
docker run -p 5000:5000 --env-file backend/.env trading-scripts-app
```

## Updating Scripts

When you update the original trading scripts, upload them to S3:

```bash
cd deploy
./upload_scripts.sh
```

## Monitoring

### View Running Instances

```bash
aws ec2 describe-instances \
  --filters "Name=tag:Source,Values=webapp" "Name=instance-state-name,Values=running,pending" \
  --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==`Script`].Value|[0],State.Name,LaunchTime]' \
  --output table
```

### View Spot Requests

```bash
aws ec2 describe-spot-instance-requests \
  --filters "Name=tag:Source,Values=webapp" \
  --query 'SpotInstanceRequests[*].[SpotInstanceRequestId,Status.Code,InstanceId,CreateTime]' \
  --output table
```

### Check S3 Scripts

```bash
aws s3 ls s3://trading-models-automation-1761354723/scripts/
```

## Troubleshooting

### Script Fails to Launch

1. Check AWS credentials: `aws sts get-caller-identity`
2. Verify S3 bucket exists: `aws s3 ls s3://your-bucket/`
3. Check IAM role permissions
4. Verify security group allows outbound traffic

### Email Not Received

1. Check spam/junk folder
2. Verify email credentials in `.env`
3. Check script logs in CloudWatch (if configured)
4. SSH into instance during execution to debug

### Instance Not Terminating

1. Check if script completed successfully
2. Verify IAM role has EC2 terminate permission
3. Manually terminate: `aws ec2 terminate-instances --instance-ids i-xxxxx`

### Frontend Can't Connect to Backend

1. Check backend is running: `curl http://localhost:5000/api/health`
2. Update `API_BASE_URL` in `frontend/script.js`
3. Check CORS settings in `backend/app.py`

## Cost Estimation

- **Spot Instance Cost**: ~$0.01-0.05 per script run
- **S3 Storage**: ~$0.023 per GB/month (scripts are small)
- **Data Transfer**: Minimal (<$0.01 per run)

**Monthly estimate for 100 runs**: ~$3-7

## Security Notes

- Email credentials are stored in environment variables (not committed to git)
- IAM role has minimal required permissions
- Security group blocks all inbound traffic
- Instances auto-terminate after completion
- Frontend validates email format
- Backend validates all inputs

## Support

For issues or questions:
1. Check CloudWatch logs for instance execution logs
2. Review S3 bucket for uploaded scripts
3. Test individual scripts locally before deploying
4. Check AWS service health dashboard

## License

Internal use only - Plutus Advisors

## Credits

Built for Plutus Advisors trading automation platform.
# Throwaway
