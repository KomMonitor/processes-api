"""Mint a user offline token non-interactively via Keycloak admin impersonation.

Shared by ``spike_offline_token.py`` (feasibility check) and ``bootstrap_offline_tokens.py``
(one-off migration). Pure ``requests`` - no app dependencies - so it can be run standalone.

Mechanism (does NOT use the deprecated token-exchange:v1 feature):
  1. A service account with the realm-management ``impersonation`` role obtains an admin token.
  2. ``POST /admin/realms/{realm}/users/{id}/impersonation`` creates a real user session for the
     target user and returns session cookies.
  3. Carrying those cookies, an authorization-code request with ``scope=offline_access`` returns a
     code (no login/consent page for a first-party client with consentRequired=false).
  4. Exchanging the code yields a genuine offline refresh token (JWT header ``"typ":"Offline"``).

Required environment variables (see dev.env):
  KC_URL, KC_REALM_NAME, KC_ADMIN_CLIENT_ID, KC_ADMIN_CLIENT_SECRET,
  KC_OFFLINE_CLIENT_ID, KC_OFFLINE_CLIENT_SECRET (optional, empty for a public client),
  KC_OFFLINE_REDIRECT_URI (a redirect URI registered on KC_OFFLINE_CLIENT_ID).
"""
import base64
import json
import os
import urllib.parse
import uuid

import requests

KC_URL = os.getenv("KC_URL", "https://keycloak:8443").rstrip("/")
KC_REALM_NAME = os.getenv("KC_REALM_NAME", "kommonitor-demo")
KC_ADMIN_CLIENT_ID = os.getenv("KC_ADMIN_CLIENT_ID", "kommonitor-processes-api")
KC_ADMIN_CLIENT_SECRET = os.getenv("KC_ADMIN_CLIENT_SECRET", "")
KC_OFFLINE_CLIENT_ID = os.getenv("KC_OFFLINE_CLIENT_ID", "kommonitor-web-client")
KC_OFFLINE_CLIENT_SECRET = os.getenv("KC_OFFLINE_CLIENT_SECRET", "")
KC_OFFLINE_REDIRECT_URI = os.getenv("KC_OFFLINE_REDIRECT_URI", "http://localhost:8084/")

TOKEN_ENDPOINT = f"{KC_URL}/realms/{KC_REALM_NAME}/protocol/openid-connect/token"
AUTH_ENDPOINT = f"{KC_URL}/realms/{KC_REALM_NAME}/protocol/openid-connect/auth"
IMPERSONATION_ENDPOINT = f"{KC_URL}/admin/realms/{KC_REALM_NAME}/users/{{user_id}}/impersonation"


class MintError(RuntimeError):
    """Raised when an offline token could not be minted for a user."""


def jwt_header_typ(token: str) -> str | None:
    """Return the ``typ`` field of a JWT header without verifying the signature."""
    try:
        header_b64 = token.split(".")[0]
        header_b64 += "=" * (-len(header_b64) % 4)  # pad to a multiple of 4
        header = json.loads(base64.urlsafe_b64decode(header_b64))
        return header.get("typ")
    except Exception:
        return None


def get_admin_token() -> str:
    """Client-credentials token for the impersonating service account."""
    resp = requests.post(TOKEN_ENDPOINT, data={
        "grant_type": "client_credentials",
        "client_id": KC_ADMIN_CLIENT_ID,
        "client_secret": KC_ADMIN_CLIENT_SECRET,
    })
    if resp.status_code != 200:
        raise MintError(f"Could not obtain admin token for '{KC_ADMIN_CLIENT_ID}': "
                        f"{resp.status_code} {resp.text}")
    return resp.json()["access_token"]


def mint_offline_token(user_id: str, admin_token: str | None = None) -> str:
    """Mint an offline refresh token for ``user_id`` via impersonation + auth-code flow."""
    admin_token = admin_token or get_admin_token()
    session = requests.Session()

    # 1. Impersonate the user -> session cookies land in the session cookie jar.
    imp = session.post(
        IMPERSONATION_ENDPOINT.format(user_id=user_id),
        headers={"Authorization": f"Bearer {admin_token}"},
        allow_redirects=False,
    )
    if imp.status_code not in (200, 201, 204, 302):
        raise MintError(f"Impersonation failed for user '{user_id}': {imp.status_code} {imp.text}")
    if not session.cookies:
        raise MintError(
            f"Impersonation returned no session cookies for user '{user_id}'. The admin "
            f"impersonation REST behavior is version-sensitive - ensure the impersonation and "
            f"auth calls hit the same Keycloak host, and that the service account holds the "
            f"'impersonation' role."
        )

    # 2. Authorization-code request as the (now impersonated) user, asking for offline_access.
    auth = session.get(AUTH_ENDPOINT, params={
        "client_id": KC_OFFLINE_CLIENT_ID,
        "redirect_uri": KC_OFFLINE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid offline_access",
        "state": uuid.uuid4().hex,
    }, allow_redirects=False)
    location = auth.headers.get("Location", "")
    query = urllib.parse.parse_qs(urllib.parse.urlparse(location).query)
    if auth.status_code not in (302, 303) or "code" not in query:
        raise MintError(
            f"Authorization request for user '{user_id}' did not return a code (status "
            f"{auth.status_code}). The impersonated session was likely not recognized, or a "
            f"login/consent page was shown. Verify KC_OFFLINE_REDIRECT_URI is registered on "
            f"'{KC_OFFLINE_CLIENT_ID}', the client has consentRequired=false, and the user has "
            f"the 'offline_access' role."
        )
    code = query["code"][0]

    # 3. Exchange the code for tokens; the refresh_token is the offline token.
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": KC_OFFLINE_REDIRECT_URI,
        "client_id": KC_OFFLINE_CLIENT_ID,
    }
    if KC_OFFLINE_CLIENT_SECRET:
        data["client_secret"] = KC_OFFLINE_CLIENT_SECRET
    tok = requests.post(TOKEN_ENDPOINT, data=data)
    if tok.status_code != 200:
        raise MintError(f"Code exchange failed for user '{user_id}': {tok.status_code} {tok.text}")
    refresh_token = tok.json().get("refresh_token")
    if not refresh_token:
        raise MintError(f"No refresh_token returned for user '{user_id}'.")
    return refresh_token
