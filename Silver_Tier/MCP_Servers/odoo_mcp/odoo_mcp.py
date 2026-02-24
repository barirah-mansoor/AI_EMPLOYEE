#!/usr/bin/env python3
"""
Odoo MCP Server - Provides accounting operations via Odoo ERP
Tools: create_invoice, list_invoices, create_customer, get_accounting_summary, post_invoice
"""

import json
import os
import sys
import xmlrpc.client
from datetime import datetime
from pathlib import Path

# Configuration
DEV_MODE = os.environ.get("DEV_MODE", "false").lower() == "true"
ODOO_URL = os.environ.get("ODOO_URL", "http://localhost:8069")
ODOO_DB = os.environ.get("ODOO_DB", "odoo")
ODOO_USER = os.environ.get("ODOO_USER", "admin")
ODOO_PASSWORD = os.environ.get("ODOO_PASSWORD", "admin")

# For MCP server protocol
def send_json_response(data):
    """Send JSON response to stdout."""
    print(json.dumps(data))
    sys.stdout.flush()


def send_error(error):
    """Send error response."""
    print(json.dumps({"error": str(error)}))
    sys.stdout.flush()


# Dev mode mock data
MOCK_INVOICES = [
    {"id": 1, "partner_id": [1, "Acme Corp"], "amount_total": 1500.00, "state": "draft", "date": "2026-02-01"},
    {"id": 2, "partner_id": [2, "Beta Inc"], "amount_total": 2500.00, "state": "posted", "date": "2026-02-15"},
    {"id": 3, "partner_id": [1, "Acme Corp"], "amount_total": 750.00, "state": "paid", "date": "2026-02-20"},
]

MOCK_CUSTOMERS = [
    {"id": 1, "name": "Acme Corp", "email": "billing@acme.com"},
    {"id": 2, "name": "Beta Inc", "email": "accounts@beta.com"},
    {"id": 3, "name": "Gamma LLC", "email": "finance@gamma.com"},
]


def get_odoo_client():
    """Get Odoo XML-RPC client."""
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
        if not uid:
            return None

        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        return {"uid": uid, "models": models}
    except Exception as e:
        return None


def create_invoice(partner_name: str, amount: float, description: str) -> dict:
    """Create a draft invoice in Odoo."""
    if DEV_MODE:
        return {
            "success": True,
            "dev_mode": True,
            "invoice": {
                "id": f"dev_{datetime.now().timestamp()}",
                "partner_name": partner_name,
                "amount": amount,
                "description": description,
                "state": "draft",
                "created_at": datetime.now().isoformat()
            },
            "message": "DEV_MODE: Invoice created (mock)"
        }

    client = get_odoo_client()
    if not client:
        return {"error": "Cannot connect to Odoo. Check ODOO_URL and credentials."}

    try:
        # Find partner
        partner_id = client["models"].execute_kw(
            ODOO_DB, client["uid"], ODOO_PASSWORD,
            "res.partner", "search_read",
            [[["name", "=", partner_name]]],
            {"fields": ["id"], "limit": 1}
        )

        if not partner_id:
            return {"error": f"Partner '{partner_name}' not found"}

        # Create invoice
        invoice_id = client["models"].execute_kw(
            ODOO_DB, client["uid"], ODOO_PASSWORD,
            "account.move", "create",
            [{
                "partner_id": partner_id[0]["id"],
                "move_type": "out_invoice",
                "invoice_line_ids": [[0, 0, {
                    "name": description,
                    "quantity": 1,
                    "price_unit": amount,
                }]]
            }]
        )

        return {"success": True, "invoice_id": invoice_id}
    except Exception as e:
        return {"error": str(e)}


def list_invoices(state: str = None) -> dict:
    """List invoices from Odoo."""
    if DEV_MODE:
        invoices = MOCK_INVOICES
        if state:
            invoices = [inv for inv in invoices if inv["state"] == state]
        return {
            "success": True,
            "dev_mode": True,
            "invoices": invoices,
            "message": "DEV_MODE: Mock invoices returned"
        }

    client = get_odoo_client()
    if not client:
        return {"error": "Cannot connect to Odoo"}

    try:
        domain = []
        if state:
            domain.append(["state", "=", state])

        invoices = client["models"].execute_kw(
            ODOO_DB, client["uid"], ODOO_PASSWORD,
            "account.move", "search_read",
            [domain],
            {"fields": ["id", "partner_id", "amount_total", "state", "date"], "limit": 50}
        )

        return {"success": True, "invoices": invoices}
    except Exception as e:
        return {"error": str(e)}


def create_customer(name: str, email: str) -> dict:
    """Create a customer in Odoo."""
    if DEV_MODE:
        return {
            "success": True,
            "dev_mode": True,
            "customer": {
                "id": f"dev_{datetime.now().timestamp()}",
                "name": name,
                "email": email,
                "created_at": datetime.now().isoformat()
            },
            "message": "DEV_MODE: Customer created (mock)"
        }

    client = get_odoo_client()
    if not client:
        return {"error": "Cannot connect to Odoo"}

    try:
        customer_id = client["models"].execute_kw(
            ODOO_DB, client["uid"], ODOO_PASSWORD,
            "res.partner", "create",
            [{"name": name, "email": email}]
        )

        return {"success": True, "customer_id": customer_id}
    except Exception as e:
        return {"error": str(e)}


