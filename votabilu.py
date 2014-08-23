#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
from _config import votabilu_conf as config
from _config import secrets as secret
from os import path
from jinja2 import Environment, FileSystemLoader
import redis
import requests

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
        candidato = get_candidate(get_random_candidate([]))
        if 'miniBio' in candidato.keys():
            minibio = candidato['miniBio']
        else:
            minibio = 'Candidato nao tem minibio.'
        return tmpl.render(foto = candidato['foto'],
            dica1 = minibio,
            dica2 = 'Idade: ' + candidato['idade'] + ' anos',
            dica3 = 'Instrucao: ' + candidato['instrucao'],
            dica4 = 'Ocupacao: ' + candidato['ocupacao'],
            dica5 = 'Partido: ' + candidato['partido'],
            dica6 = 'Cargo: ' + candidato['cargo'],
            dica7 = 'Letras do nome: ' + candidato['apelido'].upper(),
            name = candidato['apelido'])

    @cherrypy.expose
    def hof(self):
        tmpl = env.get_template('hof.html')
        ranking = get_ranking()
        return tmpl.render(title = 'Hall of Fame',
            n1 = "Eneas", s1 = 1000000000000,
            n2 = "Bilu", s2 = 10000000000,
            n3 = "Minion", s3 = 10000000000,
            n4 = "Plinio", s4 = 100000000,
            n5 = "Pedrinho", s5 = 10000000,
            n6 = "Poo", s6 = 1000000,
            n7 = "Huguinho", s7 = 500000,
            n8 = "Bolinha", s8 = 400000,
            n9 = "Carol", s9 = 300000,
            n10 = "Gugu", s10 = 200000


cherrypy.quickstart(VotaBilu(), '/', config.CHERRYPY_CONFIG)