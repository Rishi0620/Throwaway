# Trading Scripts Web App - Project Summary

## What Was Built

A complete web application that allows users to run trading signal scripts on-demand via AWS spot instances. Users enter their email, click a button, and receive the results via email when the script completes.

## Features

✅ **5 Trading Scripts**
- India Daily Equity
- US Rolling Weekly
- India Weekly F&O
- India Weekly NSE500
- US Pairs 15-Min

✅ **Simple User Interface**
- Single-page web app
- Email input field
- One button per script
- Real-time status updates

✅ **AWS Integration**
- Launches spot instances on-demand
- Auto-terminates instances when done
- Cost-effective (only pay for runtime)
- Secure IAM role-based permissions

✅ **Email Delivery**
- Uses existing Office 365 SMTP
- Sends CSV results to user's email
- No need to wait for scheduled runs

## Project Structure

```
webapp/
├── backend/                        # Flask API server
│   ├── app.py                     # Main API endpoints
│   ├── aws_runner.py              # Spot instance launcher
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment template
│   └── scripts/
│       └── script_wrapper.py      # Script execution wrapper
│
├── frontend/                       # Web interface
│   ├── index.html                 # Main page
│   ├── style.css                  # Styling
│   └── script.js                  # Frontend logic
│
├── deploy/                         # Deployment tools
│   ├── setup.sh                   # Initial setup
│   ├── upload_scripts.sh          # Upload to S3
│   └── check_config.py            # Configuration checker
│
├── start_backend.sh               # Development server
├── start_production.sh            # Production server (Gunicorn)
├── .gitignore                     # Git ignore rules
│
├── README.md                      # Full documentation
├── QUICKSTART.md                  # Quick start guide
└── PROJECT_SUMMARY.md             # This file
```

## How It Works

1. **User visits web page** → Enters email and clicks script button
2. **Frontend calls API** → POST /api/run with script_name and email
3. **Backend launches spot instance** → EC2 instance with user data script
4. **Instance downloads scripts** → From S3 bucket
5. **Instance runs script** → Executes trading model
6. **Script emails results** → Sends CSV to user's email
7. **Instance terminates** → Automatically after completion

## Files Created

### Backend (Flask API)
- `backend/app.py` - Main Flask server with API endpoints
- `backend/aws_runner.py` - AWS EC2 spot instance management
- `backend/scripts/script_wrapper.py` - Wrapper to run scripts with custom email
- `backend/requirements.txt` - Python dependencies (Flask, boto3, etc.)
- `backend/.env.example` - Environment variables template

### Frontend (Web Interface)
- `frontend/index.html` - Single-page interface with buttons
- `frontend/style.css` - Modern, responsive styling
- `frontend/script.js` - API calls and user interactions

### Deployment & Setup
- `deploy/setup.sh` - Automated setup script (uploads to S3, installs deps)
- `deploy/upload_scripts.sh` - Quick script upload to S3
- `deploy/check_config.py` - Configuration verification tool
- `start_backend.sh` - Start development server
- `start_production.sh` - Start production server with Gunicorn

### Documentation
- `README.md` - Complete documentation (architecture, deployment, troubleshooting)
- `QUICKSTART.md` - 10-minute setup guide
- `PROJECT_SUMMARY.md` - This file
- `.gitignore` - Git ignore rules (prevents committing secrets)

## Technologies Used

**Backend:**
- Python 3.8+
- Flask (web framework)
- Boto3 (AWS SDK)
- Gunicorn (production server)

**Frontend:**
- Vanilla HTML/CSS/JavaScript
- No frameworks (simple and fast)
- Responsive design

**AWS Services:**
- EC2 Spot Instances (compute)
- S3 (script storage)
- IAM (permissions)

**Email:**
- Office 365 SMTP
- Existing credentials (signals@plutusadvisors.ai)

## Quick Start

```bash
# 1. Configure environment
cd webapp/backend
cp .env.example .env
# Edit .env with your AWS configuration

# 2. Check configuration
cd ../deploy
python3 check_config.py

# 3. Run setup
./setup.sh

# 4. Update AWS config in backend/aws_runner.py
# Lines 116-119 (key pair, security group, IAM role)

# 5. Start backend
cd ..
./start_backend.sh

# 6. Open frontend
# Open frontend/index.html in browser
```

## Configuration Required

Before running, you need to set these in `backend/.env`:

```bash
# AWS Configuration
EC2_KEY_PAIR=your-key-pair-name
EC2_SECURITY_GROUP=sg-xxxxxxxxxxxxx
EC2_IAM_ROLE=TradingModelsEC2Role
S3_BUCKET=trading-models-automation-1761354723

# Email (already set)
SENDER_EMAIL=signals@plutusadvisors.ai
SENDER_PASSWORD=Plutus!23@advisors
```

