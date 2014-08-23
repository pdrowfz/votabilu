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

    @cherrypy.expose
    def hof(self):
        tmpl = env.get_template('hof.html')
        return tmpl.render(title = 'Hall of Fame',
            n1 = 'HNN', s1 = '666',
            n2 = 'HNN', s2 = '666',
            n3 = 'HNN', s3 = '666',
            n4 = 'HNN', s4 = '666',
            n5 = 'HNN', s5 = '666',
            n6 = 'HNN', s6 = '666',
            n7 = 'HNN', s7 = '666',
            n8 = 'HNN', s8 = '666',
            n9 = 'HNN', s9 = '666',
            n10 = 'HNN', s10 = '666')

    def get_random_candidate(sorteds = None):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        candidate = r.srandmember('candidatos:SP')
        while candidate in sorteds:
            candidate = r.srandmember('candidatos:SP')
        return candidate

cherrypy.quickstart(VotaBilu(), '/', config.CHERRYPY_CONFIG)