# Migration bridge: bootstrap offline tokens via admin impersonation + keep them alive

## Context

The processes-api has been migrated to Keycloak **Standard Token Exchange (v2)**. Scheduled runs now
need a stored **offline token** per schedule (Prefect `Secret` block `km-offline-token-<schedule_id>`),
because v2 cannot mint a user token from service credentials. A re-authorization endpoint
(`POST /schedules/<id>/offline-token`) already lets users attach an offline token to an existing
schedule — but that requires every user to act manually.

The goal of this bridge is to **avoid manual re-authorization** for the schedules that already exist
in the running instance, by using the Keycloak **admin impersonation endpoint** to mint a genuine
offline token for each existing schedule non-interactively, and to add a cron that refreshes stored
offline tokens so they never idle out. `token-exchange:v1` is **not** used anywhere in this bridge —
the admin impersonation endpoint is a standard, supported endpoint independent of that feature.

## Feasibility verdict

- **Bootstrap via admin impersonation + authorization-code flow — feasible, recommended.**
  `POST /admin/realms/{realm}/users/{id}/impersonation` (caller needs the `impersonation`
  realm-management role) creates a **real user session** for the target user and returns **session
  cookies** (`KEYCLOAK_IDENTITY`, `KEYCLOAK_SESSION`, `AUTH_SESSION_ID`) — not tokens. Carrying those
  cookies through a normal auth-code flow with `scope=openid offline_access` yields a genuine **offline
  token** (`"typ":"Offline"`), backed by a real offline session. Unlike token exchange, this creates the
  session an offline token needs, and it does not depend on the deprecated `token-exchange:v1` feature.
