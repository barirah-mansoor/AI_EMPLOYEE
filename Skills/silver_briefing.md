# SKILL: silver_briefing

**Mode: AUTO-EXECUTE**

## Purpose
Generate enhanced daily briefing with Gmail and system metrics

## Steps
1. Execute all steps from standard daily_briefing skill
2. Add Silver Tier sections to briefing:
   - **Email Summary**: Count of emails processed, pending responses, high priority items
   - **System Health**: API connection status, credential expiry warnings, error counts
   - **Automation Status**: Scheduled task results, any failed automations
   - **Performance Metrics**: Processing times, success rates, cost analysis
3. Read Silver_Tier/Gmail/processed_history.json for email statistics
4. Check Silver_Tier/Automation/Logs/ for scheduler status
5. Generate enhanced briefing file with Silver Tier data
6. Update Dashboard.md with comprehensive status
7. Log briefing generation with enhanced metrics

## Enhanced Briefing Sections
- **📧 Email Activity**: Today's email processing summary
- **⚡ System Performance**: Response times and efficiency metrics
- **🔧 Maintenance**: Any system issues or upcoming maintenance needs
- **💰 Cost Analysis**: API usage and associated costs

## Output Files
- Enhanced briefing in Briefings/ folder
- Updated Dashboard.md with Silver Tier status
- Log entry with comprehensive metrics
