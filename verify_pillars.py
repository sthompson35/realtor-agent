"""Full pillar verification across all 12 feature areas."""
import json, sys
from web_server import app

client = app.test_client()
passed = failed = 0


def check(label, method, url, body=None, expect_status=(200, 201), expect_key=None):
    global passed, failed
    if method == "POST":
        r = client.post(url, data=json.dumps(body or {}), content_type="application/json")
    elif method == "PATCH":
        r = client.patch(url, data=json.dumps(body or {}), content_type="application/json")
    elif method == "DELETE":
        r = client.delete(url)
    else:
        r = client.get(url)
    ok = r.status_code in expect_status
    if ok and expect_key and r.content_type.startswith("application/json"):
        d = json.loads(r.data)
        ok = expect_key in d
    if ok:
        passed += 1
        print(f"  PASS [{label}]  {method} {url}  {r.status_code}")
    else:
        failed += 1
        preview = r.data[:120].decode(errors="ignore")
        print(f"  FAIL [{label}]  {method} {url}  {r.status_code}  {preview}")


CS1 = dict(
    contract_price=85000, arv=155000, rehab_cost=28000,
    hold_months=5, monthly_rent=1100, taxes=1200, insurance=900,
)

print("=== PILLAR 1: Core Pages ===")
for page in ["/", "/deals", "/deals/pipeline", "/bots", "/analytics",
             "/reports", "/settings", "/contacts", "/training", "/training/3"]:
    check(f"page {page}", "GET", page, expect_status=(200,))

print()
print("=== PILLAR 2: Read API ===")
check("stats",            "GET", "/api/stats",           expect_key="total_deals")
check("deals list",       "GET", "/api/deals",            expect_key="deals")
check("pipeline",         "GET", "/api/pipeline",         expect_key="stages")
check("bots status",      "GET", "/api/bots/status")
check("recent activity",  "GET", "/api/recent-activity")
check("system status",    "GET", "/api/system-status",   expect_key="database")
check("analytics",        "GET", "/api/analytics",       expect_key="strategy_performance")
check("closed deals",     "GET", "/api/closed-deals")
check("schedule",         "GET", "/api/schedule")
check("health",           "GET", "/health",              expect_key="status")

print()
print("=== PILLAR 3: Deal CRUD + Underwriter ===")
check("quick calc", "POST", "/api/calculate", CS1, expect_key="strategies")
check("create deal", "POST", "/api/deals",
      dict(address="123 Test St", contract_price=80000, arv=150000, rehab_cost=25000),
      expect_key="success")
deals_r = client.get("/api/deals")
deals = json.loads(deals_r.data).get("deals", [])
if deals:
    did = deals[0]["id"]
    check("get deal",        "GET",   f"/api/deals/{did}",        expect_key="strategies")
    check("patch deal",      "PATCH", f"/api/deals/{did}",        dict(status="qualified", notes="verified"), expect_key="success")
    check("edit deal full",  "PATCH", f"/api/deals/{did}/edit",   dict(arv=155000, monthly_rent=1200), expect_key="success")
    check("underwrite",      "POST",  f"/api/deals/{did}/underwrite", expect_key="success")
    check("activity list",   "GET",   f"/api/deals/{did}/activity")
    check("activity create", "POST",  f"/api/deals/{did}/activity",
          dict(activity_type="note", description="Test note"), expect_key="success")
    check("documents list",  "GET",   f"/api/deals/{did}/documents")

print()
print("=== PILLAR 4: Phase 3 — Pipeline Automation ===")
check("leads generate",  "POST", "/api/leads/generate",   dict(num_leads=2),   expect_status=(200,201,202), expect_key="run_id")
check("auto find",       "POST", "/api/deals/auto-find",  dict(max_deals=2),   expect_status=(200,201,202), expect_key="run_id")
check("pipeline metrics","GET",  "/api/pipeline/metrics", expect_key="weighted_pipeline_value")

print()
print("=== PILLAR 5: Phase 4 — Auth ===")
check("register",  "POST", "/api/auth/register",
      dict(username="testuser99", email="t99@test.com", password="Test1234!"),
      expect_status=(200, 201, 409))
check("login",     "POST", "/api/auth/login",
      dict(username="testuser99", password="Test1234!"),
      expect_status=(200, 401))
check("auth me",   "GET",  "/api/auth/me", expect_status=(200, 401))
check("logout",    "POST", "/api/auth/logout", expect_key="success")

print()
print("=== PILLAR 6: Phase 4 — Contacts ===")
check("contacts list",   "GET",  "/api/contacts",  expect_key="contacts")
check("contacts create", "POST", "/api/contacts",
      dict(name="Jane Doe", contact_type="owner", phone="573-555-0001"),
      expect_key="success")
contacts_r = client.get("/api/contacts")
contacts = json.loads(contacts_r.data).get("contacts", [])
if contacts:
    cid = contacts[0]["id"]
    check("contact get",    "GET",   f"/api/contacts/{cid}", expect_key="name")
    check("contact update", "PATCH", f"/api/contacts/{cid}", dict(notes="VIP"), expect_key="success")
    check("contact delete", "DELETE",f"/api/contacts/{cid}", expect_key="success")

