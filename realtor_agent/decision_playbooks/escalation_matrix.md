# Escalation Matrix

This matrix defines when issues are escalated to human operators or specialists.

## Risk-Based Escalation

| Risk Level | Triggers | Escalate To | Response Time |
|------------|----------|-------------|---------------|
| Low | 1-2 minor flags | Human Review | End of day |
| Medium | 3-4 flags or legal questions | Senior Analyst | 4 hours |
| High | 5+ flags or title issues | Attorney/Legal | Immediate |
| Critical | Compliance violation or fraud suspicion | Compliance Officer | Immediate |

## Deal Value Escalation

| Deal Value | Auto-Approval Limit | Review Required | Approver |
|------------|---------------------|-----------------|----------|
| <$50K | $40K | $40K-$50K | Analyst |
| $50K-$250K | $200K | $200K-$250K | Manager |
| $250K-$1M | $750K | $750K-$1M | Director |
| >$1M | None | All | Executive |

## Issue-Specific Escalation

### Legal/Compliance
- **Fair Housing**: Any suspicion → Compliance Officer (immediate)
- **DNC Violation**: Detected → Legal (immediate)
- **ToS Breach**: Suspected → Legal (24 hours)
- **Licensing**: Out-of-state deal → Attorney (before outreach)

### Technical
- **Data Errors**: Inconsistent comps → Data Team (4 hours)
- **Bot Failures**: 3+ consecutive errors → DevOps (1 hour)
- **API Limits**: Rate limited → Admin (end of day)

### Operational
- **Seller Hostile**: Threats or abuse → Manager (immediate)
- **Competitor Interference**: Detected → Legal (24 hours)
- **Market Changes**: Sudden comp shifts → Analyst (end of day)

## Escalation Process

1. **Detection**: Bot flags issue with evidence
2. **Log**: Record in deal log with timestamp and details
3. **Notify**: Alert appropriate party via configured channel
4. **Pause**: Halt automated actions until resolution
5. **Review**: Human reviews context and decides next steps
6. **Resolve**: Update deal status and resume if appropriate

## De-Escalation

Issues can be de-escalated if:
- Risk mitigated with new information
- Human override with documented rationale
- False positive confirmed

All escalations tracked for process improvement.
