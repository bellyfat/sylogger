#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017-2019 Pavel Kardash
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import flask
import logging
logging.getLogger('werkzeug').setLevel(logging.INFO)

from .transaction import Transaction

import ConfigParser

def create_app(config_filename = "/opt/synapse/sylogger.conf"):
    app = flask.Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    Syl = Sylogger(config_filename)
    transact_view = Transaction.as_view('transact_api', Syl)
    app.add_url_rule(
        "/transactions/<transaction>",
        view_func=transact_view, methods=["PUT"]
    )
    return app


class Sylogger(object):
    ''' Main application class '''

    CONFIG_SECTIONS = ['tokens', 'listen']
    CONFIG_DEFAULTS = {
        'listen.port': '5001',
        'listen.ip': '127.0.0.1',
    }

    def __init__(self, configfile):
        # Read the configuration file
        self.configfile = configfile
        self.parse_config()

    def run(self):
        ''' Flask application start '''
        transact_view = Transaction.as_view('transact_api', self)
        self.app.add_url_rule(
            "/transactions/<transaction>",
            view_func=transact_view, methods=["PUT"]
        )
        self.app.run(
            host=self.cfg.get('listen', 'ip'),
            port=self.cfg.get('listen', 'port')
        )

    def parse_config(self):
        ''' Configuration parse '''
        self.cfg = ConfigParser.SafeConfigParser(self.CONFIG_DEFAULTS)
        for sect in self.CONFIG_SECTIONS:
            try:
                self.cfg.add_section(sect)
            except ConfigParser.DuplicateSectionError:
                pass
        self.cfg.read(self.configfile)
