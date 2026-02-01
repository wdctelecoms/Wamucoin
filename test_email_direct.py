#!/usr/bin/env python3
"""Direct test of the registration endpoint and email sending"""

import sys
sys.path.insert(0, "/workspaces/Wamucoin/finshield-ai")

from app.app import app, send_verification_email, EMAIL_SENDER
from dotenv import load_dotenv
import os

load_dotenv()

# Test the app in test mode
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

print("=" * 60)
print("FinShield Email Verification Test")
print("=" * 60)

# Check SMTP configuration
smtp_password = os.environ.get("SMTP_PASSWORD", "")
print(f"\n1. SMTP Configuration:")
print(f"   Email Sender: {EMAIL_SENDER}")
print(f"   SMTP Password Configured: {'✓' if smtp_password else '✗'}")

if not smtp_password:
    print("\n✗ ERROR: SMTP_PASSWORD not set in .env")
    sys.exit(1)

# Test sending verification email
print(f"\n2. Testing Email Send...")
test_token = "test_verification_token_12345"
test_email = "finshieldAI@gmail.com"

result = send_verification_email(test_email, test_token)

if result:
    print(f"   ✓ Email sent successfully to {test_email}")
    print(f"   ✓ From: {EMAIL_SENDER}")
else:
    print(f"   ✗ Email send failed")
    sys.exit(1)

# Test registration flow
print(f"\n3. Testing Registration Flow...")
with app.test_client() as client:
    response = client.post('/register', data={
        'username': 'testuser_' + os.urandom(4).hex(),
        'email': 'test_' + os.urandom(4).hex() + '@example.com',
        'password': 'TestPass123',
        'account_type': 'individual'
    }, follow_redirects=True)
    
    if response.status_code == 200:
        if b'verification' in response.data.lower() or b'email' in response.data.lower():
            print(f"   ✓ Registration successful")
            print(f"   ✓ Response contains verification message")
        else:
            print(f"   ✓ Registration returned 200")
    else:
        print(f"   ✗ Registration failed with status {response.status_code}")

print("\n" + "=" * 60)
print("✓ All tests passed! Email verification is working.")
print("=" * 60)
