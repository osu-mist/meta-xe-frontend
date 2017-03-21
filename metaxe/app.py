# encoding: utf-8
from __future__ import print_function
import json
import os
#import urllib
#import urlparse
import requests

import flask
from flask_seasurf import SeaSurf

from . import api

app = flask.Flask('metaxe')

# Configuration defaults
app.config['SECRET_KEY'] = None
app.config['API_ENDPOINT'] = None
app.config['TOKEN_ENDPOINT'] = None

# make cookies more secure
# cookies with the secure flag are only sent over HTTPS
# cookies with the HttpOnly flag are not accessible with JavaScript
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['CSRF_COOKIE_SECURE'] = True
app.config['CSRF_COOKIE_HTTPONLY'] = True

# Load user config
if 'METAXE_CONFIG' in os.environ:
    app.config.from_envvar('METAXE_CONFIG')

csrf = SeaSurf(app)
#request = flask.request
#session = flask.session

@app.before_request
def check_config_vars():
    if not app.config.get('SECRET_KEY') or not app.config.get('API_ENDPOINT') or not app.config.get('TOKEN_ENDPOINT'):
        raise RuntimeError('The meta XE app is not configured properly. Please set SECRET_KEY, API_ENDPOINT, TOKEN_ENDPOINT.')

@app.route('/')
def index():
    client = api.Client(app)
    response = client.search()
    apps = response
    return flask.render_template('index.html', apps=apps)


def append_query(url, query):
    url = urlparse.urlsplit(url)
    if url.query:
        query = url.query + '&' + query
    return urlparse.urlunsplit([url.scheme, url.netloc, url.path, query, url.fragment])
