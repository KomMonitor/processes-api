import asyncio
import collections
import os
import requests
from authlib.oauth2.rfc7662 import IntrospectTokenValidator
from flask import session, Blueprint, Flask, request, g, send_from_directory
from pygeoapi import flask_app
from pygeoapi.flask_app import STATIC_FOLDER, API_RULES, CONFIG, api_

from authlib.integrations.flask_oauth2 import ResourceProtector

KC_CLIENT_ID = os.getenv('KC_CLIENT_ID')
KC_CLIENT_SECRET = os.getenv('KC_CLIENT_SECRET')


class MyIntrospectTokenValidator(IntrospectTokenValidator):
    def introspect_token(self, token_string):
        url = 'http://keycloak:8080/realms/kommonitor/protocol/openid-connect/token/introspect'
        data = {'token': token_string, 'token_type_hint': 'access_token'}
        auth = (KC_CLIENT_ID, KC_CLIENT_SECRET)
        resp = requests.post(url, data=data, auth=auth)
        resp.raise_for_status()
        token = resp.json()

        # Store username and roles in context
        if token["active"]:
            g.user = token["username"]
            g.roles = token["realm_access"]["roles"]
        return token


require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyIntrospectTokenValidator())

APP = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='/static')
APP.url_map.strict_slashes = API_RULES.strict_slashes
APP.config['JSONIFY_PRETTYPRINT_REGULAR'] = CONFIG['server'].get('pretty_print', True)


@APP.route('/')
def landing_page():
    return flask_app.landing_page()


@APP.route('/processes')
@APP.route('/processes/<process_id>')
@require_oauth()
def get_processes(process_id=None):
    return flask_app.get_processes(process_id)


@APP.post('/processes')
@require_oauth()
def create_processes():
    raise Exception("Not impelemented yet!")


@APP.route('/processes/<process_id>/execution', methods=['POST'])
@require_oauth()
def execute_process_jobs(process_id):
    return flask_app.execute_process_jobs(process_id)


@APP.route('/jobs')
@APP.route('/jobs/<job_id>',
           methods=['GET', 'DELETE'])
@require_oauth()
def get_jobs(job_id=None):
    return flask_app.get_jobs(job_id)


@APP.route('/jobs/<job_id>/results',
           methods=['GET'])
@require_oauth()
def get_job_result(job_id=None):
    return flask_app.get_job_result(job_id)


@APP.route('/jobs/<job_id>/results/<resource>',
           methods=['GET'])
@require_oauth()
def get_job_result_resource(job_id, resource):
    return flask_app.get_job_result_resource(job_id, resource)


@APP.route('/results/<path:path>')
def send_report(path):
    return send_from_directory('results', path)


async def init():
    # deployment = await Deployment.build_from_flow(
    #    flow=aggregate_sum_flow,
    #    name="example",
    #    version="1",
    #    tags=["demo"],
    # )
    #
    # deployment.schedule = CronSchedule(
    #    cron="*/5 * * * *"
    # )
    # await deployment.apply()

    processes = collections.OrderedDict()
    processes["aggregate_sum"] = {
        "type": "process",
        "processor": {
            "name": "process.aggregate_sum.AggregateSumFlowProcessor"
        }
    }

    flask_app.api_.manager.processes = processes


def run(a, b):
    asyncio.run(init())

    APP.run(debug=False,
            host=api_.config['server']['bind']['host'],
            port=api_.config['server']['bind']['port'])


if __name__ == "__main__":
    run(None, None)
