import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import model

class Base(webapp.RequestHandler):
    """
        Totally stolen from squeeks' forrst-quote app.
        Please dont freak on me man, I totally suck at python.
        Credits to all who created that app.
    """

    view_path = "./views/%s.html"
    view_data = {}
    current_user = {'is_admin': 0}

    def __init__(self):
        self.set('current_user', self.current_user)

    def set(self, arg, val):
        self.view_data[arg] = val

    def render(self, view, data = {}):
        data = dict(self.view_data.items() + data.items())
        self.response.out.write(template.render(self.view_path % (view), data))

    def param(self, arg, default = None):
        return self.request.get(arg, default)
    
    def user(self):
        return None