- **Refresh cron: feasible and valuable** — keeps stored offline tokens from idling out.
- Rejected alternatives: v1 impersonation token exchange with `scope=offline_access` (whether it returns
  a true offline token is undocumented/unconfirmed — [keycloak#43921] unanswered, [keycloak#45275]
  concluded a custom SPI was needed); a custom Keycloak SPI (robust but heavyweight plugin development).

### Feasibility check (verified against `docker/realms/realm-export.json`)

- ✅ **Offline tokens can live indefinitely:** `offlineSessionMaxLifespanEnabled: false`,
  `offlineSessionIdleTimeout: 2592000` (30 days). A daily refresh cron keeps them perpetual — the key
  settings check passes.
- ✅ **Offline tokens are genuinely required:** `ssoSessionMaxLifespan: 36000` (10 h) means an online
  refresh token would die in 10 h; only an offline token survives for schedules.
- ✅ **`kommonitor-web-client` supports the scripted flow:** `consentRequired: false`, `offline_access`
  available as an optional scope, redirect URIs registered, and **no forced PKCE** (the `S256` entries
  belong to `account-console`/`security-admin-console`, not the web client) → the auth-code call returns
  a code with no login/consent page.
- ✅ **All codebase reuse points exist** (schedule enumeration, `base.py` token helpers, `deploy_job_clean`
  pattern, Prefect `read_block_documents`).
- ⚠️ **The `impersonation` role must be granted to the bootstrap service account.** The role exists in the
  realm (as part of the `realm-admin` composite) but is not currently assigned to a KomMonitor service
  account (only the old v1 token-exchange impersonation *policy* exists). Grant the realm-management
  `impersonation` client role to `KC_ADMIN_CLIENT_ID`'s service account.
- ⚠️ **Production realms differ:** these checks are against the local docker realm (`kommonitor`). The
  running instance uses `kommonitor-demo` / `kommonitor-demo-dev`, which are managed separately — verify
  the same offline-session settings, web-client config, and impersonation grant there before bootstrapping.
- ❓ **Spike-gated unknown:** whether the admin impersonation **REST** endpoint (called with a
  service-account bearer) returns `Set-Cookie` session cookies the `/auth` endpoint accepts is
  version-sensitive ([keycloak#9907], [keycloak#10655] show quirks by version/hostname). This is the one
  thing static analysis can't settle — Step 0 must confirm it on Keycloak 26.5.7. Everything else checks out.

## Step 0 — Spike (decisive, do first)

Standalone script (scratchpad or `scripts/`, run inside the container/venv). Validate the impersonation →
offline-token flow for one test user that owns a schedule, using an HTTP client with a **cookie jar** and
**redirects disabled** so the authorization code can be captured:

1. Get a service-account admin token (a client holding the `impersonation` role).
2. `POST {KC_URL}/admin/realms/{KC_REALM_NAME}/users/{user_id}/impersonation` with that token →
   capture the `Set-Cookie` session cookies.
3. `GET {KC_URL}/realms/{KC_REALM_NAME}/protocol/openid-connect/auth?client_id={KC_OFFLINE_CLIENT_ID}`
   `&redirect_uri={registered_uri}&response_type=code&scope=openid%20offline_access&state=x`
   **with the cookies** → expect a `302` to `redirect_uri?code=…` with no login/consent page. Extract `code`.
4. `POST …/token` with `grant_type=authorization_code`, `code`, `redirect_uri`, `client_id`
   (+ secret if confidential) → decode the returned `refresh_token` header and assert **`typ == "Offline"`**.
5. Confirm `refresh_user_token(offline_token)` succeeds (token is bound to `KC_OFFLINE_CLIENT_ID`).

Confirm along the way: the impersonation call and the `/auth` call hit the **same Keycloak host** (cookie
domain); the client has `consentRequired=false` (true for `kommonitor-web-client`); and the target user
has the `offline_access` role (default). If an assertion fails, adjust config (registered `redirect_uri`,
host, roles) — the mechanism itself is sound.

## Step 1 — Bootstrap script

One-off, idempotent admin script (`scripts/bootstrap_offline_tokens.py`). Can run at any time (does not
require `token-exchange:v1`):

- Enumerate all schedule deployments: `anyio.run(_get_prefect_deployments, PrefectManager._deploy_name_prefix)`
  (`manager.py:1003`), then per deployment `schedule_id = deployment.name.replace(DEPLOY_NAME_PREFIX, "")`
  and `user_id = deployment.parameters['execution_request']['properties']['user_id']` (the pattern from
  [`km_processes.py:222`](processor/process/custom/km_processes.py:222)).
- Skip schedules that already have a token: `has_offline_token(schedule_id)` ([`base.py`](processor/process/base.py)).
- For each remaining schedule, run the Step-0 impersonation → auth-code → token flow to obtain the user's
  offline token, then `store_offline_token(schedule_id, offline_token)` (reuse the
  [`base.py`](processor/process/base.py) helper).
- Log a summary (minted / skipped / failed). Failures (disabled/deleted users, missing `offline_access`)
  are expected for stale schedules — report them so ops can delete those schedules or ask the owner to
  re-authorize via the existing endpoint.

**Client binding:** the offline token is issued to `KC_OFFLINE_CLIENT_ID` in the auth-code flow, exactly
the client `refresh_user_token()` refreshes with — so bindings match by construction. Requirements: a
service account with the `impersonation` role (add `KC_ADMIN_CLIENT_ID` / `KC_ADMIN_CLIENT_SECRET`, or
reuse an existing admin client) and a registered `redirect_uri` on `KC_OFFLINE_CLIENT_ID`.

## Step 2 — Retire v1 leftovers (cleanup)

The bridge does not use `token-exchange:v1`, so once the bootstrap has populated tokens:
- Confirm `token-exchange:v1` is absent from the Keycloak features (already dropped in
  [`docker-compose.dev.yml`](docker/docker-compose.dev.yml)) and `standard.token.exchange.enabled=true`
  on the processor client (already set in [`realm-export.json`](docker/realms/realm-export.json)).
- Retire the old v1 token-exchange impersonation policies (`kommonitor-processor-impersonator`,
  `admin-impersonating.permission.users`) in the realm. Keep the `impersonation` realm-management role
  that the bootstrap service account uses (that is a different, still-needed permission).
- No processes-api runtime code change — the v2 scheduled path already consumes the stored offline tokens.

## Step 3 — Cron to refresh offline tokens (mirror `deploy_job_clean`)

Offline tokens die only if they idle out (`offlineSessionIdleTimeout`, default 30 days). Frequent
schedules already rotate their own token every run; this cron is the safety net for infrequent/paused
schedules. Mirror the existing job-clean pattern exactly:

- New flow in [`processor/process/utils.py`](processor/process/utils.py): `@flow() async def refresh_offline_tokens_flow()`:
  - List Secret blocks and filter by prefix (Prefect 3.6.15 has no name filter):
    ```python
    async with get_client() as client:
        docs = await client.read_block_documents(include_secrets=True)
    blocks = [d for d in docs if d.name and d.name.startswith(OFFLINE_TOKEN_BLOCK_PREFIX)
              and d.block_type_name == "Secret"]
    ```
  - For each: `schedule_id = name[len(OFFLINE_TOKEN_BLOCK_PREFIX):]`, load the token, `refresh_user_token(token)`,
    and `store_offline_token(schedule_id, new_refresh)` when rotated — reusing the helpers in
    [`base.py`](processor/process/base.py) (same logic as [`_get_dm_token_for_schedule`](processor/process/base.py)).
    Wrap each in try/except and log per-token success/failure (a failed refresh = a dead offline token →
    that schedule needs re-authorization or re-bootstrapping).
- New `deploy_offline_token_refresh()` + `init_offline_token_refresh()` in
  [`processor/app.py`](processor/app.py:221), mirroring `deploy_job_clean()` / `init_job_clean()`
  (`from_source(...).deploy(name=..., cron=..., work_pool_name="kommonitor-work-pool", parameters=...)`,
  guarded by `check_deployment_exists`), called from `init()` (`app.py:255`).
- New env vars in `dev.env` / `docker/dev.env`: `OFFLINE_TOKEN_REFRESH_ENABLED` (default True),
  `OFFLINE_TOKEN_REFRESH_CRON` (default e.g. `0 3 * * *`), and a deployment-name constant
  `OFFLINE_TOKEN_REFRESH_NAME = "pygeoapi_offline_token_refresh"`. The cron interval **must** be shorter
  than `offlineSessionIdleTimeout`.

## Schedules that can't be bootstrapped

For any schedule whose offline token could not be minted (disabled/deleted user, missing `offline_access`
role), the owner re-authorizes via the existing `POST /schedules/<id>/offline-token` endpoint. The
`offlineTokenRegistered` flag on `GET /schedules` lets the frontend list which schedules still need it.
No `token-exchange:v1` fallback is used.

## Files to modify

- **New:** `scripts/bootstrap_offline_tokens.py` (Step 1: impersonation → auth-code → offline token) and a
  throwaway Step-0 spike script.
- [`processor/process/utils.py`](processor/process/utils.py) — `refresh_offline_tokens_flow` (Step 3).
- [`processor/app.py`](processor/app.py:221) — `deploy_offline_token_refresh` / `init_offline_token_refresh`
  + env constants (Step 3).
- [`processor/process/base.py`](processor/process/base.py) — reuse `refresh_user_token`, `store_offline_token`,
  `_load_offline_token`, `has_offline_token`, `OFFLINE_TOKEN_BLOCK_PREFIX` (no changes required beyond reuse).
- `dev.env`, `docker/dev.env` — new refresh-cron env vars and admin service-account vars
  (`KC_ADMIN_CLIENT_ID` / `KC_ADMIN_CLIENT_SECRET`).
- [`README.md`](README.md) — document the bootstrap procedure and the refresh cron.

## Prerequisites / risks to verify

- **Impersonation prerequisites:** a service account with the `impersonation` realm-management role;
  target users with the `offline_access` role (default); a registered `redirect_uri` on
  `KC_OFFLINE_CLIENT_ID` with `consentRequired=false`; the impersonation + auth-code calls made against
  the **same Keycloak host** (cookie domain).
- **Realm offline-session settings:** confirm `offlineSessionMaxLifespanEnabled` is **false** (default) —
  if a max lifespan is enforced, no refresh cron can keep tokens alive past it and offline tokens will
  eventually require re-authorization. Set the refresh-cron interval below `offlineSessionIdleTimeout`.
- **Rotation races** between the refresh cron and a concurrent scheduled run are benign (each loads the
  latest token and rotates immediately), but schedule the cron at a quiet hour to minimize churn.

## Verification

1. **Spike:** run Step 0; confirm the impersonation call returns session cookies, the `/auth` call returns
   a code with no login/consent page, and the token endpoint returns a `refresh_token` with `typ==Offline`
   that `refresh_user_token()` can redeem.
2. **Bootstrap:** on a copy of the schedules, run `bootstrap_offline_tokens.py`; confirm a
   `km-offline-token-<schedule_id>` Secret block appears for every live schedule and `GET /schedules`
   reports `offlineTokenRegistered: true`; stale/failed users are listed.
3. **v2 scheduled run:** trigger a bootstrapped schedule (`POST /schedules/<id>/execution`); confirm it
   refreshes + exchanges + writes results, and the rotated token is persisted.
4. **Refresh cron:** run `refresh_offline_tokens_flow` manually; confirm every block is refreshed and
   rotated tokens are stored; simulate a dead token and confirm it is logged as needing re-authorization.
   Confirm the deployment is created once (idempotent via `check_deployment_exists`).