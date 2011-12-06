import os
from google.appengine.api import users
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
        self.set('user', self.user())
        if self.user():
            # Check if they've visited before...
            user = model.UserDB.get_by_key_name(self.user().user_id())
            if not user:
                user = model.UserDB(
                    key_name = self.user().user_id(),
                    user_id = self.user().user_id(),
                    email = self.user().email(),
                    is_admin = 0
                )
                user.put()
            
            self.current_user = {
                'nickname': self.user().nickname(),
                'email': self.user().email(),
                'id': self.user().user_id(),
                'is_admin': user.is_admin
            }
            self.set('current_user', self.current_user)

    def set(self, arg, val):
        self.view_data[arg] = val

    def render(self, view, data = {}):
        data = dict(self.view_data.items() + data.items())
        self.response.out.write(template.render(self.view_path % (view), data))

    def param(self, arg, default = None):
        return self.request.get(arg, default)
    
    def user(self):
        if users.get_current_user():
            return users.get_current_user()
        else:
            return None