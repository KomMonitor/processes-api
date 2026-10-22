import httpx
import pendulum
from prefect import flow, task, get_run_logger
from prefect.cache_policies import NO_CACHE
from prefect.client.orchestration import get_client
from prefect.exceptions import ObjectNotFound
from pygeoapi.util import JobStatus
from pygeoapi_prefect import manager

# `base` holds the Keycloak token helpers and the offline-token Secret-block convention.
# Import it the same resilient way the process modules do (package context when loaded as
# `process.utils`, flat import when Prefect loads this file standalone on the worker).
try:
    from . import base
except ImportError:
    from processor.process import base


@flow()
async def clean_job_storage_flow(job_storage_duration: str):
    logger = get_run_logger()
    duration = pendulum.parse(job_storage_duration)
    clean_time = pendulum.now().subtract(seconds=duration.total_seconds())
    logger.info(f"Start cleaning job results for jobs older than {clean_time}")
    flow_runs = await get_jobs()
    logger.info(f"Found {len(flow_runs)} existing flow runs.")
    deletion_counter = 0
    for flow_run in flow_runs:
        success = await check_and_delete_flow_run(flow_run, clean_time, logger)
        if success:
            deletion_counter += 1
    logger.info(f"Cleaned {deletion_counter} flow runs.")


@task(cache_policy=NO_CACHE)
def get_jobs():
    job_status_list = [JobStatus.successful, JobStatus.failed, JobStatus.dismissed]
    flow_runs = manager.get_flow_runs(job_status_list)
    return flow_runs


@flow()
async def refresh_offline_tokens_flow():
    """Refresh every stored schedule offline token so it never idles out.

    Each scheduled run already rotates its own offline token, so this flow is the safety net
    for schedules that run less often than the Keycloak offline-session idle timeout (or are
    paused). It redeems every stored offline token for a fresh one and persists the rotated
    token back. A token that can no longer be refreshed (revoked / idled out / user disabled)
    is reported so the schedule can be re-authorized.
    """
    logger = get_run_logger()
    prefix = base.OFFLINE_TOKEN_BLOCK_PREFIX
    async with get_client() as client:
        block_documents = await client.read_block_documents(include_secrets=True)
    offline_blocks = [
        d for d in block_documents
        if d.name and d.name.startswith(prefix) and d.block_type_name == "Secret"
    ]
    logger.info(f"Found {len(offline_blocks)} stored offline token(s) to refresh.")

    refreshed = 0
    failed = []
    for doc in offline_blocks:
        schedule_id = doc.name[len(prefix):]
        token = (doc.data or {}).get("value")
        if not token:
            logger.warning(f"Offline token block for schedule '{schedule_id}' has no value; skipping.")
            failed.append(schedule_id)
            continue
        try:
            token_resp = base.refresh_user_token(token)
            new_refresh = token_resp.get("refresh_token")
            if new_refresh and new_refresh != token:
                await base.store_offline_token(schedule_id, new_refresh)
            refreshed += 1
            logger.debug(f"Refreshed offline token for schedule '{schedule_id}'.")
        except Exception as e:
            logger.error(
                f"Could not refresh offline token for schedule '{schedule_id}' "
                f"(it may be revoked, idled out, or the user disabled) - the schedule needs "
                f"re-authorization: {e}"
            )
            failed.append(schedule_id)
    logger.info(f"Offline token refresh done: {refreshed} refreshed, {len(failed)} failed {failed}.")


@task(cache_policy=NO_CACHE)
async def check_and_delete_flow_run(flow_run, clean_time: pendulum.DateTime, logger):
    if flow_run.end_time < clean_time:
        logger.info(f"Flow run {flow_run.name} with end date {flow_run.end_time} selected for deletion.")
        outputs = flow_run.state
        success = True
        try:
            success = manager.delete_flow_outputs(outputs, logger)
        except Exception as ex:
            logger.error(f"Unexpected error while trying to delete job results for {flow_run.name} .{ex}")
        if success:
            try:
                await manager._delete_prefect_flow_run(flow_run.name)
                logger.info(f"Successfully deleted flow run {flow_run.name}")
                return True
            except ObjectNotFound as err:
                logger.error(f"Could not delete flow run {flow_run.name}. {err}")
                return False
            except httpx.ConnectError as err:
                logger.error(f"Could not connect to prefect server: {str(err)}")
                return False
        else:
            logger.warning(f"Could not delete result dir for flow run {flow_run.name}")
            return False
    else:
        logger.debug(f"Flow run {flow_run.name} with end date {flow_run.end_time} not selected for deletion.")
        return False