print()
print("=== PILLAR 7: Phase 4 — Notifications ===")
check("notif list",    "GET",   "/api/notifications",           expect_status=(200,))
check("notif count",   "GET",   "/api/notifications/count",     expect_key="unread")
check("notif create",  "POST",  "/api/notifications",
      dict(title="Test", message="Hello"), expect_key="success")
check("notif read-all","PATCH", "/api/notifications/read-all",  expect_key="success")

print()
print("=== PILLAR 8: Phase 4 — Settings ===")
check("settings get",    "GET",   "/api/settings",  expect_key="flip_profit_target_pct")
check("settings update", "PATCH", "/api/settings",
      dict(flip_profit_target_pct=0.22, dark_mode=True), expect_key="success")

print()
print("=== PILLAR 9: Phase 4 — Reports ===")
check("report performance", "GET", "/api/reports/performance", expect_key="funnel")
check("report financial",   "GET", "/api/reports/financial",   expect_key="pipeline_value")
check("report summary",     "GET", "/api/reports/summary",     expect_key="performance")

print()
print("=== PILLAR 10: Phase 4 — Export ===")
r_csv = client.get("/api/deals/export?format=csv")
r_xl  = client.get("/api/deals/export?format=excel")
if r_csv.status_code == 200:
    passed += 1
    print(f"  PASS [export csv]   {r_csv.status_code}  {r_csv.content_type}")
else:
    failed += 1
    print(f"  FAIL [export csv]   {r_csv.status_code}")
if r_xl.status_code == 200:
    passed += 1
    print(f"  PASS [export excel] {r_xl.status_code}  {r_xl.content_type}")
else:
    failed += 1
    print(f"  FAIL [export excel] {r_xl.status_code}")

print()
print("=== PILLAR 11: Training Workbook — 10 Calc Engines ===")
check("sensitivity",   "POST", "/api/calculate/sensitivity",  CS1, expect_key="matrix")
check("stress test",   "POST", "/api/calculate/stress-test",  CS1, expect_key="scenarios")
check("exit strategy", "POST", "/api/calculate/exit-strategy",CS1, expect_key="recommended")
check("wholesale MAO", "POST", "/api/calculate/wholesale",
      dict(arv=105000, rehab_cost=38000), expect_key="recommended_mao")
check("taxes flip",    "POST", "/api/calculate/taxes",
      dict(net_profit=29600, strategy="flip", purchase_price=85000),
      expect_key="after_tax_profit")
check("taxes hold",    "POST", "/api/calculate/taxes",
      dict(net_profit=12000, strategy="hold", purchase_price=62000, hold_years=2.0),
      expect_key="depreciation_benefit")
check("draw schedule", "POST", "/api/calculate/draw-schedule",
      dict(rehab_cost=95000), expect_key="phases")
check("comps",         "POST", "/api/calculate/comps",
      dict(
          subject=dict(sqft=1550, beds=3, baths=2, age=30, condition_score=3),
          comps=[
              dict(address="Comp A", sale_price=158000, sqft=1550, beds=3, baths=2, age=30, condition_score=3),
              dict(address="Comp B", sale_price=165000, sqft=1600, beds=3, baths=2, age=28, condition_score=4),
          ],
      ),
      expect_key="reconciled_arv")
check("compare",       "POST", "/api/calculate/compare",
      dict(properties=[
          dict(name="CS1", price=85000, roi_pct=23.5, cash_flow=0,    equity_capture=42000, cap_rate_pct=7.0),
          dict(name="CS5", price=78000, roi_pct=29.0, cash_flow=1200, equity_capture=55000, cap_rate_pct=8.0),
      ]),
      expect_key="properties")
check("jv waterfall",  "POST", "/api/calculate/jv",
      dict(
          total_profit=45000, total_capital=220000, management_fee_pct=0.02,
          partners=[
              dict(name="Investor", capital=154000, preferred_return_pct=0.08, profit_split_pct=0.50),
              dict(name="Operator", capital=66000,  preferred_return_pct=0.08, profit_split_pct=0.50),
          ],
      ),
      expect_key="partners")

print()
print("=== PILLAR 12: Seed Data ===")
check("seed case studies", "POST", "/api/seed/case-studies",
      dict(run_underwriter=False), expect_key="success")
# Verify CS deals show up in DB
deals2 = json.loads(client.get("/api/deals").data).get("deals", [])
cs_deals = [d for d in deals2 if d.get("deal_id", "").startswith("CS")]
print(f"  INFO  {len(cs_deals)} case study deals found in DB")
if len(cs_deals) >= 5:
    passed += 1
    print(f"  PASS [seed verification]  {len(cs_deals)} CS deals in DB")
else:
    failed += 1
    print(f"  FAIL [seed verification]  only {len(cs_deals)} CS deals found (expected 5)")

print()
print("=" * 44)
print(f"TOTAL: {passed} PASSED  |  {failed} FAILED")
if failed > 0:
    sys.exit(1)
