from base import *

class UserLogin(Base):
    def get(self):
        self.redirect('/')

class UserLogout(Base):
    def get(self):
        self.redirect('/')