from base import *
import model

class MainHandler(Base):
    def get(self, id = None):
        if id:
            self.render('view', {})
        else:
            #posts = model.PostDB.all().order('-created')
            posts = model.PostDB.gql("WHERE published = 1 ORDER BY created DESC")
            self.render('index', {'posts': posts})
