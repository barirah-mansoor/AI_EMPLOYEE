#!/usr/bin/env python3
"""
Gmail Processing Engine for Silver Tier AI Employee
Processes emails and integrates with VS Code workflow
"""

import json
import base64
import re
from datetime import datetime
from pathlib import Path
from gmail_authenticator import GmailAuthenticator


class GmailProcessor:
    def __init__(self):
        self.vault_path = Path.home() / "AI_Employee_Vault"
        self.gmail_path = self.vault_path / "Silver_Tier/Gmail"
        self.auth = GmailAuthenticator()
        self.service = None
        self.processed_ids = set()

        # Ensure directories exist
        for folder in ['Processed', 'Drafts', 'Sent', 'Failed']:
            (self.gmail_path / folder).mkdir(parents=True, exist_ok=True)

        self.load_processed_history()

    def load_processed_history(self):
        """Load list of already processed email IDs"""
        history_file = self.gmail_path / "processed_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                    self.processed_ids = set(data)
                print(f"📚 Loaded {len(self.processed_ids)} processed email IDs")
            except Exception as e:
                print(f"⚠️  Could not load history: {e}")
                self.processed_ids = set()

    def save_processed_history(self):
        """Save processed email IDs to prevent reprocessing"""
        history_file = self.gmail_path / "processed_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump(list(self.processed_ids), f)
        except Exception as e:
            print(f"⚠️  Could not save history: {e}")

    def connect(self):
        """Connect to Gmail service"""
        print("🔗 Connecting to Gmail...")
        self.service = self.auth.authenticate()
        if self.service:
            print("✅ Gmail connection established")
        return self.service is not None

    def get_unread_emails(self, max_results=100):
        """Get unread emails from inbox"""
        if not self.service:
            return []

        try:
            print(f"📧 Fetching up to {max_results} unread emails...")

            results = self.service.users().messages().list(
                userId='me',
                q='is:unread in:inbox -in:spam -in:trash',
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            unprocessed = [msg['id'] for msg in messages if msg['id'] not in self.processed_ids]

            print(f"📮 Found {len(messages)} unread, {len(unprocessed)} new")
            return unprocessed

        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []

    def get_email_content(self, message_id):
        """Extract email content and metadata"""
        try:
            message = self.service.users().messages().get(
                userId='me', id=message_id, format='full'
            ).execute()

            headers = message['payload'].get('headers', [])

            email_data = {
                'id': message_id,
                'thread_id': message['threadId'],
                'subject': self.get_header(headers, 'Subject'),
                'sender': self.get_header(headers, 'From'),
                'date': self.get_header(headers, 'Date'),
                'body': self.extract_body(message['payload']),
                'labels': message.get('labelIds', []),
                'snippet': message.get('snippet', ''),
                'received_at': datetime.now().isoformat()
            }

            email_data['importance'] = self.determine_importance(email_data)
            email_data['category'] = self.categorize_email(email_data)

            return email_data

        except Exception as e:
            print(f"❌ Error getting email {message_id}: {e}")
            return None

    def get_header(self, headers, name):
        """Extract header value by name"""
        for header in headers:
            if header['name'].lower() == name.lower():
                return header['value']
        return ''

    def extract_body(self, payload):
        """Extract email body text"""
        body = ""

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part.get('body', {}).get('data')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        elif payload['mimeType'] == 'text/plain':
            data = payload.get('body', {}).get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

        return body.strip()[:2000]  # Limit body length

    def determine_importance(self, email_data):
        """Determine email importance"""
        subject = email_data['subject'].lower()
        body = email_data['body'].lower()

        # RED: Urgent
        if any(word in subject + body for word in ['urgent', 'asap', 'emergency', 'critical']):
            return 'RED'

        # YELLOW: High priority
        if any(word in subject + body for word in ['deadline', 'meeting', 'client', 'payment']):
            return 'YELLOW'

        return 'GREEN'

    def categorize_email(self, email_data):
        """Categorize email type"""
        subject = email_data['subject'].lower()
        sender = email_data['sender'].lower()

        if 'noreply' in sender or 'no-reply' in sender:
            return 'NOTIFICATION'
        elif any(word in subject for word in ['meeting', 'calendar', 'invite']):
            return 'MEETING'
        elif any(word in subject for word in ['newsletter', 'unsubscribe']):
            return 'NEWSLETTER'
        else:
            return 'BUSINESS'

    def process_email(self, email_data):
        """Process single email through AI Employee system"""
        try:
            print(f"📧 Processing: {email_data['subject'][:50]}...")

            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_subject = re.sub(r'[^\w\s-]', '', email_data['subject'])[:20]
            safe_subject = re.sub(r'\s+', '_', safe_subject.strip())

            filename = f"EMAIL_{email_data['id'][:8]}_{safe_subject}_{timestamp}.md"
            filepath = self.vault_path / "Needs_Action" / filename

            # Create structured email task
            content = f"""---
type: email
source: gmail
priority: {email_data['importance']}
category: {email_data['category']}
gmail_id: {email_data['id']}
thread_id: {email_data['thread_id']}
processed_at: {email_data['received_at']}
---

# Email Task: {email_data['subject']}

## 📧 Email Details

**From:** {email_data['sender']}
**Subject:** {email_data['subject']}
**Date:** {email_data['date']}
**Priority:** {email_data['importance']}
**Category:** {email_data['category']}

## 📝 Content

{email_data['body']}

## 🤖 AI Processing Instructions

**Task:** Analyze this email and determine:

1. **Intent:** What does the sender want?
2. **Response needed:** Should we respond? What type?
3. **Priority confirmation:** Is the auto-assigned priority correct?
4. **Next actions:** What specific steps should be taken?

**Response Options:**
- `ACKNOWLEDGE`: Simple confirmation email
- `DETAILED_RESPONSE`: Complex response requiring approval
- `ESCALATE`: Forward to human for review
- `FILE_ONLY`: No response needed

**Priority Level:** {email_data['importance']}
"""

            # Write task file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            # Save raw data
            raw_path = self.gmail_path / "Processed" / f"{email_data['id']}.json"
            with open(raw_path, 'w') as f:
                json.dump(email_data, f, indent=2)

            # Mark as processed
            self.processed_ids.add(email_data['id'])

            print(f"✅ Created task: {filename}")
            return True

        except Exception as e:
            print(f"❌ Error processing email: {e}")
            return False

    def run_gmail_sync(self):
        """Main Gmail sync function"""
        print("🔄 Starting Gmail sync...")

        if not self.connect():
            print("❌ Could not connect to Gmail")
            return False

        unread_ids = self.get_unread_emails()
        processed_count = 0

        for email_id in unread_ids:
            email_data = self.get_email_content(email_id)
            if email_data and self.process_email(email_data):
                processed_count += 1

        self.save_processed_history()
        print(f"✅ Gmail sync complete. Processed {processed_count} emails.")
        return True


if __name__ == "__main__":
    processor = GmailProcessor()
    processor.run_gmail_sync()
