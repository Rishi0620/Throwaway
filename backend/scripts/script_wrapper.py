"""
Generic wrapper to run trading scripts and send output to custom email
Usage: python script_wrapper.py <script_name> <user_email>
"""

import sys
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date
import time
import shutil

# Script configuration
SCRIPT_CONFIGS = {
    'india_daily': {
        'script_path': '/home/ubuntu/india_daily.py',
        'csv_output': 'India_equity_Daily.csv',
        'subject': f'India Equity - Daily Outcomes - Tracking Portfolio - {date.today().strftime("%Y-%m-%d")}',
        'body': 'Please find attached your requested report for India Daily Equity signals.'
    },
    'us_rolling_weekly': {
        'script_path': '/home/ubuntu/us_rolling_weekly.py',
        'csv_output': 'US_Rolling_Weekly.csv',
        'subject': f'US Rolling Weekly - Trade Signals - {date.today().strftime("%Y-%m-%d")}',
        'body': 'Please find attached your requested report for US Rolling Weekly signals.'
    },
    'india_weekly_fno': {
        'script_path': '/home/ubuntu/india_weekly_fno.py',
        'csv_output': 'India_Weekly_FNO.csv',
        'subject': f'India Weekly F&O - Trade Signals - {date.today().strftime("%Y-%m-%d")}',
        'body': 'Please find attached your requested report for India Weekly F&O signals.'
    },
    'india_weekly_nse500': {
        'script_path': '/home/ubuntu/india_weekly_nse500.py',
        'csv_output': 'India_Weekly_NSE500.csv',
        'subject': f'India Weekly NSE500 - Trade Signals - {date.today().strftime("%Y-%m-%d")}',
        'body': 'Please find attached your requested report for India Weekly NSE500 signals.'
    },
    'us_pairs_15': {
        'script_path': '/home/ubuntu/us_pairs_15.py',
        'csv_output': 'US_pairs_trades_live.csv',
        'subject': f'US Pairs 15-Min - Trade Signals - {date.today().strftime("%Y-%m-%d")}',
        'body': 'Please find attached your requested report for US Pairs 15-minute signals.'
    }
}

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path):
    """Send email with CSV attachment"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach CSV file
    if os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)
    else:
        print(f"Warning: CSV file not found at {attachment_path}")
        msg.attach(MIMEText("Note: Script completed but no CSV output was generated.", 'plain'))

    try:
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {recipient_email}!")
        return True
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False

def run_script(script_name, user_email):
    """Run the trading script and send output to user email"""

    if script_name not in SCRIPT_CONFIGS:
        print(f"Error: Unknown script '{script_name}'")
        print(f"Available scripts: {', '.join(SCRIPT_CONFIGS.keys())}")
        sys.exit(1)

    config = SCRIPT_CONFIGS[script_name]

    # Get email credentials from environment
    sender_email = os.getenv("SENDER_EMAIL", "signals@plutusadvisors.ai")
    sender_password = os.getenv("SENDER_PASSWORD", "Plutus!23@advisors")

    print(f"Starting execution of {script_name}...")
    print(f"Output will be sent to: {user_email}")

    # Run the original script
    try:
        print(f"Executing script: {config['script_path']}")
        result = subprocess.run(
            ['python3', config['script_path']],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3600  # 1 hour timeout
        )

        print("Script execution output:")
        print(result.stdout)

        if result.stderr:
            print("Script errors/warnings:")
            print(result.stderr)

        if result.returncode != 0:
            print(f"Warning: Script exited with code {result.returncode}")

    except subprocess.TimeoutExpired:
        print("Error: Script execution timed out after 1 hour")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing script: {e}")
        sys.exit(1)

    # Send email with the CSV output
    print(f"\nSending results to {user_email}...")

    success = send_email(
        sender_email=sender_email,
        sender_password=sender_password,
        recipient_email=user_email,
        subject=config['subject'],
        body=config['body'],
        attachment_path=config['csv_output']
    )

    if success:
        print("✓ Script completed successfully!")
    else:
        print("✗ Script completed but email sending failed")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_wrapper.py <script_name> <user_email>")
        print(f"Available scripts: {', '.join(SCRIPT_CONFIGS.keys())}")
        sys.exit(1)

    script_name = sys.argv[1]
    user_email = sys.argv[2]

    run_script(script_name, user_email)
