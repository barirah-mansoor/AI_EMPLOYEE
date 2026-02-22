#!/usr/bin/env python3
"""
Gmail Authentication Handler for Silver Tier AI Employee
Optimized for VS Code development workflow
"""
import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys


class GmailAuthenticator:
    def __init__(self):
        self.vault_path = Path.home() / "AI_Employee_Vault"
        self.creds_path = self.vault_path / "Silver_Tier/Credentials"
        self.scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.modify'
        ]

        # Ensure credentials directory exists
        self.creds_path.mkdir(parents=True, exist_ok=True)

    def authenticate(self):
        """Authenticate and return Gmail service object"""
        creds = None
        token_file = self.creds_path / 'gmail_token.json'
        credentials_file = self.creds_path / 'gmail_credentials.json'

        print(f"🔐 Looking for credentials in: {self.creds_path}")

        # Load existing token
        if token_file.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(token_file), self.scopes)
                print("✅ Found existing token")
            except Exception as e:
                print(f"⚠️  Token file corrupted: {e}")
                token_file.unlink()  # Delete corrupted token

        # Refresh or get new token
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    print("🔄 Refreshing expired token...")
                    creds.refresh(Request())
                    print("✅ Token refreshed successfully")
                except Exception as e:
                    print(f"❌ Token refresh failed: {e}")
                    creds = None

            if not creds:
                if not credentials_file.exists():
                    print("❌ Gmail credentials not found!")
                    print(f"📁 Expected location: {credentials_file}")
                    print("📖 Setup guide: Silver_Tier/Credentials/GMAIL_SETUP_README.md")
                    print()
                    print("Quick setup:")
                    print("1. Go to https://console.developers.google.com/")
                    print("2. Enable Gmail API")
                    print("3. Create OAuth 2.0 credentials")
                    print("4. Download JSON file")
                    print(f"5. Save as: {credentials_file}")
                    return None

                try:
                    print("🌐 Starting OAuth flow...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(credentials_file), self.scopes)
                    creds = flow.run_local_server(port=0)
                    print("✅ OAuth flow completed")
                except Exception as e:
                    print(f"❌ OAuth flow failed: {e}")
                    return None

            # Save the token
            try:
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                print(f"💾 Token saved to: {token_file}")
            except Exception as e:
                print(f"⚠️  Could not save token: {e}")

        # Build Gmail service
        try:
            service = build('gmail', 'v1', credentials=creds)
            print("✅ Gmail service connected")
            return service
        except Exception as e:
            print(f"❌ Failed to build Gmail service: {e}")
            return None

    def test_connection(self):
        """Test Gmail connection and display account info"""
        print("🧪 Testing Gmail connection...")

        try:
            service = self.authenticate()
            if not service:
                return False

            # Get profile info
            profile = service.users().getProfile(userId='me').execute()
            email = profile['emailAddress']
            total_messages = profile['messagesTotal']

            print(f"✅ Connected to: {email}")
            print(f"📊 Total messages in account: {total_messages:,}")

            # Test reading recent messages
            results = service.users().messages().list(userId='me', maxResults=5).execute()
            messages = results.get('messages', [])
            print(f"📧 Can access {len(messages)} recent messages")

            # Test labels (folders)
            labels_result = service.users().labels().list(userId='me').execute()
            labels = labels_result.get('labels', [])
            print(f"📁 Available labels: {len(labels)}")

            return True

        except HttpError as error:
            print(f"❌ Gmail API error: {error}")
            if error.resp.status == 403:
                print("🔒 Permission denied - check OAuth scopes")
            elif error.resp.status == 401:
                print("🔑 Authentication failed - token may be invalid")
            return False
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False


if __name__ == "__main__":
    print("🤖 AI Employee Gmail Authenticator")
    print("=" * 50)
    auth = GmailAuthenticator()
    success = auth.test_connection()

    print("=" * 50)
    sys.exit(0 if success else 1)
