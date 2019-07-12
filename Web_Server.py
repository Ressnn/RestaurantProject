# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 21:48:39 2019

@author: Pranav Devarinti
"""

import tornado.ioloop
import tornado.web as web
import tornado
from tornado.web import Application,RequestHandler
import hashlib
import datetime
from secrets import *
import codecs
import os

loop = tornado.ioloop.IOLoop.instance()
class MainH(RequestHandler):
    def get(self):
        self.render('index.html')
    def post(self):
        rd = self.get_argument('Redirect')
        if rd == 'Login':
            print(rd)
            self.redirect('/Start')
    
    
class StartH(RequestHandler):
    def get(self):
        self.render('startup.html')

class Stop(RequestHandler):
    def get(self):
        global loop
        self.send_error(200)
        loop.stop()
        del loop

application = tornado.web.Application([
    (r"/", MainH),
    (r"/Start", StartH),
    (r"/Stop", Stop),
    (r'/js/(.*)', web.StaticFileHandler),
    (r'/css/(.*)', web.StaticFileHandler),
    (r'/images/(.*)', web.StaticFileHandler),
], cookie_secret=token_urlsafe(16))
    
application.listen(8080)
loop.start()