#!/usr/bin/env python3
"""
Finance Watcher - Monitors bank transactions and manages accounting
"""

import csv
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configuration
VAULT_PATH = Path("/mnt/c/Users/Admin/AI_Employee_Vault")
ACCOUNTING_DIR = VAULT_PATH / "Accounting"
BANK_CSV = ACCOUNTING_DIR / "bank_transactions.csv"
CURRENT_MONTH = ACCOUNTING_DIR / "Current_Month.md"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
PENDING_APPROVAL = VAULT_PATH / "Pending_Approval"
DEV_MODE = os.environ.get("DEV_MODE", "false").lower() == "true"
POLL_INTERVAL = 300  # 5 minutes

# Subscription patterns to detect
SUBSCRIPTION_PATTERNS = {
    'netflix': ['netflix', 'net flix'],
    'spotify': ['spotify'],
    'adobe': ['adobe', 'creative cloud'],
    'notion': ['notion'],
    'slack': ['slack'],
    'github': ['github'],
    'aws': ['amazon web', 'aws'],
    'google': ['google cloud', 'google workspace', 'g suite'],
    'openai': ['openai'],
    'anthropic': ['anthropic'],
    'zoom': ['zoom'],
    'dropbox': ['dropbox'],
    'microsoft': ['microsoft 365', 'office 365', 'azure'],
    'apple': ['apple com', 'icloud'],
    'chatgpt': ['chatgpt', 'openai'],
}


def load_current_transactions() -> set:
    """Load currently known transaction IDs."""
    month_file = ACCOUNTING_DIR / ".processed_transactions.json"
    if month_file.exists():
        try:
            return set(json.loads(month_file.read_text()))
        except json.JSONDecodeError:
            return set()
    return set()


def save_processed_transactions(transaction_ids: set):
    """Save processed transaction IDs."""
    month_file = ACCOUNTING_DIR / ".processed_transactions.json"
    month_file.write_text(json.dumps(list(transaction_ids), indent=2))


def detect_subscription(description: str) -> Optional[Dict[str, Any]]:
    """Detect if a transaction is a subscription."""
    desc_lower = description.lower()

    for service, patterns in SUBSCRIPTION_PATTERNS.items():
        for pattern in patterns:
            if pattern in desc_lower:
                # Try to extract amount
                return {
                    'service': service,
                    'detected': True,
                    'pattern': pattern
                }

    return None


def flag_suspicious(transaction: Dict[str, Any]) -> bool:
    """Check if transaction is suspicious (amount > $500)."""
    try:
        amount = float(transaction.get('amount', 0))
        return amount > 500
    except ValueError:
        return False


def create_review_files(transaction: Dict[str, Any]):
    """Create review files for suspicious transactions."""
    tx_id = transaction.get('id', 'unknown')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    NEEDS_ACTION.mkdir(parents=True, exist_ok=True)
    PENDING_APPROVAL.mkdir(parents=True, exist_ok=True)

    # Needs_Action file
    needs_content = f"""---
type: finance_review
transaction_id: "{tx_id}"
amount: "{transaction.get('amount', '0')}"
description: "{transaction.get('description', '')}"
date: "{transaction.get('date', '')}"
status: pending
priority: high
---

# Finance Review Required

**Transaction ID:** {tx_id}
**Amount:** ${transaction.get('amount', '0')}
**Description:** {transaction.get('description', '')}
**Date:** {transaction.get('date', '')}

## Required Action

- [ ] Verify transaction legitimacy
- [ ] Confirm authorization
- [ ] Approve or dispute
"""

    needs_file = NEEDS_ACTION / f"FINANCE_review_{tx_id}_{timestamp}.md"
    needs_file.write_text(needs_content)

    # Pending_Approval file
    approval_content = f"""---
type: payment_review
transaction_id: "{tx_id}"
amount: "{transaction.get('amount', '0')}"
description: "{transaction.get('description', '')}"
status: pending_approval
required_by: human
---

# Payment Review Required

**Transaction ID:** {tx_id}
**Amount:** ${transaction.get('amount', '0')}
**Description:** {transaction.get('description', '')}

## Approval Required

This transaction exceeds $500 and requires human approval before posting to accounting.

- [ ] Approve transaction
- [ ] Dispute transaction
- [ ] Request more information
"""

    approval_file = PENDING_APPROVAL / f"PAYMENT_review_{tx_id}_{timestamp}.md"
    approval_file.write_text(approval_content)

    return needs_file, approval_file


def update_current_month(transactions: List[Dict[str, Any]]):
    """Update Current_Month.md with new transactions."""
    # Read existing content
    existing_content = ""
    if CURRENT_MONTH.exists():
        existing_content = CURRENT_MONTH.read_text()

    # Build new transactions section
    new_tx_section = "\n## Transactions\n\n"
    new_tx_section += "| Date | Description | Amount | Category | Status |\n"
    new_tx_section += "|------|-------------|--------|----------|--------|\n"

    for tx in transactions:
        category = tx.get('category', 'uncategorized')
        amount = float(tx.get('amount', 0))
        amount_str = f"+${amount}" if amount > 0 else f"-${abs(amount)}"
        new_tx_section += f"| {tx.get('date', '')} | {tx.get('description', '')} | {amount_str} | {category} | {tx.get('status', 'pending')} |\n"

    # Check if transactions section exists
    if "## Transactions" in existing_content:
        # Append to existing section
        parts = existing_content.split("## Transactions")
        existing_content = parts[0] + "## Transactions" + new_tx_section
    else:
        existing_content += new_tx_section

    CURRENT_MONTH.parent.mkdir(parents=True, exist_ok=True)
    CURRENT_MONTH.write_text(existing_content)


