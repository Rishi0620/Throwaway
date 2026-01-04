# Quick Start Guide

Get the Trading Scripts Web App running in 10 minutes.

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] AWS account with EC2, S3 permissions
- [ ] Trading scripts in parent directory (india_daily.py, etc.)

## Steps

### 1. Configure Environment (2 min)

```bash
cd webapp/backend
cp .env.example .env
```

Edit `.env` and set these **required** values:
- `EC2_KEY_PAIR` - Your AWS key pair name
- `EC2_SECURITY_GROUP` - Your security group ID (sg-xxxxx)
- `EC2_IAM_ROLE` - IAM role name (create if needed)

### 2. Run Setup (3 min)

```bash
cd ../deploy
./setup.sh
```

This uploads scripts to S3 and installs dependencies.

### 3. Update AWS Config (2 min)

Edit `backend/aws_runner.py`:

Line 116: Replace `'your-key-pair'` with your actual key pair name
Line 117: Replace `'sg-0123456789abcdef0'` with your security group ID

### 4. Start Backend (1 min)

```bash
cd ../backend
python3 app.py
```

You should see:
```
Starting Trading Scripts Web App on port 5000
Available scripts: india_daily, us_rolling_weekly, ...
```

### 5. Test Frontend (2 min)

Open `webapp/frontend/index.html` in your browser.

1. Enter your email
2. Click any script button
3. You should see "Script launched successfully!"

### 6. Verify Execution

Check spot instance was created:
```bash
aws ec2 describe-spot-instance-requests --region us-east-1 | grep -A 5 webapp
```

## Creating Required AWS Resources

### IAM Role (if you don't have one)

```bash
# Create role
aws iam create-role \
  --role-name TradingModelsEC2Role \
  --assume-role-policy-document file://trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name TradingModelsEC2Role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Create instance profile
aws iam create-instance-profile --instance-profile-name TradingModelsEC2Role
aws iam add-role-to-instance-profile \
  --instance-profile-name TradingModelsEC2Role \
  --role-name TradingModelsEC2Role
```

Create `trust-policy.json`:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "ec2.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
```

### Security Group (if you don't have one)

```bash
# Create security group
aws ec2 create-security-group \
  --group-name trading-scripts-sg \
  --description "Security group for trading scripts" \
  --region us-east-1

# Allow all outbound (default)
# No inbound rules needed
```

### Key Pair (if you don't have one)

```bash
aws ec2 create-key-pair \
  --key-name trading-scripts-key \
  --query 'KeyMaterial' \
  --output text > trading-scripts-key.pem

chmod 400 trading-scripts-key.pem
```

## Testing Without AWS

To test the backend API without launching instances:

1. Comment out the spot instance launch in `backend/app.py`
2. Return a mock success response
3. Test the frontend interaction

## Common Issues

### "No module named 'boto3'"
```bash
cd backend
pip3 install -r requirements.txt
```

### "An error occurred (UnauthorizedOperation) when calling..."
Run `aws configure` and set your credentials.

### "InvalidKeyPair.NotFound"
Update `EC2_KEY_PAIR` in `.env` with a valid key pair name from your AWS account.

### "InvalidGroup.NotFound"
Update `EC2_SECURITY_GROUP` in `.env` with a valid security group ID.

### Frontend can't connect to backend
- Ensure backend is running on port 5000
- Check browser console for errors
- Update `API_BASE_URL` in `frontend/script.js` if needed

## Next Steps

Once working locally:
1. Deploy backend to a server (see README.md)
2. Set up a domain name
3. Configure SSL/HTTPS
4. Set up monitoring

## Need Help?

- Check the main [README.md](README.md) for detailed docs
- Review [AWS documentation](https://docs.aws.amazon.com/)
- Check CloudWatch logs for instance execution details
