import httpx
import pendulum
from prefect import flow, task, get_run_logger
from prefect.cache_policies import NO_CACHE
from prefect.exceptions import ObjectNotFound
from pygeoapi.util import JobStatus
from pygeoapi_prefect import manager


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




