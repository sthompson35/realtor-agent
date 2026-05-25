import pytest
import yaml
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MockOrchestrator:
    def __init__(self, agent_config_path, knowledge_path):
        with open(agent_config_path, 'r') as f:
            self.agent_config = yaml.safe_load(f)
        with open(knowledge_path, 'r') as f:
            self.knowledge = yaml.safe_load(f)

    def check_deal_approval(self, mao, risk_flags, deal_value):
        """Check if deal meets approval criteria"""
        goals = self.agent_config['goals']

        # Auto-approve criteria
        if (mao > 0 and
            len(risk_flags) <= goals['risk_tolerance']['max_risk_flags'] and
            deal_value >= goals['target_markets'][0]['price_range'][0] and
            deal_value <= goals['target_markets'][0]['price_range'][1]):
            return 'approved'

        # Escalate if high risk
        if len(risk_flags) > goals['risk_tolerance']['max_risk_flags']:
            return 'escalate'

        return 'review'

    def validate_compliance(self, action_type, data):
        """Mock compliance validation"""
        compliance = self.agent_config['compliance']

        if action_type == 'outreach':
            if not data.get('consent', False):
                return False, "Consent required for outreach"
            if data.get('dnc_violation', False):
                return False, "DNC violation detected"

        if action_type == 'scraping':
            if not compliance['tos_compliance']:
                return False, "ToS compliance disabled"

        return True, "Compliant"

def test_orchestrator_config():
    """Test orchestrator configuration loading"""
    orchestrator = MockOrchestrator('realtor_agent/agent_config.yml', 'realtor_agent_knowledge_pack.yml')

    assert 'goals' in orchestrator.agent_config
    assert 'bots' in orchestrator.agent_config
    assert 'compliance' in orchestrator.agent_config

def test_deal_approval_logic():
    """Test deal approval decision logic"""
    orchestrator = MockOrchestrator('realtor_agent/agent_config.yml', 'realtor_agent_knowledge_pack.yml')

    # Test auto-approve case
    result = orchestrator.check_deal_approval(mao=50000, risk_flags=['minor'], deal_value=75000)
    assert result == 'approved'

    # Test escalate case
    result = orchestrator.check_deal_approval(mao=30000, risk_flags=['high_risk1', 'high_risk2', 'high_risk3', 'high_risk4'], deal_value=75000)
    assert result == 'escalate'

def test_compliance_validation():
    """Test compliance validation"""
    orchestrator = MockOrchestrator('realtor_agent/agent_config.yml', 'realtor_agent_knowledge_pack.yml')

    # Test compliant outreach
    compliant, message = orchestrator.validate_compliance('outreach', {'consent': True, 'dnc_violation': False})
    assert compliant == True

    # Test non-compliant outreach
    compliant, message = orchestrator.validate_compliance('outreach', {'consent': False, 'dnc_violation': True})
    assert compliant == False
    assert "Consent required" in message or "DNC violation" in message

def test_knowledge_integration():
    """Test orchestrator uses knowledge pack"""
    orchestrator = MockOrchestrator('realtor_agent/agent_config.yml', 'realtor_agent_knowledge_pack.yml')

    # Check operating principles are accessible
    assert 'operating_principles' in orchestrator.knowledge
    assert len(orchestrator.knowledge['operating_principles']) > 0