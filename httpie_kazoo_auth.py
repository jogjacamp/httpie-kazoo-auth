"""
Kazoo Auth plugin for HTTPie

Original Code taken from https://github.com/ChillarAnand/httpie-django-auth
by Chillar Anand (c) 2017 MIT License
"""

import json
import hashlib
import os
import shlex
import requests
import subprocess

from httpie.plugins import AuthPlugin
from urllib.parse import urlsplit


def get_session_file(domain, session_name):
    domain = domain.replace(':', '_')
    file_path = '~/.httpie/sessions/{}/{}.json'.format(domain, session_name)
    return os.path.expanduser(file_path)


def clean_session(domain, session_name):
    # TODO: Check if last accessed is > 600 seconds, so that we need to get
    # a fresh auth token
    file_path = get_session_file(domain, session_name)
    try:
        os.remove(file_path)
    except OSError:
        pass


def run_shell_command(cmd):
    print(cmd)
    subprocess.check_output(shlex.split(cmd))


class KazooAuth(requests.auth.AuthBase):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session_name = 'httpie_kazoo_auth_%s' % username

    def __call__(self, r):
        result = urlsplit(r.url)
        scheme = result.scheme
        domain = result.netloc
        port = result.port or 8000

        login_url = '{}://{}:{}/api_auth'.format(scheme, domain, port)

        clean_session(domain, self.session_name)
        cmd = 'http GET {} --session={}'.format(login_url, self.session_name)
        run_shell_command(cmd)

        session = json.load(open(get_session_file(domain, self.session_name)))
        csrf_token = session['cookies']['csrftoken']['value']
        cmd = 'http -f POST {} username={} passowrd={} X-CSRFToken:{} --session={}'.format(
            login_url, self.username, self.password, csrf_token, self.session_name
        )
        run_shell_command(cmd)
        return r


class KazooAuthPlugin(AuthPlugin):

    name = 'kazoo auth'
    auth_type = 'kazoo'
    description = 'Kazoo token auth'

    def get_auth(self, username=None, password=None):
        return KazooAuth(username, password)
