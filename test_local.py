#!/usr/bin/env python3
"""
Local testing script for Trading Scripts Web App
Tests the backend API without launching AWS resources
"""

import requests
import json
import sys

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

BASE_URL = "http://localhost:5000/api"

def print_test(name):
    print(f"\n{BLUE}Testing: {name}{RESET}")

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def test_health():
    """Test health endpoint"""
    print_test("Health Check")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)

        if response.status_code == 200:
            data = response.json()
            print_success(f"Backend is healthy: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend")
        print_warning("Make sure backend is running: ./start_backend.sh")
        return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_get_scripts():
    """Test getting list of scripts"""
    print_test("Get Available Scripts")

    try:
        response = requests.get(f"{BASE_URL}/scripts", timeout=5)

        if response.status_code == 200:
            data = response.json()
            scripts = data.get('scripts', {})

            print_success(f"Found {len(scripts)} scripts:")
            for name, info in scripts.items():
                print(f"  - {info['name']} ({name})")

            return True
        else:
            print_error(f"Failed to get scripts: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Get scripts error: {e}")
        return False

def test_run_script_validation():
    """Test input validation without actually running"""
    print_test("Input Validation")

    tests = [
        {
            'name': 'Missing email',
            'data': {'script_name': 'india_daily'},
            'should_fail': True
        },
        {
            'name': 'Missing script_name',
            'data': {'user_email': 'test@example.com'},
            'should_fail': True
        },
        {
            'name': 'Invalid email format',
            'data': {'script_name': 'india_daily', 'user_email': 'invalid-email'},
            'should_fail': True
        },
        {
            'name': 'Invalid script name',
            'data': {'script_name': 'nonexistent', 'user_email': 'test@example.com'},
            'should_fail': True
        },
    ]

    all_passed = True

    for test in tests:
        try:
            response = requests.post(
                f"{BASE_URL}/run",
                json=test['data'],
                timeout=5
            )

            if test['should_fail'] and response.status_code != 200:
                print_success(f"{test['name']}: Correctly rejected")
            elif not test['should_fail'] and response.status_code == 200:
                print_success(f"{test['name']}: Correctly accepted")
            else:
                print_error(f"{test['name']}: Unexpected response {response.status_code}")
                all_passed = False

        except Exception as e:
            print_error(f"{test['name']}: Error - {e}")
            all_passed = False

    return all_passed

def test_cors():
    """Test CORS headers"""
    print_test("CORS Configuration")

    try:
        response = requests.options(
            f"{BASE_URL}/run",
            headers={'Origin': 'http://localhost:8000'}
        )

        cors_header = response.headers.get('Access-Control-Allow-Origin')

        if cors_header:
            print_success(f"CORS enabled: {cors_header}")
            return True
        else:
            print_warning("CORS headers not found (may cause frontend issues)")
            return False

    except Exception as e:
        print_error(f"CORS test error: {e}")
        return False

def main():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Trading Scripts Web App - Local Testing{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

    tests = [
        ("Health Check", test_health),
        ("Get Scripts", test_get_scripts),
        ("Input Validation", test_run_script_validation),
        ("CORS", test_cors),
    ]

    results = {}

    for name, test_func in tests:
        results[name] = test_func()

    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        if result:
            print_success(test_name)
        else:
            print_error(test_name)

    print(f"\n{passed}/{total} tests passed\n")

    if passed == total:
        print_success("All tests passed! Backend is working correctly.")
        print_warning("\nNote: This doesn't test AWS integration (spot instances)")
        print_warning("To test end-to-end, use the frontend and run a real script")
        print(f"\nNext steps:")
        print(f"  1. Open frontend/index.html in your browser")
        print(f"  2. Enter your email")
        print(f"  3. Click a script button to test full flow")
        return 0
    else:
        print_error("Some tests failed. Check the backend logs for errors.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
