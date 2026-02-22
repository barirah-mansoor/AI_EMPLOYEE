# SKILL: system_monitor

**Mode: AUTO-EXECUTE**

## Purpose
Monitor Silver Tier system health and performance

## Steps
1. **API Health Checks**:
   - Test Gmail API connection and token validity
   - Check Google Calendar API if configured
   - Verify all credential files exist and are valid
2. **System Resource Monitoring**:
   - Check disk space usage in vault directory
   - Monitor Python process memory usage
   - Verify file watcher processes are running
3. **Performance Analysis**:
   - Measure email processing times
   - Check skill execution success rates
   - Analyze error patterns in logs
4. **Security Audit**:
   - Scan for any exposed credentials in logs
   - Verify file permissions on sensitive directories
   - Check for unusual file access patterns
5. **Automation Health**:
   - Verify scheduler is running if enabled
   - Check scheduled task completion rates
   - Identify any failed automation jobs
6. **Generate Health Report**:
   - Create detailed status report in Silver_Tier/Analytics/
   - Update Dashboard.md system status section
   - Alert on any critical issues found

## Alert Conditions
- API tokens expiring within 7 days
- Disk space usage above 80%
- Error rates above 10% for any skill
- Failed scheduled tasks in past 24 hours
- Any security violations detected

## Output Files
- System health report in Silver_Tier/Analytics/Reports/
- Updated Dashboard.md system status
- Alert notifications for critical issues
- Daily log entry with health metrics
