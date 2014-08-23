#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from _config import votabilu_conf as config
from os import path
from jinja2 import Environment, FileSystemLoader

env = Environment(loader = FileSystemLoader('static'))

class VotaBilu(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(title = 'Vota, Bilu!')

cherrypy.quickstart(VotaBilu(), '/', config.CHERRYPY_CONFIG)