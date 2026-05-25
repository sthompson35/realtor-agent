#!/usr/bin/env python3
"""
Test script to verify the Master Guide integration is working properly.
"""

import requests
import sys

def test_route(url, description, file):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            result = f"OK {description}: {url} - OK\n"
            print(result.strip())
            file.write(result)
            return True
        else:
            result = f"FAIL {description}: {url} - Status {response.status_code}\n"
            print(result.strip())
            file.write(result)
            return False
    except Exception as e:
        result = f"FAIL {description}: {url} - Error: {e}\n"
        print(result.strip())
        file.write(result)
        return False

def main():
    base_url = "http://localhost:5001"

    routes = [
        ("/", "Dashboard"),
        ("/master-guide", "Master Guide Table of Contents"),
        ("/master-guide/executive-summary", "Executive Summary"),
        ("/master-guide/county-examples", "County Examples"),
        ("/master-guide/resource-framework", "Resource Framework"),
        ("/master-guide/formulas", "Investment Formulas"),
        ("/master-guide/contact-database", "Contact Database"),
        ("/master-guide/strategies", "Implementation Strategies"),
        ("/master-guide/action-plans", "Action Plans"),
        ("/master-guide/pro-tips", "Pro Tips"),
        ("/master-guide/pitfalls", "Common Pitfalls"),
    ]

    print("Testing Master Guide Integration...")
    print("=" * 50)

    with open("test_results.txt", "w") as file:
        success_count = 0
        for route, description in routes:
            if test_route(base_url + route, description, file):
                success_count += 1

        print("=" * 50)
        print(f"Test Results: {success_count}/{len(routes)} routes working")

        file.write("=" * 50 + "\n")
        file.write(f"Test Results: {success_count}/{len(routes)} routes working\n")

        if success_count == len(routes):
            message = "✅ All routes are working!\n"
            print(message.strip())
            file.write(message)
            return 0
        else:
            message = f"❌ {len(routes) - success_count} routes failed\n"
            print(message.strip())
            file.write(message)
            return 1

if __name__ == "__main__":
    sys.exit(main())