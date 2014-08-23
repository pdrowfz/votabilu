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

    def get_ranking():
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        ranking = {}
        for e in r.zrange('hof', 0, 9):
            ranking[e] = r.zscore('hof', e)
        return ranking

    def insert_in_ranking(name, score):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)
        if r.zcount('hof', score, 1000000000) == 0:
            return False
        else:
            if r.zadd('hof', name, score) == 1:
                r.zremrangebyrank('hof', -1, -1)
            return True


cherrypy.quickstart(VotaBilu(), '/', config.CHERRYPY_CONFIG)