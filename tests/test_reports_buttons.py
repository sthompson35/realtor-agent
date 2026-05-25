#!/usr/bin/env python3
"""
Test script to validate button functionality in reports.html
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_reports_buttons():
    """Test that all button functions are properly configured in reports.html"""

    reports_path = Path(__file__).parent.parent / 'web' / 'templates' / 'reports.html'

    if not reports_path.exists():
        print(f"❌ reports.html not found at {reports_path}")
        return False

    with open(reports_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for required onclick handlers
    required_handlers = [
        'generateReport(\'performance\', this)',
        'generateReport(\'financial\', this)',
        'generateReport(\'market\', this)',
        'generateReport(\'bot-performance\', this)',
        'downloadReport(1, this)',
        'deleteReport(1, this)',
        'downloadReport(2, this)',
        'deleteReport(2, this)',
        'downloadReport(3, this)',
        'deleteReport(3, this)',
        'downloadReport(4, this)',
        'deleteReport(4, this)',
        'downloadReport(\'new\', this)',
        'deleteReport(\'new\', this)',
        'deleteSchedule(1, this)',
        'deleteSchedule(2, this)',
        'deleteSchedule(3, this)',
        'openScheduleModal()'
    ]

    missing_handlers = []
    for handler in required_handlers:
        if handler not in content:
            missing_handlers.append(handler)

    if missing_handlers:
        print("❌ Missing onclick handlers:")
        for handler in missing_handlers:
            print(f"  - {handler}")
        return False

    # Check for required JavaScript functions
    required_functions = [
        'function generateReport(type, button)',
        'function downloadReport(id, button)',
        'function deleteReport(id, button)',
        'function deleteSchedule(id, button)',
        'function openScheduleModal()'
    ]

    missing_functions = []
    for func in required_functions:
        if func not in content:
            missing_functions.append(func)

    if missing_functions:
        print("❌ Missing JavaScript functions:")
        for func in missing_functions:
            print(f"  - {func}")
        return False

    # Check for RealtorAgent.showAlert usage
    if 'RealtorAgent.showAlert' not in content:
        print("❌ RealtorAgent.showAlert not found in template")
        return False

    print("✅ All button configurations validated successfully!")
    print("✅ All onclick handlers are properly configured")
    print("✅ All JavaScript functions are defined with correct parameters")
    print("✅ RealtorAgent.showAlert is properly used for user feedback")

    return True

if __name__ == '__main__':
    print("Testing reports page button functionality...")
    success = test_reports_buttons()

    if success:
        print("\n🎉 All tests passed! Button functionality should work correctly.")
    else:
        print("\n💥 Tests failed! Please check the button configurations.")
        sys.exit(1)