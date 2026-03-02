#!/usr/bin/env python3
"""
Audit Logic - Financial transaction analysis and subscription detection
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


# Subscription patterns to detect
SUBSCRIPTION_PATTERNS: Dict[str, List[str]] = {
    'netflix': ['netflix', 'net flix'],
    'spotify': ['spotify'],
    'adobe': ['adobe', 'creative cloud'],
    'notion': ['notion'],
    'slack': ['slack'],
    'github': ['github', 'github enterprise'],
    'aws': ['amazon web', 'aws', 'amazon web services'],
    'google': ['google cloud', 'google workspace', 'g suite', 'google one'],
    'openai': ['openai', 'chatgpt'],
    'anthropic': ['anthropic', 'claude'],
    'zoom': ['zoom'],
    'dropbox': ['dropbox'],
    'microsoft': ['microsoft 365', 'office 365', 'azure', 'onedrive'],
    'apple': ['apple com', 'icloud', 'apple music', 'apple tv'],
    'chatgpt': ['chatgpt', 'openai plus', 'openai pro'],
    'figma': ['figma'],
    'jira': ['jira', 'atlassian'],
    'confluence': ['confluence', 'atlassian'],
    'heroku': ['heroku'],
    'digitalocean': ['digitalocean'],
}


def analyze_transaction(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a single transaction for subscriptions and anomalies.

    Args:
        transaction: Dict with keys: id, date, description, amount, category

    Returns:
        Dict with analysis results including:
        - is_subscription: bool
        - service_name: str or None
        - is_suspicious: bool
        - anomaly_reason: str or None
    """
    result = {
        'is_subscription': False,
        'service_name': None,
        'is_suspicious': False,
        'anomaly_reason': None,
    }

    description = transaction.get('description', '').lower()
    amount_str = transaction.get('amount', '0')

    # Parse amount
    try:
        amount = float(amount_str.replace('$', '').replace(',', ''))
    except (ValueError, AttributeError):
        amount = 0

    # Detect subscription
    for service, patterns in SUBSCRIPTION_PATTERNS.items():
        for pattern in patterns:
            if pattern in description:
                result['is_subscription'] = True
                result['service_name'] = service
                break

    # Check for suspicious transactions (amount > $500)
    if abs(amount) > 500:
        result['is_suspicious'] = True
        result['anomaly_reason'] = f"Amount ${abs(amount)} exceeds $500 threshold"

    # Check for unusual patterns
    if amount > 0 and 'refund' in description.lower():
        result['anomaly_reason'] = "Potential refund detected"

    return result


def flag_unused_subscriptions(
    transactions: List[Dict[str, Any]],
    days_threshold: int = 30
) -> List[Dict[str, Any]]:
    """
    Identify subscriptions that haven't been used recently.

    Args:
        transactions: List of transaction dicts
        days_threshold: Days of inactivity before flagging (default 30)

    Returns:
        List of unused subscriptions with recommendations
    """
    # Group subscriptions by service
    service_usage: Dict[str, List[Dict[str, Any]]] = {}

    for tx in transactions:
        analysis = analyze_transaction(tx)
        if analysis['is_subscription']:
            service = analysis['service_name']
            if service not in service_usage:
                service_usage[service] = []
            service_usage[service].append(tx)

    # Find unused subscriptions
    unused = []
    cutoff_date = datetime.now() - timedelta(days=days_threshold)

    for service, tx_list in service_usage.items():
        # Get most recent transaction for this service
        sorted_tx = sorted(tx_list, key=lambda x: x.get('date', ''), reverse=True)
        if sorted_tx:
            latest_date_str = sorted_tx[0].get('date', '')
            try:
                latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d')
                if latest_date < cutoff_date:
                    unused.append({
                        'service': service,
                        'last_used': latest_date_str,
                        'days_ago': (datetime.now() - latest_date).days,
                        'monthly_cost': abs(float(sorted_tx[0].get('amount', '0'))),
                        'recommendation': f"Consider canceling - {abs(float(sorted_tx[0].get('amount', '0'))) * 12}/year"
                    })
            except ValueError:
                pass

    return unused


def get_monthly_subscription_total(transactions: List[Dict[str, Any]]) -> float:
    """Calculate total monthly subscription costs."""
    total = 0
    for tx in transactions:
        analysis = analyze_transaction(tx)
        if analysis['is_subscription']:
            try:
                amount = float(tx.get('amount', '0').replace('$', '').replace(',', ''))
                total += abs(amount)
            except ValueError:
                pass
    return total


def categorize_transaction(transaction: Dict[str, Any]) -> str:
    """
    Categorize a transaction based on description and amount.

    Returns:
        Category: subscription, income, expense, transfer, or uncategorized
    """
    description = (transaction.get('description', '') or '').lower()
    amount_str = transaction.get('amount', '0')

    try:
        amount = float(amount_str.replace('$', '').replace(',', ''))
    except (ValueError, AttributeError):
        amount = 0

    # Check for subscription first
    analysis = analyze_transaction(transaction)
    if analysis['is_subscription']:
        return 'subscription'

    # Check income (positive amount)
    if amount > 0:
        return 'income'

    # Check expenses
    if amount < 0:
        # Common expense categories
        if any(kw in description for kw in ['grocery', 'food', 'restaurant', 'coffee']):
            return 'food'
        elif any(kw in description for kw in ['uber', 'lyft', 'gas', 'fuel', 'parking']):
            return 'transportation'
        elif any(kw in description for kw in ['rent', 'mortgage', 'utilities']):
            return 'housing'
        elif any(kw in description for kw in ['insurance', 'medical', 'pharmacy']):
            return 'insurance'
        else:
            return 'expense'

    return 'uncategorized'


if __name__ == "__main__":
    # Test the audit logic
    test_transactions = [
        {'id': '1', 'date': '2026-02-24', 'description': 'Netflix Subscription', 'amount': '-15.99', 'category': 'subscription'},
        {'id': '2', 'date': '2026-02-24', 'description': 'AWS Monthly Bill', 'amount': '-234.50', 'category': 'subscription'},
        {'id': '3', 'date': '2026-02-24', 'description': 'Client Payment - Acme Corp', 'amount': '5000.00', 'category': 'income'},
        {'id': '4', 'date': '2026-02-24', 'description': 'Large Purchase', 'amount': '-750.00', 'category': 'expense'},
    ]

    print("=== Transaction Analysis ===")
    for tx in test_transactions:
        analysis = analyze_transaction(tx)
        print(f"\n{tx['description']}:")
        print(f"  Is Subscription: {analysis['is_subscription']}")
        print(f"  Service: {analysis['service_name']}")
        print(f"  Suspicious: {analysis['is_suspicious']}")
        print(f"  Reason: {analysis['anomaly_reason']}")

    print("\n=== Monthly Subscription Total ===")
    total = get_monthly_subscription_total(test_transactions)
    print(f"Total: ${total:.2f}")

    print("\n=== Categorization ===")
    for tx in test_transactions:
        cat = categorize_transaction(tx)
        print(f"{tx['description']}: {cat}")