You also need to update `backend/aws_runner.py`:
- Line 116: KeyName
- Line 117: SecurityGroupIds
- Line 119: IamInstanceProfile Name

## AWS Resources Needed

1. **IAM Role** (`TradingModelsEC2Role`)
   - S3 read/write permissions
   - EC2 terminate permission
   - Instance profile attached

2. **Security Group**
   - Outbound: Allow all (for downloads and email)
   - Inbound: None needed

3. **EC2 Key Pair**
   - For SSH access (optional, for debugging)

4. **S3 Bucket** (`trading-models-automation-1761354723`)
   - Stores trading scripts
   - Already exists in your AWS account

See `QUICKSTART.md` for creating these resources.

## Cost Estimate

- **Per script run**: $0.01 - $0.05 (30-90 minutes of spot instance)
- **S3 storage**: ~$0.023/GB/month (minimal, scripts are small)
- **Monthly (100 runs)**: ~$3-7

Much cheaper than running scheduled instances 24/7!

## Deployment Options

### Option 1: Local Testing
```bash
./start_backend.sh
# Open frontend/index.html in browser
```

### Option 2: Simple VPS
```bash
# On server (EC2, DigitalOcean, etc.)
./start_production.sh
# Set up nginx reverse proxy
```

### Option 3: Docker
```bash
docker build -t trading-webapp .
docker run -p 5000:5000 --env-file backend/.env trading-webapp
```

### Option 4: AWS Elastic Beanstalk
```bash
cd backend
eb init && eb create
```

See README.md for detailed deployment instructions.

## Security Features

✅ Email validation (frontend + backend)
✅ Environment variables for secrets
✅ IAM role-based permissions
✅ Auto-terminating instances
✅ Security group blocks inbound traffic
✅ Input sanitization
✅ CORS enabled for frontend
✅ .gitignore prevents committing secrets

## API Endpoints

```bash
# Health check
GET /api/health

# List available scripts
GET /api/scripts

# Run a script
POST /api/run
Body: {"script_name": "india_daily", "user_email": "user@example.com"}

# Check instance status
GET /api/status/<instance_id>
```

## Testing

```bash
# Test backend API
curl http://localhost:5000/api/health
curl http://localhost:5000/api/scripts

# Test script run
curl -X POST http://localhost:5000/api/run \
  -H "Content-Type: application/json" \
  -d '{"script_name":"india_daily", "user_email":"test@example.com"}'
```

## Monitoring

```bash
# View running instances
aws ec2 describe-instances \
  --filters "Name=tag:Source,Values=webapp" \
  --query 'Reservations[*].Instances[*].[InstanceId,State.Name,LaunchTime]' \
  --output table

# View spot requests
aws ec2 describe-spot-instance-requests \
  --filters "Name=tag:Source,Values=webapp"

# Check S3 uploads
aws s3 ls s3://trading-models-automation-1761354723/scripts/
```

## Troubleshooting

Common issues and solutions:

**"No module named 'boto3'"**
→ Run: `pip3 install -r backend/requirements.txt`

**"UnauthorizedOperation"**
→ Run: `aws configure` and set credentials

**"InvalidKeyPair.NotFound"**
→ Update `EC2_KEY_PAIR` in `.env`

**"InvalidGroup.NotFound"**
→ Update `EC2_SECURITY_GROUP` in `.env`

**Frontend can't connect**
→ Ensure backend is running on port 5000
→ Check browser console for CORS errors

See README.md for more troubleshooting.

## What's NOT Included

This is a simple, functional app. It doesn't have:
- User authentication (anyone can run scripts)
- Usage tracking/quotas
- Database (stateless)
- Rate limiting
- Advanced error handling
- Monitoring dashboard
- Email queue
- Webhook notifications

These can be added later if needed.

## Next Steps

1. ✅ Complete setup (run `./deploy/setup.sh`)
2. ✅ Test locally (run a script, check email)
3. ⬜ Deploy to server (if needed)
4. ⬜ Set up domain name (optional)
5. ⬜ Add authentication (if needed)
6. ⬜ Set up monitoring (CloudWatch, etc.)

## Support

- **Documentation**: See README.md and QUICKSTART.md
- **Configuration**: Run `python3 deploy/check_config.py`
- **AWS Issues**: Check CloudWatch logs for instance execution
- **Email Issues**: Verify SMTP credentials in `.env`

## Summary

You now have a fully functional web app that:
- Lets users run trading scripts on-demand
- Sends results to their email
- Uses AWS spot instances (cost-effective)
- Auto-terminates instances
- Works with your existing scripts (no modifications needed)
- Is ready to deploy and use

**Everything is in the `webapp/` folder - ready to push and deploy!**

---

Created for Plutus Advisors | Trading Automation Platform
