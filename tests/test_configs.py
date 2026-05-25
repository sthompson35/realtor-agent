import pytest
import yaml
import os
from pathlib import Path

def test_config_files_exist():
    """Test that all required config files exist"""
    config_files = [
        'realtor_agent/agent_config.yml',
        'realtor_agent/memory/global_knowledge.yml',
        'realtor_agent_knowledge_pack.yml'
    ]

    for config_file in config_files:
        assert os.path.exists(config_file), f"Config file {config_file} does not exist"

def test_config_files_valid_yaml():
    """Test that all config files are valid YAML"""
    config_files = [
        'realtor_agent/agent_config.yml',
        'realtor_agent/memory/global_knowledge.yml',
        'realtor_agent_knowledge_pack.yml',
        'bots/web_scout/bot_config.yml',
        'bots/underwriter/bot_config.yml',
        'bots/outreach/bot_config.yml',
        'bots/negotiator/bot_config.yml',
        'bots/deal_desk/bot_config.yml',
        'bots/owner_finder/bot_config.yml',
        'bots/compliance_qa/bot_config.yml'
    ]

    for config_file in config_files:
        with open(config_file, 'r') as f:
            try:
                yaml.safe_load(f)
            except yaml.YAMLError as e:
                pytest.fail(f"YAML validation failed for {config_file}: {e}")

def test_knowledge_pack_structure():
    """Test that knowledge pack has required sections"""
    with open('realtor_agent_knowledge_pack.yml', 'r') as f:
        knowledge = yaml.safe_load(f)

    required_sections = ['meta', 'operating_principles', 'capabilities_matrix', 'core_formulas']
    for section in required_sections:
        assert section in knowledge, f"Required section {section} missing from knowledge pack"

def test_agent_config_structure():
    """Test that agent config has required sections"""
    with open('realtor_agent/agent_config.yml', 'r') as f:
        config = yaml.safe_load(f)

    required_sections = ['goals', 'bots', 'compliance']
    for section in required_sections:
        assert section in config, f"Required section {section} missing from agent config"