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
''' Log registrator glass implementation '''

import logging
from logging.handlers import RotatingFileHandler
import datetime
from urlparse import urlparse
import sys
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class Registrator(object):
    ''' Registrator class '''

    def __init__(self, cfg):
        self.cfg = cfg
        self.logfile = self.cfg.get('log', 'simple')
        try:
            if self.cfg.get('log', 'stdin') == 'True':
                self.writestdin = True
            else:
                self.writestdin = False
        except:
            self.writestdin = False
        self.replace_newlines = self.cfg.get('log', 'replace_newlines')
        logging.basicConfig(
            filename=self.logfile, level=logging.INFO, format="%(message)s"
        )
        self.logger = logging.getLogger("Simple")
        try:
            handler = RotatingFileHandler(
                self.cfg.get('log', 'simple'),
                maxBytes=self.cfg.get('log', 'maxBytes'),
                backupCount=self.cfg.get('log', 'backupCount')
            )
            self.logger.addHandler(handler)

        except:
            pass

    def register(self, event, info):
        '''
            Event registration
            event - matrix event structure
            info  - extracted event info to log
        '''
        dat = datetime.datetime.fromtimestamp(
            event['origin_server_ts']/1000
        ).strftime('%Y-%m-%d %H:%M:%S')
        if self.replace_newlines:
            info = info.replace('\r', '').replace('\n', '\\n')
        self.logger.info("%s %s %s %s %s" % (
            dat, event['type'], event['sender'], event['room_id'], info)
        )
        if self.writestdin:
            print "%s %s %s %s %s" % (
                dat, event['type'], event['sender'], event['room_id'], info
            )
            sys.stdout.flush()

    def convert_mxc(self, string):
        '''
            Convert URl from  mxc:// https://
            string - mxc:// URL string
        '''
        url = urlparse(string)
        #TODO https??
        return "https://%s/_matrix/media/v1/download/%s%s" % (
            url.netloc, url.netloc, url.path
        )
