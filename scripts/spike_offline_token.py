"""Step 0 feasibility spike: can we mint a genuine OFFLINE token via admin impersonation?

Run once against the target Keycloak before relying on the bootstrap. It mints an offline token
for a given user id and asserts the returned refresh token is of type "Offline" and can be
redeemed again.

Usage (from the repo root, env loaded from dev.env or exported):
    python scripts/spike_offline_token.py <keycloak_user_id>

Exit code 0 = offline token confirmed; non-zero = not feasible as configured (see message).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from offline_token_mint import (
    MintError, mint_offline_token, jwt_payload_typ,
    TOKEN_ENDPOINT, KC_OFFLINE_CLIENT_ID, KC_OFFLINE_CLIENT_SECRET,
)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    user_id = sys.argv[1]

    try:
        token = mint_offline_token(user_id)
    except MintError as e:
        print(f"FAIL: {e}")
        return 1

    typ = jwt_payload_typ(token)
    print(f"Minted refresh token for user {user_id}: typ={typ!r}")
    if typ != "Offline":
        print("FAIL: token is NOT an offline token (expected typ='Offline'). An online refresh "
              "token dies at the SSO session max lifespan and is unusable for schedules.")
        return 1

    # Prove the offline token can be redeemed for a fresh access token.
    data = {"grant_type": "refresh_token", "client_id": KC_OFFLINE_CLIENT_ID, "refresh_token": token}
    if KC_OFFLINE_CLIENT_SECRET:
        data["client_secret"] = KC_OFFLINE_CLIENT_SECRET
    resp = requests.post(TOKEN_ENDPOINT, data=data)
    if resp.status_code != 200:
        print(f"FAIL: offline token could not be refreshed: {resp.status_code} {resp.text}")
        return 1

    print("OK: offline token confirmed (typ='Offline' and refreshable). The bootstrap is feasible.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
