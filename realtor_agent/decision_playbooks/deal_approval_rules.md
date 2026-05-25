# Deal Approval Rules

These rules govern when deals are automatically approved, require human review, or are rejected.

## Automatic Approval Criteria

A deal is auto-approved if ALL of the following are met:

1. **MAO Positive**: MAO > 0 with 20%+ profit margin
2. **Risk Flags**: ≤ 1 low-risk flag (no title issues, physical damage, or zoning problems)
3. **Market Fit**: Property in target market (state/county/property type/price range)
4. **Compliance**: All compliance checks pass (fair housing, DNC, ToS)
5. **Data Quality**: Underwriting based on recent comps (< 90 days) and verified data

## Human Review Required

Escalate for human approval if ANY of the following:

1. **MAO Marginal**: 10-20% profit margin OR MAO < $10,000
2. **Risk Flags**: 2-3 medium-risk flags (e.g., potential liens, older roof, flood zone)
3. **Unusual Structure**: Owner finance with balloon < 5 years OR interest > 8%
4. **High Value**: Offer > $250,000
5. **New Market**: First deal in county/state
6. **Seller Resistance**: Multiple objections or counteroffers

## Automatic Rejection

Reject immediately if ANY of the following:

1. **MAO Negative**: MAO ≤ 0 OR profit margin < 10%
2. **High Risk**: ≥ 4 risk flags OR critical issues (no access, clouded title, floodway)
3. **Non-Compliance**: Violates fair housing, spam laws, or ToS
4. **Data Gaps**: Missing key data (no comps, unknown zoning, unverified owner)
5. **Out of Scope**: Property type not in configured scope (e.g., commercial if not enabled)

## Risk Flag Definitions

- **Low Risk**: Minor issues (cosmetic repairs, older HVAC)
- **Medium Risk**: Significant but manageable (roof replacement needed, lien to clear)
- **High Risk**: Deal-breakers (foundation issues, no utilities, title defects)

## Override Rules

Human can override auto-rejection for strategic reasons, but must document rationale.

All approvals/rejections logged with criteria met/failed.
