"""Step 1 bootstrap: mint and store an offline token for every existing schedule.

For each scheduled Prefect deployment, read the owner's Keycloak user id from the stored
execution request and mint an offline token for that user via admin impersonation
(``offline_token_mint.mint_offline_token``), then store it as the schedule's offline token so
Standard Token Exchange (v2) scheduled runs work without the owner re-authorizing manually.

Idempotent: schedules that already have a stored offline token are skipped (unless ``--force``).
Does NOT use the deprecated token-exchange:v1 feature.

Usage (from the repo root, env loaded from dev.env or exported; PREFECT_API_URL must point at the
Prefect server):
    python scripts/bootstrap_offline_tokens.py [--dry-run] [--force]
"""
import argparse
import asyncio
import os
import sys

# Make `offline_token_mint` (this dir) and `process.base` (../processor) importable.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROCESSOR_DIR = os.path.join(os.path.dirname(_SCRIPT_DIR), "processor")
sys.path.insert(0, _SCRIPT_DIR)
sys.path.insert(0, _PROCESSOR_DIR)

from prefect.client.orchestration import get_client
from prefect.server.schemas import filters

from offline_token_mint import MintError, mint_offline_token, get_admin_token, jwt_payload_typ
# from process.base import store_offline_token, has_offline_token  # noqa: E402
from processor.process.base import store_offline_token, has_offline_token
# Must match pygeoapi_prefect.manager.DEPLOY_NAME_PREFIX.
DEPLOY_NAME_PREFIX = "pygeoapi_schedule_"


async def _list_schedule_deployments():
    async with get_client() as client:
        return await client.read_deployments(
            deployment_filter=filters.DeploymentFilter(
                name=filters.DeploymentFilterName(like_=DEPLOY_NAME_PREFIX)
            )
        )


def _owner_user_id(deployment) -> str | None:
    try:
        return deployment.parameters["execution_request"]["properties"]["user_id"]
    except (KeyError, TypeError):
        return None


async def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap schedule offline tokens via impersonation.")
    parser.add_argument("--dry-run", action="store_true", help="List actions without minting/storing.")
    parser.add_argument("--force", action="store_true", help="Re-mint even if a token already exists.")
    args = parser.parse_args()

    deployments = await _list_schedule_deployments()
    print(f"Found {len(deployments)} schedule deployment(s).")

    minted, skipped, failed = 0, 0, []
    admin_token = None if args.dry_run else get_admin_token()

    for deployment in deployments:
        schedule_id = deployment.name.replace(DEPLOY_NAME_PREFIX, "")
        user_id = _owner_user_id(deployment)

        if not user_id:
            print(f"  [skip] {schedule_id}: no stored user_id (cannot determine owner).")
            failed.append(schedule_id)
            continue
        if not args.force and has_offline_token(schedule_id):
            print(f"  [skip] {schedule_id}: offline token already stored.")
            skipped += 1
            continue
        if args.dry_run:
            print(f"  [dry-run] would mint + store offline token for {schedule_id} (user {user_id}).")
            continue

        try:
            token = mint_offline_token(user_id, admin_token=admin_token)
            if jwt_payload_typ(token) != "Offline":
                raise MintError("minted token is not of type 'Offline' (run the Step 0 spike first)")
            await store_offline_token(schedule_id, token)
            minted += 1
            print(f"  [ok]   {schedule_id}: stored offline token for user {user_id}.")
        except MintError as e:
            print(f"  [fail] {schedule_id} (user {user_id}): {e}")
            failed.append(schedule_id)

    print(f"\nDone: {minted} minted, {skipped} already present, {len(failed)} failed.")
    if failed:
        print("Failed schedules need the owner to re-authorize via "
              "POST /schedules/<id>/offline-token, or should be deleted:")
        for sid in failed:
            print(f"  - {sid}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
