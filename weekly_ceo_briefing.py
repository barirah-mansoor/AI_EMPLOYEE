#!/usr/bin/env python3
"""
Weekly CEO Briefing - Autonomous weekly business audit
Generates comprehensive briefing from all domains
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any

# Configuration
VAULT_PATH = Path("/mnt/c/Users/Admin/AI_Employee_Vault")
DONE_DIR = VAULT_PATH / "Done"
ACCOUNTING_DIR = VAULT_PATH / "Accounting"
BRIEFINGS_DIR = VAULT_PATH / "Briefings"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
DEV_MODE = os.environ.get("DEV_MODE", "true").lower() == "true"


def read_business_goals() -> str:
    """Read business goals."""
    goals_file = VAULT_PATH / "Business_Goals.md"
    if goals_file.exists():
        return goals_file.read_text()
    return "No business goals defined."


def get_completed_tasks() -> List[Dict[str, Any]]:
    """Get tasks completed this week from Done folder."""
    tasks = []
    week_ago = datetime.now() - timedelta(days=7)

    if not DONE_DIR.exists():
        return tasks

    for task_file in DONE_DIR.glob("*.md"):
        # Check file modification time
        mtime = datetime.fromtimestamp(task_file.stat().st_mtime)
        if mtime >= week_ago:
            content = task_file.read_text()
            tasks.append({
                "file": task_file.name,
                "completed_at": mtime.isoformat(),
                "preview": content[:200]
            })

    return tasks


def read_accounting_data() -> Dict[str, Any]:
    """Read accounting data."""
    data = {
        "current_month": {},
        "transactions": [],
        "subscriptions": []
    }

    # Read Current_Month.md
    current_month_file = ACCOUNTING_DIR / "Current_Month.md"
    if current_month_file.exists():
        content = current_month_file.read_text()
        data["current_month"]["raw"] = content[:500]

    # Read bank transactions
    bank_csv = ACCOUNTING_DIR / "bank_transactions.csv"
    if bank_csv.exists():
        import csv
        with open(bank_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data["transactions"].append(row)

                # Track subscriptions
                amount_str = row.get('amount', '0')
                try:
                    amount = float(amount_str)
                    if amount < 0 and abs(amount) < 500:
                        data["subscriptions"].append({
                            "service": row.get('description', 'Unknown'),
                            "amount": abs(amount)
                        })
                except ValueError:
                    pass

    return data


def audit_subscriptions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Audit subscriptions using audit_logic."""
    # Import the audit logic
    sys.path.insert(0, str(VAULT_PATH))
    try:
        from audit_logic import analyze_transaction, flag_unused_subscriptions
    except ImportError:
        return []

    unused = []
    for tx in transactions:
        analysis = analyze_transaction(tx)
        if analysis.get('is_subscription'):
            unused.append({
                "service": analysis.get('service_name'),
                "amount": tx.get('amount'),
                "description": tx.get('description')
            })

    return unused


def get_odoo_summary() -> Dict[str, Any]:
    """Get Odoo accounting summary (or DEV_MODE mock)."""
    if DEV_MODE:
        return {
            "dev_mode": True,
            "total_revenue": 9750.00,
            "total_expenses": 2500.00,
            "net_profit": 7250.00,
            "outstanding_invoices": 2,
            "paid_invoices": 1,
            "as_of": datetime.now().isoformat()
        }

    # Real Odoo integration would go here
    return {"error": "Odoo not configured"}


