import ast
import asyncio
import glob
import os
import secrets
import httpx
import logging

if not os.getenv("PYGEOAPI_CONFIG"):
    os.environ["PYGEOAPI_CONFIG"] = os.path.join(os.path.dirname(__file__), "default-config.yml")
if not os.getenv("PYGEOAPI_OPENAPI"):
    os.environ["PYGEOAPI_OPENAPI"] = os.path.join(os.path.dirname(__file__), "default-openapi.yml")

from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import Flask, send_from_directory, request

from prefect.client.orchestration import get_client
from prefect.server.schemas import filters
from werkzeug.utils import secure_filename

from flask_cors import CORS

from auth import *
from process.custom import km_processes
from process import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

KOMMONITOR_CORS_ORIGIN = os.getenv('KOMMONITOR_PROCESSES_API_ALLOWED_CORS_ORIGINS', "http://localhost:8000")
JOB_STORAGE_DURATION = os.getenv('JOB_STORAGE_DURATION', "P30D")
JOB_CLEAN_ENABLED = os.getenv('JOB_CLEAN_ENABLED', "False")
JOB_CLEAN_CRON = os.getenv('JOB_CLEAN_CRON', "0 0 * * *")
RESULTS_DIR = os.getenv('PROCESS_RESULTS_DIR', '/tmp')

from pygeoapi import flask_app
from pygeoapi.flask_app import STATIC_FOLDER, API_RULES, CONFIG, api_, processes_api, execute_from_flask

JOB_CLEAN_NAME = "pygeoapi_job_clean"

require_oauth = ResourceProtector()
require_oauth.register_token_validator(KomMonitorIntrospectTokenValidator())

APP = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
APP.url_map.strict_slashes = API_RULES.strict_slashes
APP.config['JSONIFY_PRETTYPRINT_REGULAR'] = CONFIG['server'].get('pretty_print', True)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    APP.logger.handlers = gunicorn_logger.handlers
    APP.logger.setLevel(gunicorn_logger.level)

CORS(APP)
cors = CORS(APP, resources={
    r"/*":{
        "origins":KOMMONITOR_CORS_ORIGIN
    }
})


@APP.get('/')
def landing_page():
    return flask_app.landing_page()


@APP.get('/processes', endpoint=API_GET_PROCESSES)
@APP.get('/processes/<process_id>', endpoint=API_GET_PROCESSES)
def get_processes(process_id=None):
    return flask_app.get_processes(process_id)

@APP.post('/processes', endpoint=API_CREATE_PROCESS)
@require_oauth()
def create_process():
    FILE = "source"
    HASH = secrets.token_hex(nbytes=8)
    UPLOAD_FOLDER = f"process/custom/"

    # check if the post request has the file part
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == "py"

    if FILE not in request.files:
        raise Exception("Error: file not found!")

    file = request.files[FILE]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        raise Exception("Error: filename not present!")
    if file and allowed_file(file.filename):

        filename = f"{secure_filename(file.filename)[:-3]}_{HASH}.py"
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        print("TODO: check if process already exists and possibly reject POST")
        parse_processes("custom")
    else:
        raise Exception("Error: file not allowed!")

    return ""


@APP.put('/processes', endpoint=API_UPDATE_PROCESS)
@require_oauth()
def update_process():
    # check if update or new creation

    # store as file
    # register as process
    # increment version number
    raise Exception("Not implemented yet!")


@APP.post('/processes/<process_id>/execution', endpoint=API_EXECUTE_PROCESS)
@require_oauth(optional=True)
def execute_process_jobs(process_id):
    return flask_app.execute_process_jobs(process_id)

@APP.post('/processes/<process_id>/schedule', endpoint=API_SCHEDULE_PROCESS)
@require_oauth()
def schedule_process(process_id):
    return flask_app.execute_from_flask(km_processes.schedule_process, request,
                              process_id)


@APP.get('/schedules', endpoint=API_GET_SCHEDULES)
@APP.route('/schedules/<schedule_id>',
           methods=['GET', 'DELETE'], endpoint=API_GET_SCHEDULES)
@require_oauth()
def get_schedules(schedule_id=None):
    if schedule_id is None:
        return flask_app.execute_from_flask(km_processes.get_schedules, request)
    else:
        if request.method == 'DELETE':
            return flask_app.execute_from_flask(km_processes.delete_schedule, request, schedule_id)
        else:
            return flask_app.execute_from_flask(km_processes.get_schedules, request, schedule_id)
        
