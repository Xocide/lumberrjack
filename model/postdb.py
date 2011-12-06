from google.appengine.ext import db

class PostDB(db.Model):
    author_name  = db.StringProperty()
    type         = db.StringProperty()
    title        = db.StringProperty()
    content      = db.StringProperty(multiline=True)
    url          = db.StringProperty()
    votes        = db.IntegerProperty()
    created      = db.DateTimeProperty(auto_now_add=True)
    unique_hash  = db.StringProperty()
    published    = db.IntegerProperty()