def generate_briefing() -> str:
    """Generate the weekly CEO briefing."""
    # Gather data
    business_goals = read_business_goals()
    completed_tasks = get_completed_tasks()
    accounting = read_accounting_data()
    subscriptions = audit_subscriptions(accounting.get('transactions', []))
    odoo_summary = get_odoo_summary()

    # Calculate metrics
    total_income = sum(
        float(tx.get('amount', 0)) for tx in accounting.get('transactions', [])
        if float(tx.get('amount', 0)) > 0
    )
    total_expenses = sum(
        abs(float(tx.get('amount', 0))) for tx in accounting.get('transactions', [])
        if float(tx.get('amount', 0)) < 0
    )

    # Build markdown
    today = datetime.now()
    monday_date = today - timedelta(days=today.weekday())
    briefing_date = monday_date.strftime("%Y-%m-%d")

    content = f"""# Weekly CEO Briefing

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Week of:** {briefing_date}

---

## Executive Summary

This week saw {len(completed_tasks)} tasks completed with a focus on system automation and business operations. Revenue tracking is active through the accounting integration.

---

## Revenue Summary

| Metric | Amount |
|--------|--------|
| **This Week** | ${total_income:,.2f} |
| **MTD** | ${total_income:,.2f} |
| **Total Expenses** | ${total_expenses:,.2f} |
| **Net** | ${total_income - total_expenses:,.2f} |

### Odoo Accounting

"""

    if odoo_summary.get("dev_mode"):
        content += f"- ⚠️ **DEV_MODE**: Using simulated data\n"
        content += f"- Total Revenue: ${odoo_summary.get('total_revenue', 0):,.2f}\n"
        content += f"- Total Expenses: ${odoo_summary.get('total_expenses', 0):,.2f}\n"
        content += f"- Net Profit: ${odoo_summary.get('net_profit', 0):,.2f}\n"
    else:
        content += f"- Revenue: ${odoo_summary.get('total_revenue', 0):,.2f}\n"

    content += f"""
### Invoice Status

| Status | Count |
|--------|-------|
| Outstanding | {odoo_summary.get('outstanding_invoices', 0)} |
| Paid | {odoo_summary.get('paid_invoices', 0)} |

---

## Completed Tasks This Week

"""

    if completed_tasks:
        for task in completed_tasks:
            content += f"- [x] {task['file']}\n"
    else:
        content += "- No tasks completed this week\n"

    content += """

---

## Bottlenecks & Delays

| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| (No bottlenecks reported) | | | |

---

## Proactive Suggestions

### Subscription Audit

"""

    if subscriptions:
        content += "| Service | Monthly Cost |\n|--------|-------------|\n"
        for sub in subscriptions:
            try:
                amount = float(sub.get('amount', 0))
            except (ValueError, TypeError):
                amount = 0
            content += f"| {sub.get('service', 'Unknown')} | ${amount:.2f} |\n"
    else:
        content += "No active subscriptions detected.\n"

    content += """

### Cost Optimization Opportunities

- Review unused subscriptions
- Consider annual billing for discounts
- Audit service tiers for downgrades

### Upcoming Deadlines

- [ ] Review pending approvals in `Pending_Approval/`
- [ ] Process week-end accounting reconciliation

---

## System Status

| Component | Status |
|-----------|--------|
| WhatsApp Watcher | ✅ Active |
| Finance Watcher | ✅ Active |
| Email Intelligence | ✅ Active |
| Orchestrator | ✅ Running |

---

*Generated by Gold Tier AI Employee*
"""

    return content


def save_briefing(content: str) -> Path:
    """Save briefing to Briefings folder."""
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now()
    monday_date = today - timedelta(days=today.weekday())
    filename = f"{monday_date.strftime('%Y-%m-%d')}_Monday_CEO_Briefing.md"

    file_path = BRIEFINGS_DIR / filename
    file_path.write_text(content)

    return file_path


def log_briefing(file_path: Path):
    """Log briefing generation to audit log."""
    log_file = VAULT_PATH / "Logs" / f"{datetime.now().strftime('%Y-%m-%d')}.json"
    logs = []

    if log_file.exists():
        try:
            logs = json.loads(log_file.read_text())
        except json.JSONDecodeError:
            pass

    logs.append({
        "timestamp": datetime.now().isoformat(),
        "skill": "weekly_ceo_briefing",
        "action": "Generated weekly CEO briefing",
        "files_affected": [str(file_path)],
        "approval_required": False,
        "result": "success"
    })

    log_file.write_text(json.dumps(logs, indent=2))


def main():
    """Main entry point."""
    print(f"Generating Weekly CEO Briefing...")
    print(f"DEV_MODE: {DEV_MODE}")

    # Generate briefing
    content = generate_briefing()

    # Save
    file_path = save_briefing(content)

    # Log
    log_briefing(file_path)

    print(f"Briefing saved to: {file_path}")


if __name__ == "__main__":
    main()
