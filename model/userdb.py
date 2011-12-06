from google.appengine.ext import db

class UserDB(db.Model):
    user_id   = db.StringProperty()
    is_admin  = db.IntegerProperty()
    email     = db.StringProperty()