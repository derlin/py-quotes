#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# see :
# http://cherrypy.readthedocs.org/en/latest/tutorials.html#tutorial-7-give-us-a-rest


import os
import os.path
import sqlite3
import datetime as d

import cherrypy
import simplejson as json


current_dir = os.path.dirname(os.path.abspath(__file__))
DB_STRING = os.path.join(current_dir, "../quotes.db")


class StringGenerator(object):

    @cherrypy.expose
    def index(self):
        return open(os.path.join(current_dir, 'index.html')).read()

    @cherrypy.expose
    # @cherrypy.tools.json_out()
    def ToJson(self):
        conn = sqlite3.connect(DB_STRING)
        cur = conn.cursor()
        cur.execute("SELECT * FROM quotes")
        result = cur.fetchall()
        cur.close()
        conn.close()

        res = []

        for r in result:
            a = {'author': r[1], 'quote': r[2]}
            res.append(a)
            # a[0] = a[0].split(".")[0]


        cherrypy.response.headers['Content-Type'] = "application/json;charset=UTF-8"
        return json.dumps(res, indent=4, ensure_ascii=False).encode("UTF-8")


class StringGeneratorWebService(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        conn = sqlite3.connect(DB_STRING)
        cur = conn.cursor()
        cur.execute("SELECT * FROM quotes")
        result = cur.fetchall()
        cur.close()
        conn.close()
        return json.dumps(result)

    @cherrypy.tools.accept(media='text/json')
    def POST(self):

        text = None
        author = None
        ret = "OK"

        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = json.loads(rawbody)

        if "text" in body:
            text = body["text"]
        if "author" in body:
            author = body["author"]

        if text is None:
            cherrypy.response.status = 500
            return "ERROR"

        date = d.datetime.now()
        conn = sqlite3.connect(DB_STRING)
        c = conn.cursor()

        try:
            c.execute('insert into quotes values(?, ?, ?)', [date, author, text])
            conn.commit()

        except Exception as e:
            print(e)
            ret = "ERROR"

        c.close()
        conn.close()
        print("OK")

        return ret

        # some_string = ''.join(random.sample(string.hexdigits, int(length)))
        # conn = sqlite3.connect(DB_STRING)
        # cur = conn.cursor()
        # cur.execute("INSERT INTO quotes VALUES (?, ?)", [int(1), some_string])
        # conn.commit()
        # cur.close()
        # conn.close()
        # return some_string

    def PUT(self):

        ret = "OK"

        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body = simplejson.loads(rawbody)

        conn = sqlite3.connect(DB_STRING)
        c = conn.cursor()

        try:
            c.execute('update quotes set author=?, text=? where id=?', [body['1'], body['2'], body['0']])
            conn.commit()

        except Exception as e:
            print(e)
            ret = "ERROR"

        c.close()
        conn.close()
        print("OK")

        return ret

    def DELETE(self, id):
        with sqlite3.connect(DB_STRING) as c:
            c.execute("DELETE FROM quotes WHERE id=?",
                      [id])


def setup_database():
    """
 Create the `user_string` table in the database
 on server startup
 """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("CREATE TABLE IF NOT EXISTS quotes (id TIMESTAMP PRIMARY KEY , author TEXT, text TEXT)")


def cleanup_database():
    """
 Destroy the `user_string` table from the database
 on server shutdown.
 """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE quotes")


if __name__ == '__main__':
    conf = {

        'global': {
            # 'server.socket_host': "127.0.0.1",
            # 'server.socket_port': 14000,
            'tools.staticfile.root': os.path.dirname(os.path.abspath(__file__)),
            'tools.encode.on': True,
            # 'tools.encode.encoding': "utf-8",
            # 'tools.sessions.on': True,
            # 'tools.sessions.locking': 'explicit',
            # 'checker.on': False
        },

        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
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

        # angular partials
        '/add.partial': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "html/well.html",
        },
        '/edit.partial': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': "html/modal.html",
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    # cherrypy.engine.subscribe('stop', cleanup_database)

print(os.path.dirname(os.path.abspath(__file__)))
webapp = StringGenerator()
webapp.generator = StringGeneratorWebService()
cherrypy.quickstart(webapp, config=conf)