#!/usr/bin/env python3
"""
Realtor Agent Webhook Client
A utility for sending webhooks to the Realtor Agent system.
"""

import os
import json
import sys
import time
import hashlib
import hmac
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

class RealtorAgentWebhookClient:
    """Client for sending webhooks to Realtor Agent system."""

    def __init__(self, base_url: str = None, api_key: str = None, webhook_secret: str = None):
        """
        Initialize webhook client.

        Args:
            base_url: Base URL of the Realtor Agent API
            api_key: API key for authentication
            webhook_secret: Secret for HMAC signature generation
        """
        self.base_url = base_url or os.getenv('REALTOR_AGENT_WEBHOOK_URL', 'http://localhost:5000')
        self.api_key = api_key or os.getenv('REALTOR_AGENT_API_KEY', 'test_key')
        self.webhook_secret = webhook_secret or os.getenv('WEBHOOK_SECRET', 'default_webhook_secret')

        # Remove trailing slash from base URL
        self.base_url = self.base_url.rstrip('/')

    def _generate_signature(self, payload: str, timestamp: str) -> str:
        """Generate HMAC signature for webhook payload."""
        message = f"{timestamp}.{payload}"
        signature = hmac.new(
            self.webhook_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"

    def _send_webhook(self, endpoint: str, event: str, data: Dict[str, Any],
                     source: str, use_signature: bool = True) -> Dict[str, Any]:
        """
        Send webhook to specified endpoint.

        Args:
            endpoint: API endpoint path
            event: Event type
            data: Event data
            source: Source identifier
            use_signature: Whether to use HMAC signature authentication

        Returns:
            Response from server
        """
        url = f"{self.base_url}{endpoint}"

        payload = {
            "event": event,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": source,
            "data": data
        }

        payload_json = json.dumps(payload, separators=(',', ':'))

        headers = {
            "Content-Type": "application/json"
        }

        if use_signature:
            # Use HMAC signature authentication
            timestamp = str(int(datetime.utcnow().timestamp()))
            signature = self._generate_signature(payload_json, timestamp)

            headers.update({
                "X-Webhook-Signature": signature,
                "X-Webhook-Timestamp": timestamp
            })
        else:
            # Use API key authentication
            headers["X-API-Key"] = self.api_key

        try:
            response = requests.post(url, data=payload_json, headers=headers, timeout=30)
            return {
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "success": response.status_code in [200, 201]
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": None,
                "response": f"Request failed: {str(e)}",
                "success": False
            }

    # Property Webhook Methods
    def send_property_listed(self, property_data: Dict[str, Any], source: str = "external_api") -> Dict[str, Any]:
        """Send new property listing webhook."""
        return self._send_webhook(
            "/api/webhooks/properties/new",
            "property.listed",
            property_data,
            source
        )

    def send_property_price_change(self, price_change_data: Dict[str, Any], source: str = "mls_feed") -> Dict[str, Any]:
        """Send property price change webhook."""
        return self._send_webhook(
            "/api/webhooks/properties/price_change",
            "property.price_changed",
            price_change_data,
            source
        )

    def send_property_status_change(self, status_change_data: Dict[str, Any], source: str = "realtor_api") -> Dict[str, Any]:
        """Send property status change webhook."""
        return self._send_webhook(
            "/api/webhooks/properties/status_change",
            "property.status_changed",
            status_change_data,
            source
        )

    # Lead Webhook Methods
    def send_lead_submitted(self, lead_data: Dict[str, Any], source: str = "website_form") -> Dict[str, Any]:
        """Send new lead submission webhook."""
        return self._send_webhook(
            "/api/webhooks/leads/new",
            "lead.submitted",
            lead_data,
            source
        )

    def send_lead_status_update(self, status_update_data: Dict[str, Any], source: str = "crm_system") -> Dict[str, Any]:
        """Send lead status update webhook."""
        return self._send_webhook(
            "/api/webhooks/leads/status_update",
            "lead.status_updated",
            status_update_data,
            source
        )

    # Transaction Webhook Methods
    def send_offer_submitted(self, offer_data: Dict[str, Any], source: str = "portal_system") -> Dict[str, Any]:
        """Send offer submission webhook."""
        return self._send_webhook(
            "/api/webhooks/transactions/offer_submitted",
            "transaction.offer_submitted",
            offer_data,
            source
        )

    def send_closing_update(self, closing_data: Dict[str, Any], source: str = "title_company") -> Dict[str, Any]:
        """Send closing update webhook."""
        return self._send_webhook(
            "/api/webhooks/transactions/closing_update",
            "transaction.closing_updated",
            closing_data,
            source
        )

    # Compliance Webhook Methods
    def send_compliance_alert(self, alert_data: Dict[str, Any], source: str = "compliance_monitor") -> Dict[str, Any]:
        """Send compliance alert webhook."""
        return self._send_webhook(
            "/api/webhooks/compliance/alert",
            "compliance.alert",
            alert_data,
            source
        )

    # Data Synchronization Methods
    def send_data_sync(self, sync_data: Dict[str, Any], source: str = "external_crm") -> Dict[str, Any]:
        """Send data synchronization webhook."""
        return self._send_webhook(
            "/api/webhooks/sync/data",
            "sync.data_update",
            sync_data,
            source
        )

    # Test Methods
    def test_webhook(self, test_type: str = "general") -> Dict[str, Any]:
        """Send test webhook."""
        test_data = {"test_type": test_type}

        if test_type == "signature_verification":
            # For signature verification test, we need to send with signature
            return self._send_webhook(
                "/api/webhooks/test",
                "test.signature_verification",
                test_data,
                "test_client"
            )
        else:
            # For general test, use API key auth
            return self._send_webhook(
                "/api/webhooks/test",
                "test.general",
                test_data,
                "test_client",
                use_signature=False
            )

    def get_webhook_stats(self) -> Dict[str, Any]:
        """Get webhook processing statistics."""
        url = f"{self.base_url}/api/webhooks/stats"
        headers = {"X-API-Key": self.api_key}

        try:
            response = requests.get(url, headers=headers, timeout=30)
            return {
                "status_code": response.status_code,
                "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "success": response.status_code == 200
            }
        except requests.exceptions.RequestException as e:
            return {
                "status_code": None,
                "response": f"Request failed: {str(e)}",
                "success": False
            }


def main():
    """Command-line interface for webhook client."""
    import argparse

    parser = argparse.ArgumentParser(description="Realtor Agent Webhook Client")
    parser.add_argument("--url", help="Realtor Agent API URL")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--secret", help="Webhook secret for HMAC signatures")
    parser.add_argument("--source", default="cli_client", help="Source identifier")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Property commands
    prop_parser = subparsers.add_parser("property", help="Property-related webhooks")
    prop_subparsers = prop_parser.add_subparsers(dest="property_command")

    prop_listed = prop_subparsers.add_parser("listed", help="Send new property listing")
    prop_listed.add_argument("--data-file", required=True, help="JSON file with property data")

    prop_price = prop_subparsers.add_parser("price-change", help="Send property price change")
    prop_price.add_argument("--data-file", required=True, help="JSON file with price change data")

    prop_status = prop_subparsers.add_parser("status-change", help="Send property status change")
    prop_status.add_argument("--data-file", required=True, help="JSON file with status change data")

    # Lead commands
    lead_parser = subparsers.add_parser("lead", help="Lead-related webhooks")
    lead_subparsers = lead_parser.add_subparsers(dest="lead_command")

    lead_new = lead_subparsers.add_parser("new", help="Send new lead")
    lead_new.add_argument("--data-file", required=True, help="JSON file with lead data")

    lead_update = lead_subparsers.add_parser("status-update", help="Send lead status update")
    lead_update.add_argument("--data-file", required=True, help="JSON file with status update data")

    # Transaction commands
    txn_parser = subparsers.add_parser("transaction", help="Transaction-related webhooks")
    txn_subparsers = txn_parser.add_subparsers(dest="transaction_command")

    txn_offer = txn_subparsers.add_parser("offer", help="Send offer submission")
    txn_offer.add_argument("--data-file", required=True, help="JSON file with offer data")

    txn_closing = txn_subparsers.add_parser("closing", help="Send closing update")
    txn_closing.add_argument("--data-file", required=True, help="JSON file with closing data")

    # Compliance commands
    compliance_parser = subparsers.add_parser("compliance", help="Send compliance alert")
    compliance_parser.add_argument("--data-file", required=True, help="JSON file with alert data")

    # Sync commands
    sync_parser = subparsers.add_parser("sync", help="Send data synchronization")
    sync_parser.add_argument("--data-file", required=True, help="JSON file with sync data")

    # Test commands
    test_parser = subparsers.add_parser("test", help="Test webhook functionality")
    test_parser.add_argument("--type", default="general", choices=["general", "signature"], help="Test type")

    # Stats command
    subparsers.add_parser("stats", help="Get webhook statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize client
    client = RealtorAgentWebhookClient(
        base_url=args.url,
        api_key=args.api_key,
        webhook_secret=args.secret
    )

    try:
        if args.command == "property":
            if args.property_command == "listed":
                with open(args.data_file, 'r') as f:
                    data = json.load(f)
                result = client.send_property_listed(data, args.source)

            elif args.property_command == "price-change":
                with open(args.data_file, 'r') as f:
                    data = json.load(f)
                result = client.send_property_price_change(data, args.source)

            elif args.property_command == "status-change":
                with open(args.data_file, 'r') as f:
                    data = json.load(f)
                result = client.send_property_status_change(data, args.source)

        elif args.command == "lead":
            if args.lead_command == "new":
                with open(args.data_file, 'r') as f:
                    data = json.load(f)
                result = client.send_lead_submitted(data, args.source)

            elif args.lead_command == "status-update":
                with open(args.data_file, 'r') as f:
                    data = json.load(f)
                result = client.send_lead_status_update(data, args.source)

        elif args.command == "transaction":
            if args.transaction_command == "offer":
                with open(args.data_file, 'r') as f:
                    data = json.load(f)
                result = client.send_offer_submitted(data, args.source)

            elif args.transaction_command == "closing":
                with open(args.data_file, 'r') as f:
                    data = json.load(f)
                result = client.send_closing_update(data, args.source)

        elif args.command == "compliance":
            with open(args.data_file, 'r') as f:
                data = json.load(f)
            result = client.send_compliance_alert(data, args.source)

        elif args.command == "sync":
            with open(args.data_file, 'r') as f:
                data = json.load(f)
            result = client.send_data_sync(data, args.source)

        elif args.command == "test":
            test_type = "signature_verification" if args.type == "signature" else "general"
            result = client.test_webhook(test_type)

        elif args.command == "stats":
            result = client.get_webhook_stats()

        # Print result
        if result["success"]:
            print("✅ Webhook sent successfully!")
            print(f"Status Code: {result['status_code']}")
            print(f"Response: {json.dumps(result['response'], indent=2)}")
        else:
            print("❌ Webhook failed!")
            print(f"Status Code: {result['status_code']}")
            print(f"Error: {result['response']}")
            sys.exit(1)

    except FileNotFoundError:
        print(f"❌ Error: File not found: {args.data_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in file: {args.data_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()