#!/usr/bin/env python3
"""
Comprehensive Realtor Agent System Scanner and Test Runner
Scans the entire realtor_agent folder and runs all tests
"""

import os
import sys
import yaml
import json
from pathlib import Path
import subprocess

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def scan_folder_structure():
    """Scan and display folder structure"""
    print_header("📁 FOLDER STRUCTURE SCAN")
    
    base_path = Path(__file__).parent
    
    # Define structure to scan
    key_paths = {
        'Configurations': ['*.yml', '*.yaml'],
        'Python Scripts': ['*.py'],
        'Documentation': ['*.md'],
        'Data Files': ['*.json'],
        'Bots': ['bots/*/bot_config.yml'],
        'Decision Playbooks': ['realtor_agent/decision_playbooks/*.md'],
        'Prompts': ['realtor_agent/prompts/*.txt'],
        'Tests': ['tests/*.py']
    }
    
    results = {}
    
    for category, patterns in key_paths.items():
        files = []
        for pattern in patterns:
            files.extend(base_path.glob(pattern))
        results[category] = len(files)
        print(f"✅ {category}: {len(files)} files")
    
    return results

def validate_configurations():
    """Validate all YAML configuration files"""
    print_header("⚙️ CONFIGURATION VALIDATION")
    
    config_files = [
        'realtor_agent/agent_config.yml',
        'realtor_agent_knowledge_pack.yml',
        'realtor_agent/memory/global_knowledge.yml',
        'bots/web_scout/bot_config.yml',
        'bots/underwriter/bot_config.yml',
        'bots/outreach/bot_config.yml',
        'bots/negotiator/bot_config.yml',
        'bots/deal_desk/bot_config.yml',
        'bots/owner_finder/bot_config.yml',
        'bots/compliance_qa/bot_config.yml'
    ]
    
    valid = 0
    invalid = 0
    
    for config_file in config_files:
        try:
            with open(config_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {config_file}")
            valid += 1
        except Exception as e:
            print(f"❌ {config_file}: {e}")
            invalid += 1
    
    print(f"\n📊 Results: {valid} valid, {invalid} invalid")
    return valid, invalid

def check_documentation():
    """Check documentation completeness"""
    print_header("📚 DOCUMENTATION CHECK")
    
    doc_files = [
        ('README.md', 'Main documentation'),
        ('SETUP_GUIDE.md', 'Setup instructions'),
        ('master_guide.md', 'Master guide'),
        ('TEST_REPORT.md', 'Test report'),
        ('DEPLOYMENT_SUMMARY.md', 'Deployment info'),
        ('INTEGRATION_COMPLETE.md', 'Integration status')
    ]
    
    found = 0
    for doc_file, description in doc_files:
        if os.path.exists(doc_file):
            size = os.path.getsize(doc_file) / 1024
            print(f"✅ {doc_file} ({size:.1f} KB) - {description}")
            found += 1
        else:
            print(f"❌ {doc_file} - {description} (MISSING)")
    
    print(f"\n📊 Found: {found}/{len(doc_files)} documentation files")
    return found

def scan_bots():
    """Scan bot configurations"""
    print_header("🤖 BOT CONFIGURATION SCAN")
    
    bots_dir = Path('bots')
    if not bots_dir.exists():
        print("❌ Bots directory not found")
        return 0
    
    bot_dirs = [d for d in bots_dir.iterdir() if d.is_dir()]
    
    bot_count = 0
    for bot_dir in bot_dirs:
        config_file = bot_dir / 'bot_config.yml'
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                enabled = config.get('enabled', False)
                status = "🟢 ENABLED" if enabled else "🔴 DISABLED"
                print(f"{status} {bot_dir.name}")
                bot_count += 1
            except Exception as e:
                print(f"❌ {bot_dir.name}: Error loading config - {e}")
        else:
            print(f"⚠️  {bot_dir.name}: No config file")
    
    print(f"\n📊 Total bots: {bot_count}")
    return bot_count

def check_database():
    """Check database status"""
    print_header("💾 DATABASE CHECK")
    
    db_file = 'data/realtor_agent.db'
    if os.path.exists(db_file):
        size = os.path.getsize(db_file) / 1024
        print(f"✅ Database exists: {db_file} ({size:.1f} KB)")
        return True
    else:
        print(f"⚠️  Database not found: {db_file}")
        print("   (Database will be created on first run)")
        return False

def scan_python_files():
    """Scan Python files"""
    print_header("🐍 PYTHON FILES SCAN")
    
    py_files = list(Path('.').rglob('*.py'))
    
    categories = {
        'Main Scripts': [],
        'Bot Files': [],
        'Test Files': [],
        'Utility Files': [],
        'Other': []
    }
    
    for py_file in py_files:
        path_str = str(py_file)
        if 'test' in path_str.lower():
            categories['Test Files'].append(py_file)
        elif 'bot' in path_str.lower():
            categories['Bot Files'].append(py_file)
        elif any(x in path_str for x in ['util', 'helper', 'config']):
            categories['Utility Files'].append(py_file)
        elif py_file.parent == Path('.'):
            categories['Main Scripts'].append(py_file)
        else:
            categories['Other'].append(py_file)
    
    for category, files in categories.items():
        if files:
            print(f"\n{category}: {len(files)} files")
            for f in sorted(files)[:10]:  # Show first 10
                print(f"  - {f}")
            if len(files) > 10:
                print(f"  ... and {len(files) - 10} more")
    
    return len(py_files)

def run_test_system():
    """Run the main test system"""
    print_header("🧪 RUNNING TEST SYSTEM")
    
    try:
        result = subprocess.run(
            [sys.executable, 'test_system.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Test system timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running test system: {e}")
        return False

def run_pytest():
    """Run pytest on tests directory"""
    print_header("🧪 RUNNING PYTEST")
    
    if not os.path.exists('tests'):
        print("⚠️  No tests directory found")
        return None
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'tests/', '-v'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Pytest timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False

def generate_summary_report(results):
    """Generate summary report"""
    print_header("📊 SUMMARY REPORT")
    
    print("System Scan Results:")
    print(f"  ✅ Configuration Files: {results['configs'][0]} valid, {results['configs'][1]} invalid")
    print(f"  ✅ Documentation Files: {results['docs']} found")
    print(f"  ✅ Bot Configurations: {results['bots']} bots")
    print(f"  ✅ Python Files: {results['py_files']} files")
    print(f"  ✅ Database: {'Present' if results['database'] else 'Not created yet'}")
    
    print("\nTest Results:")
    test_status = "✅ PASSED" if results['test_system'] else "❌ FAILED"
    print(f"  Test System: {test_status}")
    
    if results['pytest'] is not None:
        pytest_status = "✅ PASSED" if results['pytest'] else "❌ FAILED"
        print(f"  Pytest: {pytest_status}")
    else:
        print(f"  Pytest: ⚠️  No tests found")
    
    # Overall status
    print("\n" + "="*80)
    if results['test_system'] and (results['pytest'] is None or results['pytest']):
        print("🎉 OVERALL STATUS: ALL TESTS PASSED - SYSTEM READY")
    else:
        print("⚠️  OVERALL STATUS: SOME TESTS FAILED - REVIEW NEEDED")
    print("="*80 + "\n")

def main():
    """Main execution"""
    print("\n" + "="*80)
    print("  🔍 REALTOR AGENT SYSTEM - COMPREHENSIVE SCAN & TEST")
    print("="*80)
    
    results = {}
    
    # Scan folder structure
    scan_folder_structure()
    
    # Validate configurations
    results['configs'] = validate_configurations()
    
    # Check documentation
    results['docs'] = check_documentation()
    
    # Scan bots
    results['bots'] = scan_bots()
    
    # Check database
    results['database'] = check_database()
    
    # Scan Python files
    results['py_files'] = scan_python_files()
    
    # Run test system
    results['test_system'] = run_test_system()
    
    # Run pytest
    results['pytest'] = run_pytest()
    
    # Generate summary
    generate_summary_report(results)
    
    return 0 if results['test_system'] else 1

if __name__ == "__main__":
    sys.exit(main())
