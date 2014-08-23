#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from _config import votabilu_conf as config
from os import path
from jinja2 import Environment, FileSystemLoader
import redis

env = Environment(loader = FileSystemLoader('static'))

class VotaBilu(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(title = 'Vota, Bilu!')

    def get_random_candidate(sorteds = None):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        candidate = r.srandmember('candidatos:SP')
        while candidate in sorteds:
            candidate = r.srandmember('candidatos:SP')
        return candidate


cherrypy.quickstart(VotaBilu(), '/', config.CHERRYPY_CONFIG)