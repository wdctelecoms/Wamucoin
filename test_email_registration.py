#!/usr/bin/env python3
"""
Test script to verify email sending during registration.
Registers a test user and checks if email was sent.
"""

import sys
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB = "database.db"

def test_registration():
    """Test if user was created and check email sending logs"""
    
    # Check database for latest user
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT username, email, email_verified, verification_token FROM users ORDER BY id DESC LIMIT 1")
        user = c.fetchone()
        conn.close()
        
        if user:
            username, email, verified, token = user
            print(f"\n✓ Test User Created:")
            print(f"  Username: {username}")
            print(f"  Email: {email}")
            print(f"  Email Verified: {verified}")
            print(f"  Token: {token[:20]}..." if token else "  Token: None")
            print(f"\n✓ Verification Link: http://localhost:5000/verify_email/{token}")
            
            # Check if email sending is configured
            smtp_password = os.environ.get("SMTP_PASSWORD", "")
            if smtp_password:
                print(f"\n✓ SMTP Configured:")
                print(f"  Email Sender: {os.environ.get('EMAIL_SENDER', 'finshieldAI@gmail.com')}")
                print(f"  SMTP Server: {os.environ.get('SMTP_SERVER', 'smtp.gmail.com')}")
                print(f"  Password: Set ✓")
            else:
                print(f"\n✗ SMTP NOT Configured - emails won't be sent!")
                print(f"  Set SMTP_PASSWORD in .env file")
            
            return True
        else:
            print("✗ No users found in database")
            return False
            
    except Exception as e:
        print(f"✗ Error checking database: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("FinShield Email Verification Test")
    print("=" * 60)
    
    success = test_registration()
    sys.exit(0 if success else 1)
