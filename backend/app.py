"""
Flask API for Trading Scripts Web App
Provides endpoints to run trading scripts on AWS spot instances
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from aws_runner import SpotInstanceRunner
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize AWS runner
runner = SpotInstanceRunner()

# Available scripts
AVAILABLE_SCRIPTS = {
    'india_daily': {
        'name': 'India Daily Equity',
        'description': 'Daily Indian equity signals (Mon-Thu)',
        'estimated_time': '45-60 min'
    },
    'us_rolling_weekly': {
        'name': 'US Rolling Weekly',
        'description': 'Weekly US equity signals (Mon-Thu)',
        'estimated_time': '60-90 min'
    },
    'india_weekly_fno': {
        'name': 'India Weekly F&O',
        'description': 'Weekly Indian F&O signals (Friday)',
        'estimated_time': '45-60 min'
    },
    'india_weekly_nse500': {
        'name': 'India Weekly NSE500',
        'description': 'Weekly NSE500 signals (Friday)',
        'estimated_time': '45-60 min'
    },
    'us_pairs_15': {
        'name': 'US Pairs 15-Min',
        'description': '15-minute pair trading signals',
        'estimated_time': '30-45 min'
    }
}

def validate_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Trading Scripts Web App',
        'version': '1.0.0'
    })

@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    """Get list of available scripts"""
    return jsonify({
        'scripts': AVAILABLE_SCRIPTS
    })

@app.route('/api/run', methods=['POST'])
def run_script():
    """
    Run a trading script on AWS spot instance
    Body: {
        "script_name": "india_daily",
        "user_email": "user@example.com"
    }
    """
    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    script_name = data.get('script_name')
    user_email = data.get('user_email')

    if not script_name:
        return jsonify({'error': 'script_name is required'}), 400

    if not user_email:
        return jsonify({'error': 'user_email is required'}), 400

    # Validate script name
    if script_name not in AVAILABLE_SCRIPTS:
        return jsonify({
            'error': f'Invalid script name. Available: {", ".join(AVAILABLE_SCRIPTS.keys())}'
        }), 400

    # Validate email format
    if not validate_email(user_email):
        return jsonify({'error': 'Invalid email format'}), 400

    # Launch spot instance
    try:
        print(f"Launching spot instance for {script_name} with email {user_email}")
        result = runner.launch_spot_instance(script_name, user_email)
        print(f"Launch result: {result}")

        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Script {script_name} started successfully',
                'script': AVAILABLE_SCRIPTS[script_name]['name'],
                'email': user_email,
                'spot_request_id': result['spot_request_id'],
                'instance_id': result.get('instance_id'),
                'estimated_time': AVAILABLE_SCRIPTS[script_name]['estimated_time'],
                'note': 'You will receive an email when the script completes'
            }), 200
        else:
            print(f"Launch failed: {result.get('error')}")
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error occurred')
            }), 500

    except Exception as e:
        print(f"Exception launching script: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Failed to launch script: {str(e)}'
        }), 500

@app.route('/api/status/<instance_id>', methods=['GET'])
def get_status(instance_id):
    """Get status of a running instance"""
    try:
        status = runner.get_instance_status(instance_id)
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"Starting Trading Scripts Web App on port {port}")
    print(f"Available scripts: {', '.join(AVAILABLE_SCRIPTS.keys())}")

    app.run(host='0.0.0.0', port=port, debug=debug)
