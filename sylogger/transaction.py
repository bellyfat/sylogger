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
''' Transaction handling module '''

from flask.views import MethodView
from flask import jsonify, request
import logging
import logging.handlers
import json
import datetime

class Transaction(MethodView):
    ''' Class for implement /transaction API part '''

    def __init__(self, reg):
        self.logger = logging.getLogger('matrix_sylogger')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler(address = '/dev/log')
        self.logger.addHandler(handler)

    def put(self, transaction):
        '''
            Receive transaction  with PUT method
            transaction - contain transaction id number
        '''
        events = request.get_json()["events"]
        for event in events:
            etype = event['type'].replace('.', '_')
            if hasattr(self, etype):
                method = getattr(self, etype)
                try:
                    method(event)
                except:
                    info = "%r" % event
                    self.register(event, info)
            else:
                # !!! Encoding !!!
                info = json.dumps(event,  ensure_ascii=False)
                self.register(event, info)
        return jsonify({})

    def register(self, event, info):
        '''
            Event registration
            event - matrix event structure
            info  - extracted event info to log
        '''
        dat = datetime.datetime.fromtimestamp(
            event['origin_server_ts']/1000
        ).strftime('%Y-%m-%d %H:%M:%S')
        info = info.replace('\r', '').replace('\n', '\\n')
        self.logger.info("%s %s %s %s %s" % (
            dat, event['type'], event['sender'], event['room_id'], info)
        )


    def m_text(self, event):
        ''' For text message dump body '''
        return event['content']['body']

    def m_image(self, event):
        ''' For image message dump attributes '''
        res = "filename: %s type: %s size: %d url: %s" % (
            event['content']['body'],
            event['content']['info']['mimetype'],
            event['content']['info']['size'],
            event['content']['url']
        )
        return res

    def m_file(self, event):
        ''' For file message dump attributes '''
        try:
            mime = event['content']['info'].has['mimetype']
        except:
            mime = "n/a"
        res = "filename: %s type: %s size: %d url: %s" % (
            event['content']['body'],
            mime,
            event['content']['info']['size'],
            event['content']['url']
        )
        return res

    def m_room_message(self, event):
        ''' Process m.room.message event '''
        mtype = event['content']['msgtype'].replace('.', '_')
        if hasattr(self, mtype):
            method = getattr(self, mtype)
            info = "%s %s" % (event['content']['msgtype'], method(event))
        else:
            info = "%s %s %r" % (
                event['content']['msgtype'],
                event['content']['body'],
                event['content']
            )
        self.register(event, info)

    def m_room_create(self, event):
        ''' Process m.room.create event '''
        info = "created"
        self.register(event, info)

    def m_room_name(self, event):
        ''' Process m.room.name event '''
        info = "set_name: %s" % event['content']['name']
        self.register(event, info)

    def m_room_topic(self, event):
        ''' Process m.room.topic event '''
        info = "set_topic: %s" % event['content']['topic']
        self.register(event, info)

    def m_room_aliases(self, event):
        ''' Process m.room.aliases event '''
        info = "set_aliases: %r" % event['content']['aliases']
        self.register(event, info)

    def m_room_member(self, event):
        ''' Process m.room.member event '''
        info = "%s %s" % (event['membership'], event['state_key'])
        self.register(event, info)

    def m_room_power_levels(self, event):
        ''' Process m.room.power_levels event '''
        info = "power_levels: %s" % event['content']
        self.register(event, info)

    def m_room_join_rules(self, event):
        ''' Process m.room.join_rules event '''
        info = "join_rules: %s" % event['content']['join_rule']
        self.register(event, info)

    def m_room_history_visibility(self, event):
        ''' Process m.room.history_visibility event '''
        info = "history_visib: %s" % event['content']['history_visibility']
        self.register(event, info)

    def m_room_guest_access(self, event):
        ''' Process m.room.guest_access event '''
        info = "guest_access: %s" % event['content']['guest_access']
        self.register(event, info)

    def m_room_canonical_alias(self, event):
        ''' Process m.room.canonical_alias event '''
        if event['content']['alias'] == '':
            info = "canonical_alias: replaced"
        else:
            info = "canonical_alias: %s" % event['content']['alias']
        self.register(event, info)

    def m_room_avatar(self, event):
        ''' Process m.room.avatar '''
        info = "room_avatar: %s" % self.reg.convert_mxc(event['content']['url'])
        self.register(event, info)
