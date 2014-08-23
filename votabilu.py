#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from _config import votabilu_conf as config
from _config import secrets as secret
from os import path
from jinja2 import Environment, FileSystemLoader
import redis

env = Environment(loader = FileSystemLoader('static'))


def get_ranking():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    ranking = {}
    for e in r.zrange('hof', 0, 9):
        ranking[e] = r.zscore('hof', e)
    return ranking

def get_random_candidate(sorteds = None):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    candidate = r.srandmember('candidatos:SP')
    while candidate in sorteds:
        candidate = r.srandmember('candidatos:SP')
    return candidate

def get_candidate(candidate_id):
    token = secret.token
    headers = {'content-type': 'application/json', 'App-Token': token, 'Accept': 'application/json'}
    url_base = 'http://api.transparencia.org.br/api/v1/'
    page = 0
    candidatos = requests.get(url_base + 'candidatos/' + candidate_id, headers=headers)
    return candidatos.json()


def insert_in_ranking(name, score):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    if r.zcount('hof', score, 1000000000) == 0:
        return False
    else:
        if r.zadd('hof', name, score) == 1:
            r.zremrangebyrank('hof', -1, -1)
        return True


class VotaBilu(object):
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(title = 'Vota, Bilu!')

    @cherrypy.expose
    def play(self):
        tmpl = env.get_template('candidato.html')
        return tmpl.render()

    @cherrypy.expose
    def hof(self):
        tmpl = env.get_template('hof.html')
        ranking = get_ranking()
        return tmpl.render(title = 'Hall of Fame',
            n1 = ranking.keys()[0], s1 = str(ranking[ranking.keys()[0]]),
            n2 = ranking.keys()[1], s2 = str(ranking[ranking.keys()[1]]),
            n3 = ranking.keys()[2], s3 = str(ranking[ranking.keys()[2]]),
            n4 = ranking.keys()[3], s4 = str(ranking[ranking.keys()[3]]),
            n5 = ranking.keys()[4], s5 = str(ranking[ranking.keys()[4]]),
            n6 = ranking.keys()[5], s6 = str(ranking[ranking.keys()[5]]),
            n7 = ranking.keys()[6], s7 = str(ranking[ranking.keys()[6]]),
            n8 = ranking.keys()[7], s8 = str(ranking[ranking.keys()[7]]),
            n9 = ranking.keys()[8], s9 = str(ranking[ranking.keys()[8]]),
            n10 = ranking.keys()[9], s10 = str(ranking[ranking.keys()[9]]))


cherrypy.quickstart(VotaBilu(), '/', config.CHERRYPY_CONFIG)