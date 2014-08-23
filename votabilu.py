#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from _config import votabilu_conf as config
from os import path

class VotaBilu(object):
    @cherrypy.expose
    def index(self):
        return open(path.join(config.STATIC_DIR, 'index.html'))

cherrypy.quickstart(VotaBilu(), '/', config.CHERRYPY_CONFIG)