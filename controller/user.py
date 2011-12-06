from base import *

class UserLogin(Base):
    def get(self):
        self.redirect(users.create_login_url('/'))

class UserLogout(Base):
    def get(self):
        self.redirect(users.create_logout_url('/'))