def get_accounting_summary() -> dict:
    """Get accounting summary from Odoo."""
    if DEV_MODE:
        return {
            "success": True,
            "dev_mode": True,
            "summary": {
                "total_revenue": 9750.00,
                "total_expenses": 2500.00,
                "net_profit": 7250.00,
                "outstanding_invoices": 2,
                "paid_invoices": 1,
                "as_of": datetime.now().isoformat()
            },
            "message": "DEV_MODE: Mock summary returned"
        }

    client = get_odoo_client()
    if not client:
        return {"error": "Cannot connect to Odoo"}

    try:
        # Get posted invoices
        posted = client["models"].execute_kw(
            ODOO_DB, client["uid"], ODOO_PASSWORD,
            "account.move", "search_read",
            [[["move_type", "=", "out_invoice"], ["state", "=", "posted"]]],
            {"fields": ["amount_total"], "limit": 100}
        )

        total_revenue = sum(inv["amount_total"] for inv in posted)

        return {
            "success": True,
            "summary": {
                "total_revenue": total_revenue,
                "outstanding_invoices": len(posted),
                "as_of": datetime.now().isoformat()
            }
        }
    except Exception as e:
        return {"error": str(e)}


def post_invoice(invoice_id: int) -> dict:
    """Post (validate) an invoice in Odoo. Requires HITL approval."""
    # Check if there's approval
    vault_path = Path(os.environ.get("VAULT_PATH", "/mnt/c/Users/Admin/AI_Employee_Vault"))
    approved_file = vault_path / "Approved" / f"INVOICE_{invoice_id}.md"

    if not approved_file.exists():
        return {
            "error": "Invoice posting requires HITL approval. Create Pending_Approval/INVOICE_{id}.md and get it approved."
        }

    if DEV_MODE:
        return {
            "success": True,
            "dev_mode": True,
            "invoice_id": invoice_id,
            "state": "posted",
            "message": "DEV_MODE: Invoice posted (mock)"
        }

    client = get_odoo_client()
    if not client:
        return {"error": "Cannot connect to Odoo"}

    try:
        client["models"].execute_kw(
            ODOO_DB, client["uid"], ODOO_PASSWORD,
            "account.move", "action_post",
            [[invoice_id]]
        )

        return {"success": True, "invoice_id": invoice_id, "state": "posted"}
    except Exception as e:
        return {"error": str(e)}


# MCP Server Protocol
def handle_tool(name: str, args: dict) -> dict:
    """Route tool calls to appropriate functions."""
    tools = {
        "create_invoice": lambda: create_invoice(
            args.get("partner", ""),
            args.get("amount", 0),
            args.get("description", "")
        ),
        "list_invoices": lambda: list_invoices(args.get("state")),
        "create_customer": lambda: create_customer(
            args.get("name", ""),
            args.get("email", "")
        ),
        "get_accounting_summary": lambda: get_accounting_summary(),
        "post_invoice": lambda: post_invoice(args.get("id", 0)),
    }

    if name not in tools:
        return {"error": f"Unknown tool: {name}"}

    return tools[name]()


# Main loop - read JSON from stdin
if __name__ == "__main__":
    print(f"Odoo MCP Server starting... DEV_MODE={DEV_MODE}", file=sys.stderr)

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())

            if request.get("method") == "tools/list":
                send_json_response({
                    "tools": [
                        {
                            "name": "create_invoice",
                            "description": "Create a draft invoice in Odoo",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "partner": {"type": "string", "description": "Partner/Customer name"},
                                    "amount": {"type": "number", "description": "Invoice amount"},
                                    "description": {"type": "string", "description": "Invoice description"}
                                },
                                "required": ["partner", "amount", "description"]
                            }
                        },
                        {
                            "name": "list_invoices",
                            "description": "List invoices from Odoo",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "state": {"type": "string", "description": "Filter by state (draft, posted, paid)"}
                                }
                            }
                        },
                        {
                            "name": "create_customer",
                            "description": "Create a customer in Odoo",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "Customer name"},
                                    "email": {"type": "string", "description": "Customer email"}
                                },
                                "required": ["name", "email"]
                            }
                        },
                        {
                            "name": "get_accounting_summary",
                            "description": "Get accounting summary",
                            "inputSchema": {"type": "object", "properties": {}}
                        },
                        {
                            "name": "post_invoice",
                            "description": "Post (validate) an invoice - requires HITL approval",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "number", "description": "Invoice ID"}
                                },
                                "required": ["id"]
                            }
                        }
                    ]
                })

            elif request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name")
                tool_args = request.get("params", {}).get("arguments", {})
                result = handle_tool(tool_name, tool_args)
                send_json_response({"content": [{"type": "text", "text": json.dumps(result)}]})

        except Exception as e:
            send_error(str(e))
