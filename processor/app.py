import ast
import asyncio
import glob
import os
import secrets

from authlib.integrations.flask_oauth2 import ResourceProtector
from flask import Flask, send_from_directory, request
from werkzeug.utils import secure_filename

from auth import MyIntrospectTokenValidator

if not os.getenv("PYGEOAPI_CONFIG"):
    os.environ["PYGEOAPI_CONFIG"] = os.path.join(os.path.dirname(__file__), "default-config.yml")
if not os.getenv("PYGEOAPI_OPENAPI"):
    os.environ["PYGEOAPI_OPENAPI"] = os.path.join(os.path.dirname(__file__), "default-openapi.yml")

from pygeoapi import flask_app
from pygeoapi.flask_app import STATIC_FOLDER, API_RULES, CONFIG, api_, processes_api, execute_from_flask

require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyIntrospectTokenValidator())

APP = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
APP.url_map.strict_slashes = API_RULES.strict_slashes
APP.config['JSONIFY_PRETTYPRINT_REGULAR'] = CONFIG['server'].get('pretty_print', True)


@APP.get('/')
def landing_page():
    return flask_app.landing_page()


@APP.get('/processes')
@APP.get('/processes/<process_id>')
@require_oauth()
def get_processes(process_id=None):
    return flask_app.get_processes(process_id)

@APP.post('/processes')
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


@APP.put('/processes')
@require_oauth()
def update_process():
    # check if update or new creation

    # store as file
    # register as process
    # increment version number
    raise Exception("Not implemented yet!")


@APP.post('/processes/<process_id>/execution')
@require_oauth()
def execute_process_jobs(process_id):
    return flask_app.execute_process_jobs(process_id)


@APP.get('/jobs')
@APP.route('/jobs/<job_id>',
           methods=['GET', 'DELETE'])
@require_oauth()
def get_jobs(job_id=None):
    return flask_app.get_jobs(job_id)


@APP.get('/jobs/<job_id>/results')
@require_oauth()
def get_job_result(job_id=None):
    return flask_app.get_job_result(job_id)


@APP.get('/jobs/<job_id>/results/<resource>')
@require_oauth()
def get_job_result_resource(job_id, resource):
    return flask_app.get_job_result_resource(job_id, resource)


@APP.route('/results/<path:path>')
@require_oauth()
def send_report(path):
    return send_from_directory('results', path)


def parse_processes(package: str) -> None:
    """
    Dynamically parses processes and adds them to the global processing list
    """
    processes = flask_app.api_.manager.processes
    for process in glob.glob(f"process/{package}/*.py"):
        print(process)
        with open(process) as fh:
            root = ast.parse(fh.read())
            for node in ast.iter_child_nodes(root):
                if isinstance(node, ast.ClassDef) and node.bases[0].id == "KommonitorProcess":
                    process_path = os.path.normpath(fh.name)
                    processes[node.name] = {
                        "type": "process",
                        "processor": {
                            "name": f"process.{package}.{process_path.split(os.path.sep)[-1][:-3]}.{node.name}"
                        }
                    }
    flask_app.api_.manager.processes = processes
    api_.config['resources'] = processes


async def init():
    # Scan for available processes
    parse_processes("kommonitor")
    parse_processes("custom")

    # deployment = await Deployment.build_from_flow(
    #  flow=aggregate_sum_flow,
    #  name="example",
    #  version="1",
    #  tags=["demo"],
    # )

    # deployment.schedule = CronSchedule(
    #  cron="*/5 * * * *"
    # )
    # await deployment.apply()
    pass

asyncio.run(init())

def run():

    APP.run(debug=False,
            host=api_.config['server']['bind']['host'],
            port=api_.config['server']['bind']['port'])


if __name__ == "__main__":
    run()
