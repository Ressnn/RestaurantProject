# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 21:48:39 2019

@author: Pranav Devarinti
"""
import numpy as np
import tornado.ioloop
import tornado.web as web
import tornado
from tornado.web import Application,RequestHandler,RedirectHandler
import hashlib
import datetime
from secrets import *
import codecs
import os
import json
# In[]
loop = tornado.ioloop.IOLoop.instance()
User_list = dict()
try:
   with open(r"UAS.json",'r') as f:
        User_list = json.load(f)
except:
    with open(r"UAS.json",'a+') as f:
        User_list['Pranav'] = {'password':'D','Currentlist':np.random.uniform(low=-1,high=1,size=(100)).tolist()}
        User_list['Sujit'] = {'password':'I','Currentlist':np.random.uniform(low=-1,high=1,size=(100)).tolist()}
        print('dumped')
        json.dump(User_list,f)
Token_list = dict()
restraunt_list = {'LR':np.random.uniform(low=-1,high=1,size=(100)),'PR':np.random.uniform(low=-1,high=1,size=(100)),'RA':np.random.uniform(low=-1,high=1,size=(100))}
# In[]

    

class MainH(RequestHandler):
    def get(self):
        self.render('index.html')
    def post(self):
        rd = self.get_argument('Redirect')
        if rd == 'Login':
            print(rd)
            self.redirect('/Start')
        else:
            self.redirect('/Signup')
    
    
class StartH(RequestHandler):
    def get(self):
        self.render('startup.html')

class Stop(RequestHandler):
    def get(self):
        global loop
        self.send_error(200)
        loop.stop()
        del loop
class Login(RequestHandler):
    def get(self):
        self.render('login_page.html')
    def post(self):
        
        try:
            User = User_list[self.get_argument("uname")]
            print(User)
            if self.get_argument("psw") == User['password']:
                x = token_urlsafe(16)
                self.set_secure_cookie("Sess",x)
                Token_list[x] = self.get_argument("uname")
                self.redirect('/Home')
                print('accepted')
            else:
                print('Incorrect Username Or Password')
                print(self.get_argument("psw"))
        except:
            print("Bad Request")
            self.redirect('/Login')
            
class Home(RequestHandler):
    def get(self):
        try: 
            Se = str(self.get_secure_cookie("Sess"))[2:-1]
            print(Se)
            User = Token_list[Se]
            cv = str(User_list[User]['Currentlist'])
            message = '''<html>
            <head>
            <style>
            body {
            	background-color:rgb(100, 221, 233)
            	}
            	</style>
            </head>
            <body>
            <h1>Welcome<h1>
            <h1>||<h1>
            <h1>Your current food values are<h1>
            <p>|\|</p>
            </body>'''
            message = message.replace('||',User)
            message = message.replace('|\|',cv)
            self.write(message)
            
            
        except:
            print('Sending back')
            self.redirect('/Login')
    
class Signup(RequestHandler):
    def get(self):
        self.render('signup_page.html')
    def post(self):
        try:
            User_list[self.get_argument("uname")] = {'password':self.get_argument("psw"),'Currentlist':np.random.uniform(low=-1,high=1,size=(100))}
            x = token_urlsafe(16)
            self.set_secure_cookie("Sess",x)
            Token_list[x] = self.get_argument("uname")
            with open(r"C:\Users\ASUS\Desktop\RestaurantProject-master\UAS.json",'w') as f:
                json.dump(User_list,f)
            self.redirect('/Home')
            print('accepted')
        except:
            print("Bad Request")
            self.redirect('/')
            
application = tornado.web.Application([
    (r"/", MainH),
    (r"/Start", StartH),
    (r"/Stop", Stop),
    (r"/Login", Login),
    (r"/Home", Home),
    (r"/Signup", Signup),
    (r'/js/(.*)', web.StaticFileHandler),
    (r'/css/(.*)', web.StaticFileHandler),
    (r'/images/(.*)', web.StaticFileHandler),
], cookie_secret=token_urlsafe(16),)
    
application.listen(8888)
loop.start()
