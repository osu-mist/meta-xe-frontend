# encoding: utf-8
from __future__ import print_function
import os
import flask

app = flask.Flask('metaxe')
request = flask.request

from . import api

# Configuration defaults
app.config['SECRET_KEY'] = None
app.config['API_ENDPOINT'] = None
app.config['TOKEN_ENDPOINT'] = None
app.config['INSTANCES'] = ['prod', 'devl', 'dev2']

# Load user config
if 'METAXE_CONFIG' in os.environ:
    app.config.from_envvar('METAXE_CONFIG')

@app.before_request
def check_config_vars():
    if not app.config.get('SECRET_KEY') or not app.config.get('API_ENDPOINT') or not app.config.get('TOKEN_ENDPOINT'):
        raise RuntimeError('The meta XE app is not configured properly. Please set SECRET_KEY, API_ENDPOINT, and TOKEN_ENDPOINT.')

@app.route('/')
def index():
    client = api.Client(app)

    q = request.args.get('q', '')
    instance = request.args.get('instance', '')
    if instance not in app.config['INSTANCES']:
        instance = ''
    try:
        page = int(request.args['page'])
    except (ValueError, KeyError):
        page = 1

    response = client.search(q, instance=instance, page=page)

    args = {}
    if q:
        args['q'] = q
    if instance:
        args['instance'] = instance

    prev_page = None
    next_page = None
    if response.get('links', {}).get('next'):
        next_page = flask.url_for('index', page=page+1, **args)
    if response.get('links', {}).get('prev'):
        prev_page = flask.url_for('index', page=page-1, **args)

    return flask.render_template('index.html',
        apps=response['data'],
        next_page=next_page,
        prev_page=prev_page,
        instance=instance,
    )
