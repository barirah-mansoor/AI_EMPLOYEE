# SKILL: process_inbox

## Trigger
Called when new files appear in /Needs_Action

## Steps
1. List all files in /Needs_Action
2. For each file:
   - Read content and determine type and priority
   - Create /Plans/PLAN_[filename]_[date].md with:
     * Objective
     * Priority level
     * Recommended actions (checkboxes)
     * Approval needed? Yes/No
   - If approval needed: create /Pending_Approval/ file instead
3. Update Dashboard.md queue counts
4. Log all actions to /Logs/[today].json
5. Report summary: X items processed, Y need approval

## Output
- Plan files in /Plans/
- Approval files in /Pending_Approval/ if needed
- Updated Dashboard.md
- Log entry
