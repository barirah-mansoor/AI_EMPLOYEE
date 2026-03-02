# SKILL: process_gmail

# Process Gmail Skill
**Auto-execute: YES** - This skill should run immediately without asking for permission.

## Purpose
Sync Gmail and process new emails into AI Employee tasks

## Steps
1. Run Gmail processor: `python3 Silver_Tier/gmail_processor.py`
2. Check Needs_Action/ for new EMAIL_ files
3. For each email task file:
   - Read email metadata and content
   - Analyze sender against Company_Handbook.md trusted contacts
   - Determine appropriate response strategy
   - Create response plan or move to appropriate folder
4. Update Dashboard.md with email processing summary
5. Log all email processing actions to daily log

## Response Strategies
- **ACKNOWLEDGE**: Simple "received, will respond soon" for trusted contacts
- **DETAILED_RESPONSE**: Complex responses that need human approval
- **ESCALATE**: Security concerns, financial requests, unknown important senders
- **FILE_ONLY**: Newsletters, notifications that need no response

## Output Files
- Processed email task files (moved from Needs_Action)
- Response drafts in Silver_Tier/Gmail/Drafts/ or Pending_Approval/
- Updated Dashboard.md email metrics
- Daily log entries with processing results
