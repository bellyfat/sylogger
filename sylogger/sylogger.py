#!/usr/bin/env python
# Copyright 2017 Slipeer
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
'''
    Conversation logger application service for matrix-org/sydent
    Main module
'''

from flask import Flask
import logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)

from .transaction import Transaction
from .registrator import Registrator

import ConfigParser
import argparse


class Sylogger(object):
    ''' Main application class '''

    app = Flask(__name__)

    CONFIG_SECTIONS = ['tokens', 'listen', 'log']
    CONFIG_DEFAULTS = {
        'listen.port': '8008',
        'listen.ip': '127.0.0.1',
        'log.simple': 'conversations.log',
        'log.replace_newlines': 'False',
    }

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "configfile",
            nargs='?',
            default="sylogger.conf",
            help="the sylogger config file, defaults to sylogger.conf",
        )
        # Read the configuration file
        options = parser.parse_args()
        self.configfile = options.configfile
        self.parse_config()
        self.reg = Registrator(self.cfg)

    def run(self):
        ''' Flask application start '''
        transact_view = Transaction.as_view('transact_api', self.reg)
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

if __name__ == "__main__":
    SYL = Sylogger()
    SYL.run()
