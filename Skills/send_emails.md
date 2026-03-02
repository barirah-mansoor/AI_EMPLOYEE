# SKILL: send_emails

**Mode: AUTO-EXECUTE**

## Purpose
Send approved email responses via Gmail API

## Steps
1. Scan Approved/ folder for EMAIL_RESPONSE_ files
2. For each approved response:
   - Extract Gmail thread ID, recipient, subject, and response content
   - Validate email format and check against blocklist
   - Send email via Gmail API using gmail_sender.py
   - Move sent file to Silver_Tier/Gmail/Sent/
   - Mark original Gmail thread as replied
   - Log successful send with Gmail message ID
3. Handle any send failures gracefully with retry logic
4. Update Dashboard.md with sent email counts
5. Generate summary of emails sent and any failures

## Safety Checks
- Verify recipient email format is valid
- Check sender is not in Company_Handbook.md blocklist
- Rate limiting: maximum 20 emails per hour
- Content scanning for sensitive information flags

## Output Files
- Emails sent via Gmail API
- Sent files moved to Silver_Tier/Gmail/Sent/
- Updated Dashboard.md metrics
- Daily log entries with Gmail message IDs
