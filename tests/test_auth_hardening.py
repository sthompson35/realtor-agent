"""
Tests for authentication and authorization hardening in web_server.py.

Verifies:
- Anonymous browser access to protected page routes redirects to /login
- Anonymous API access to protected endpoints returns 401 JSON
- Authenticated session can access protected routes
- Public routes (login page, health, auth API) remain accessible without auth
"""
import os
import sys
import pytest

# Set required env vars BEFORE importing web_server so the secret-key check passes
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")


@pytest.fixture(scope="module")
def client():
    """Provide a Flask test client with TESTING mode enabled."""
    # Import here (after env vars are set) to avoid RuntimeError on missing SECRET_KEY
    from web_server import app as flask_app

    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Anonymous access — page routes must redirect to /login
# ---------------------------------------------------------------------------

PROTECTED_PAGE_ROUTES = [
    "/",
    "/deals",
    "/deals/new",
    "/deals/pipeline",
    "/deals/archived",
    "/bots",
    "/analytics",
    "/reports",
    "/contacts",
    "/settings",
    "/training",
    "/formulas",
    "/toolkit-dashboard",
    "/enhanced-deals",
]


@pytest.mark.parametrize("path", PROTECTED_PAGE_ROUTES)
def test_anonymous_page_redirects_to_login(client, path):
    """Unauthenticated GET requests to dashboard pages must redirect to /login."""
    resp = client.get(path)
    assert resp.status_code in (301, 302), (
        f"Expected redirect for {path}, got {resp.status_code}"
    )
    location = resp.headers.get("Location", "")
    assert "/login" in location, (
        f"Redirect for {path} should point to /login, got {location!r}"
    )


# ---------------------------------------------------------------------------
# Anonymous access — API routes must return 401
# ---------------------------------------------------------------------------

PROTECTED_API_ROUTES = [
    ("GET",  "/api/stats"),
    ("GET",  "/api/deals"),
    ("GET",  "/api/pipeline"),
    ("GET",  "/api/bots/status"),
    ("GET",  "/api/analytics"),
    ("GET",  "/api/closed-deals"),
    ("GET",  "/api/recent-activity"),
    ("GET",  "/api/system-status"),
    ("GET",  "/api/auth/me"),
    ("GET",  "/api/contacts"),
    ("GET",  "/api/notifications"),
    ("GET",  "/api/notifications/count"),
    ("GET",  "/api/reports/performance"),
    ("GET",  "/api/reports/financial"),
    ("GET",  "/api/reports/summary"),
    ("GET",  "/api/pipeline/metrics"),
    ("GET",  "/api/schedule"),
    ("GET",  "/api/deals/export"),
    ("POST", "/api/deals"),
    ("POST", "/api/bots/run"),
    ("POST", "/api/leads/generate"),
    ("POST", "/api/deals/auto-find"),
    ("POST", "/api/seed/case-studies"),
    ("POST", "/api/notifications"),
    ("POST", "/api/deals/import"),
    ("POST", "/api/calculate"),
    ("POST", "/api/calculate/sensitivity"),
    ("POST", "/api/calculate/stress-test"),
    ("POST", "/api/closed-deals"),
]


@pytest.mark.parametrize("method,path", PROTECTED_API_ROUTES)
def test_anonymous_api_returns_401(client, method, path):
    """Unauthenticated API requests must return 401 with JSON error body."""
    resp = getattr(client, method.lower())(
        path,
        content_type="application/json",
    )
    assert resp.status_code == 401, (
        f"{method} {path} expected 401, got {resp.status_code}"
    )
    data = resp.get_json()
    assert data is not None, f"{method} {path} expected JSON body"
    assert "error" in data, f"{method} {path} expected 'error' key in JSON"


# ---------------------------------------------------------------------------
# Public routes — must remain accessible without auth
# ---------------------------------------------------------------------------

def test_health_public(client):
    """/health must be accessible without authentication."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "healthy"


def test_login_page_public(client):
    """/login page must be accessible without authentication."""
    resp = client.get("/login")
    assert resp.status_code == 200


def test_register_page_public(client):
    """/register page must be accessible without authentication."""
    resp = client.get("/register")
    assert resp.status_code == 200


def test_api_auth_login_public(client):
    """/api/auth/login must be reachable (not 401) without auth."""
    # Will return 400 (bad input) — the point is it must NOT return 401
    resp = client.post(
        "/api/auth/login",
        json={"username": "", "password": ""},
        content_type="application/json",
    )
    assert resp.status_code != 401


def test_api_auth_register_public(client):
    """/api/auth/register must be reachable (not 401) without auth."""
    resp = client.post(
        "/api/auth/register",
        json={"username": "", "email": "", "password": ""},
        content_type="application/json",
    )
    assert resp.status_code != 401


def test_api_auth_logout_public(client):
    """/api/auth/logout must be reachable (not 401) without auth."""
    resp = client.post("/api/auth/logout")
    assert resp.status_code == 200


def test_logout_page_public(client):
    """/logout page must be accessible without authentication (no redirect loop)."""
    resp = client.get("/logout")
    # Should redirect to /login, not loop back through auth gate
    assert resp.status_code in (200, 301, 302)
    if resp.status_code in (301, 302):
        location = resp.headers.get("Location", "")
        assert "/login" in location


# ---------------------------------------------------------------------------
# Authenticated access — session-holding requests must succeed
# ---------------------------------------------------------------------------

def test_authenticated_session_accesses_dashboard(client):
    """A request with a valid session cookie must reach the dashboard (200)."""
    from web_server import app as flask_app

    with flask_app.test_client() as authed_client:
        with authed_client.session_transaction() as sess:
            sess["user"] = {
                "user_id": 1,
                "username": "testuser",
                "role": "admin",
            }
        resp = authed_client.get("/")
        assert resp.status_code == 200, (
            f"Authenticated user should reach dashboard, got {resp.status_code}"
        )


def test_authenticated_session_accesses_api(client):
    """A request with a valid session cookie must get data from a protected API (not 401)."""
    from web_server import app as flask_app

    with flask_app.test_client() as authed_client:
        with authed_client.session_transaction() as sess:
            sess["user"] = {
                "user_id": 1,
                "username": "testuser",
                "role": "admin",
            }
        resp = authed_client.get("/api/stats")
        # Should not be 401 (may still be 500 if DB is empty — that's fine)
        assert resp.status_code != 401, (
            f"Authenticated user should not receive 401 on /api/stats"
        )


def test_logout_clears_session_and_redirects(client):
    """GET /logout clears the session and redirects to /login."""
    from web_server import app as flask_app

    with flask_app.test_client() as authed_client:
        with authed_client.session_transaction() as sess:
            sess["user"] = {"user_id": 1, "username": "testuser", "role": "admin"}

        resp = authed_client.get("/logout")
        assert resp.status_code in (301, 302)
        location = resp.headers.get("Location", "")
        assert "/login" in location

        # Session should now be empty → subsequent request must redirect to login
        resp2 = authed_client.get("/")
        assert resp2.status_code in (301, 302)
        assert "/login" in resp2.headers.get("Location", "")
