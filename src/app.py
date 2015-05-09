#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'lucy'
## date : august 2013

import os.path

import cherrypy
import datetime as d
import json
import sqlite3


class WebApp(object):

    @cherrypy.expose
    def index(self):
        output = open('app.html').read()
        print("get index")

        return output

    @cherrypy.expose
    def POST(self, q):
        print("post: %s" % q)

        ret = "OK"
        date = d.datetime.now().strftime("%d.%m.%Y")

        conn = self.getconn()
        c = conn.cursor()

        try:
            quote = json.loads(q)
            c.execute('insert into quotes values(?, ?, ?)', [date] + quote)
            conn.commit()

        except Exception as e:
            print(e)
            ret = "ERROR"

        c.close()
        conn.close()
        print("OK")


    @cherrypy.expose
    def getall(self):
        conn = self.getconn()
        c = conn.cursor()
        c.execute("select * from quotes")
        quotes = c.fetchall()
        c.close()
        conn.close()
        return json.dumps(quotes)

    @cherrypy.expose
    def search(self, s=None):
        ret = None

        if s is None:
            return self.getall()

        ss = s.split("+")
        sql = "select * where text like '%" + "%' and text like '%".join(ss) + "%'"

        conn = self.getconn()
        c = conn.cursor()

        try:
            c.execute(sql)
            ret = c.fetchall()
            conn.commit()

        except Exception as e:
            print(e)

        c.close()
        conn.close()

        return json.dumps(ret)

    # ----------------------------

    @staticmethod
    def getconn():
        return sqlite3.connect("../quotes.db")


cherrypy.quickstart(WebApp(), config={

    'global': {
        'server.socket_host': "127.0.0.1",
        'server.socket_port': 14000,
        'tools.staticfile.root': os.path.dirname(os.path.abspath(__file__)),
        # 'tools.sessions.on': True,
        # 'tools.sessions.locking': 'explicit',
        # 'checker.on': False
    },

    ## css
    '/app.css': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "css/webapp.css"
    },

    ## bootstrap
    '/bt.css': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "css/bootstrap.min.css"
    },

    '/bt.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "css/bootstrap.min.js"
    },


    ## js
    '/jquery.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "jquery/jquery-1.11.3.min.js",
    },

    '/angular.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "angular/angular.min.js",
    },

    '/angular.min.js.map': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "angular/angular.min.js.map",
    },

    '/angular-route.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "angular/angular-route.min.js",
    },

    '/angular-resources.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "angular/angular-resource.js",
    },

    '/module.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "app/module.js",
    },

    '/ctrl.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "app/controller.js",
    },

    '/srv.js': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "app/service.js",
    },

    # angular
    '/modal.partial': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "html/modal.html",
    }

})