def get_dev_transactions() -> List[Dict[str, Any]]:
    """Get synthetic transactions for DEV_MODE."""
    return [
        {'id': 'dev_001', 'date': '2026-02-24', 'description': 'Netflix Subscription', 'amount': '-15.99', 'category': 'subscription', 'status': 'pending'},
        {'id': 'dev_002', 'date': '2026-02-24', 'description': 'Client Payment - Acme Corp', 'amount': '+5000.00', 'category': 'income', 'status': 'pending'},
        {'id': 'dev_003', 'date': '2026-02-24', 'description': 'AWS Monthly Bill', 'amount': '-234.50', 'category': 'subscription', 'status': 'pending'},
        {'id': 'dev_004', 'date': '2026-02-24', 'description': 'Office Supplies - Staples', 'amount': '-89.99', 'category': 'expense', 'status': 'pending'},
        {'id': 'dev_005', 'date': '2026-02-24', 'description': 'Spotify Premium', 'amount': '-9.99', 'category': 'subscription', 'status': 'pending'},
        {'id': 'dev_006', 'date': '2026-02-24', 'description': 'Large Equipment Purchase', 'amount': '-750.00', 'category': 'expense', 'status': 'pending'},
        {'id': 'dev_007', 'date': '2026-02-24', 'description': 'GitHub Enterprise', 'amount': '-21.00', 'category': 'subscription', 'status': 'pending'},
        {'id': 'dev_008', 'date': '2026-02-24', 'description': 'Client Payment - Beta Inc', 'amount': '+2500.00', 'category': 'income', 'status': 'pending'},
        {'id': 'dev_009', 'date': '2026-02-24', 'description': 'Notion Team', 'amount': '-96.00', 'category': 'subscription', 'status': 'pending'},
        {'id': 'dev_010', 'date': '2026-02-24', 'description': 'Zoom Pro', 'amount': '-14.99', 'category': 'subscription', 'status': 'pending'},
    ]


def check_new_transactions() -> List[Dict[str, Any]]:
    """Check for new transactions in the bank CSV."""
    processed_ids = load_current_transactions()
    new_transactions = []

    if DEV_MODE:
        transactions = get_dev_transactions()
    elif BANK_CSV.exists():
        transactions = []
        with open(BANK_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
    else:
        transactions = []

    for tx in transactions:
        tx_id = tx.get('id', tx.get('date', '') + tx.get('description', ''))

        if tx_id in processed_ids:
            continue

        # Detect subscription
        subscription = detect_subscription(tx.get('description', ''))
        if subscription:
            tx['subscription'] = subscription

        # Check for suspicious
        tx['suspicious'] = flag_suspicious(tx)

        new_transactions.append(tx)

    return new_transactions


def run_watcher():
    """Main finance watcher loop."""
    print(f"Finance Watcher starting...")
    print(f"DEV_MODE: {DEV_MODE}")
    print(f"Vault path: {VAULT_PATH}")
    print(f"Poll interval: {POLL_INTERVAL} seconds")

    while True:
        try:
            new_transactions = check_new_transactions()

            if new_transactions:
                processed_ids = load_current_transactions()

                for tx in new_transactions:
                    tx_id = tx.get('id', 'unknown')
                    print(f"New transaction: {tx.get('description', 'unknown')} - ${tx.get('amount', '0')}")

                    # Handle suspicious transactions
                    if tx.get('suspicious'):
                        print(f"  ⚠️ Suspicious transaction detected (> $500)")
                        create_review_files(tx)

                    # Handle subscriptions
                    if tx.get('subscription'):
                        print(f"  📦 Subscription detected: {tx['subscription'].get('service')}")

                    processed_ids.add(tx_id)

                # Update accounting
                update_current_month(new_transactions)
                save_processed_transactions(processed_ids)

                print(f"Processed {len(new_transactions)} new transactions")
            else:
                print(f"No new transactions at {datetime.now().strftime('%H:%M:%S')}")

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\nFinance Watcher stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(POLL_INTERVAL * 2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Finance Watcher")
    parser.add_argument("--once", action="store_true", help="Run once instead of loop")
    args = parser.parse_args()

    if args.once:
        transactions = check_new_transactions()
        print(f"Found {len(transactions)} new transactions")
        for tx in transactions:
            print(f"  {tx.get('description')} - ${tx.get('amount')}")
            if tx.get('suspicious'):
                print(f"    ⚠️ Suspicious!")
            if tx.get('subscription'):
                print(f"    📦 Subscription: {tx['subscription'].get('service')}")
    else:
        run_watcher()