@APP.post('/schedules/<schedule_id>/execution', endpoint=API_SCHEDULE_EXECUTION)
@require_oauth()
def schedule_execution(schedule_id):
    return flask_app.execute_from_flask(km_processes.execute_schedule, request,
                              schedule_id)


@APP.get('/jobs')
@APP.route('/jobs/<job_id>',
           methods=['GET', 'DELETE'],
           endpoint=API_GET_JOBS)
@require_oauth()
def get_jobs(job_id=None):
    return flask_app.get_jobs(job_id)


@APP.get('/jobs/<job_id>/results', endpoint=API_GET_JOB_RESULT)
@require_oauth()
def get_job_result(job_id=None):
    return flask_app.get_job_result(job_id)


@APP.get('/jobs/<job_id>/results/<resource>', endpoint=API_GET_JOB_RESULT_RESOURCE)
@require_oauth()
def get_job_result_resource(job_id, resource):
    return flask_app.get_job_result_resource(job_id, resource)


@APP.route('/results/<path:path>', endpoint=API_SEND_REPORT)
@require_oauth()
def send_report(path):
    return send_from_directory('results', path)


@APP.route('/exports/<job_id>', endpoint=API_DOWNLOAD_FILE)
@require_oauth(optional=True)
def download_file(job_id):
    return km_processes.execute_from_flask_custom(km_processes.download_file, request, job_id, RESULTS_DIR)


def parse_processes(package: str) -> None:
    """
    Dynamically parses processes and adds them to the global processing list
    """
    processes = flask_app.api_.manager.processes
    for process in glob.glob(f"process/{package}/*.py"):
        logger.debug(process)
        with open(process) as fh:
            root = ast.parse(fh.read())
            for node in ast.iter_child_nodes(root):
                if isinstance(node, ast.ClassDef):
                    process_path = os.path.normpath(fh.name)
                    processes[node.name] = {
                        "type": "process",
                        "processor": {
                            "name": f"process.{package}.{process_path.split(os.path.sep)[-1][:-3]}.{node.name}"
                        }
                    }
    flask_app.api_.manager.processes = processes
    api_.config['resources'] = processes


async def check_deployment_exists(deployment_name) -> bool:
    async with get_client() as client:
        deployments = await client.read_deployments(
            deployment_filter=filters.DeploymentFilter(
                name=filters.DeploymentFilterName(any_=[deployment_name])
            )
        )
        if deployments:
            return True
        else:
            return False


async def deploy_job_clean():
    source_name = os.path.dirname(os.path.abspath(utils.__file__))
    module_name = os.path.basename(utils.__file__)
    entrypoint = str.join(":", [module_name, "clean_job_storage_flow"])
    run_params = {
        "job_storage_duration": JOB_STORAGE_DURATION
    }

    try:
        deployment = await asyncio.wait_for(
            utils.clean_job_storage_flow.from_source(source=source_name, entrypoint=entrypoint,),timeout=10
        )
        deploy_id = await deployment.deploy(
            name=JOB_CLEAN_NAME,
            cron=JOB_CLEAN_CRON,
            work_pool_name="kommonitor-work-pool",
            parameters=run_params
        )
        logger.info(f'Successfully created deployment for job cleaning {deploy_id}')
    except httpx.ConnectError as err:
        logger.info(f"Could not connect to prefect server to create deployment for job cleaning: {str(err)}")


async def init_job_clean():
    # await utils.clean_job_storage_flow(JOB_STORAGE_DURATION)
    deployment_exists = await check_deployment_exists(JOB_CLEAN_NAME)
    if deployment_exists:
        logger.info("Deployment for job cleaning already exists.")
    else:
        await deploy_job_clean()


async def init():
    # Scan for available processes
    parse_processes("kommonitor")
    parse_processes("custom")
    parse_processes("export")

    if JOB_CLEAN_ENABLED:
        await init_job_clean()
    pass

asyncio.run(init())


def run():
    APP.run(debug=False,
            host=api_.config['server']['bind']['host'],
            port=api_.config['server']['bind']['port'])


if __name__ == "__main__":
    run()
