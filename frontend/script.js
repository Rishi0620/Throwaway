// Configuration
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.protocol === 'file:'
    ? 'http://localhost:5001/api'
    : '/api';  // Use relative URL in production

// State
let isRunning = false;

// DOM Elements
const emailInput = document.getElementById('userEmail');
const runButtons = document.querySelectorAll('.run-btn');
const loadingModal = document.getElementById('loadingModal');
const loadingText = document.getElementById('loadingText');
const statusSection = document.getElementById('statusSection');
const statusMessage = document.getElementById('statusMessage');

// Email validation
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Show loading modal
function showLoading(message) {
    loadingText.textContent = message;
    loadingModal.style.display = 'block';
}

// Hide loading modal
function hideLoading() {
    loadingModal.style.display = 'none';
}

// Show status message
function showStatus(message, isError = false) {
    statusSection.style.display = 'block';
    statusMessage.innerHTML = `<div class="${isError ? 'error-message' : 'success-message'}">${message}</div>`;

    // Scroll to status
    statusSection.scrollIntoView({ behavior: 'smooth' });
}

// Run script
async function runScript(scriptName) {
    // Validate email
    const userEmail = emailInput.value.trim();

    if (!userEmail) {
        alert('Please enter your email address');
        emailInput.focus();
        return;
    }

    if (!isValidEmail(userEmail)) {
        alert('Please enter a valid email address');
        emailInput.focus();
        return;
    }

    // Prevent multiple simultaneous runs
    if (isRunning) {
        alert('A script is already running. Please wait for it to complete.');
        return;
    }

    // Confirm action
    const scriptNames = {
        'india_daily': 'India Daily Equity',
        'us_rolling_weekly': 'US Rolling Weekly',
        'india_weekly_fno': 'India Weekly F&O',
        'india_weekly_nse500': 'India Weekly NSE500',
        'us_pairs_15': 'US Pairs 15-Min'
    };

    const confirmed = confirm(
        `Run ${scriptNames[scriptName]}?\n\n` +
        `Results will be sent to: ${userEmail}\n\n` +
        `This will launch an AWS spot instance and may take 30-90 minutes to complete.`
    );

    if (!confirmed) {
        return;
    }

    // Disable all buttons
    isRunning = true;
    runButtons.forEach(btn => btn.disabled = true);

    // Show loading
    showLoading(`Launching ${scriptNames[scriptName]}...`);

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                script_name: scriptName,
                user_email: userEmail
            })
        });

        const data = await response.json();

        hideLoading();

        if (response.ok && data.success) {
            // Success
            showStatus(
                `<strong>Script launched successfully!</strong><br><br>` +
                `<strong>Script:</strong> ${data.script}<br>` +
                `<strong>Email:</strong> ${data.email}<br>` +
                `<strong>Spot Request ID:</strong> ${data.spot_request_id}<br>` +
                `${data.instance_id ? `<strong>Instance ID:</strong> ${data.instance_id}<br>` : ''}` +
                `<strong>Estimated time:</strong> ${data.estimated_time}<br><br>` +
                `${data.note}<br><br>` +
                `<em>You can close this page. The script will continue running on AWS and email you when complete.</em>`,
                false
            );
        } else {
            // Error
            showStatus(
                `<strong>Failed to launch script</strong><br><br>` +
                `Error: ${data.error || 'Unknown error occurred'}<br><br>` +
                `Please try again or contact support if the issue persists.`,
                true
            );
        }
    } catch (error) {
        hideLoading();
        showStatus(
            `<strong>Network error</strong><br><br>` +
            `Failed to connect to the server: ${error.message}<br><br>` +
            `Please check your internet connection and try again.`,
            true
        );
    } finally {
        // Re-enable buttons after a delay
        setTimeout(() => {
            isRunning = false;
            runButtons.forEach(btn => btn.disabled = false);
        }, 3000);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Attach event listeners to all run buttons
    runButtons.forEach(button => {
        button.addEventListener('click', () => {
            const scriptName = button.getAttribute('data-script');
            runScript(scriptName);
        });
    });

    // Load saved email if exists
    const savedEmail = localStorage.getItem('userEmail');
    if (savedEmail) {
        emailInput.value = savedEmail;
    }

    // Save email on change
    emailInput.addEventListener('blur', () => {
        const email = emailInput.value.trim();
        if (email && isValidEmail(email)) {
            localStorage.setItem('userEmail', email);
        }
    });

    // Test API connection
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('API Health Check:', data);
        })
        .catch(error => {
            console.warn('API connection test failed:', error);
            showStatus(
                `<strong>Warning:</strong> Could not connect to backend API.<br>` +
                `Please ensure the backend server is running.`,
                true
            );
        });
});
