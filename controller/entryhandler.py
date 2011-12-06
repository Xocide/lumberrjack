import model, cgi, hashlib
from google.appengine.ext import db
from datetime import datetime
from base import *

class EntryHandler(Base):
    def get(self):
        self.render('submit')
        
    def post(self):
        data = {
            'author': self.param("author"),
            'title': self.param("title"),
            'url': self.param("url"),
            'content': self.param("content"),
        }
        
        # Error checking, the old way...
        errors = []
        
        # Entry type
        if not self.param("type"):
            errors.append('Select a post type')
        
        # Entry URL
        if not self.param("url"):
            errors.append('Include the entry URL')
        
        # Entry content
        if not self.param("content"):
            errors.append('The entry content would be nice')
        
        # Post/comment author
        if not self.param("author"):
            errors.append('You forgot the authors username')
        
        # Attempt to make sure this post hasn't been submitted before...
        unique_hash = hashlib.md5(self.param("content") + self.param("author")).hexdigest()
        #entry = model.EntryDB.gql("WHERE unique_hash = :1", unique_hash)
        entry = model.PostDB.get_by_key_name(unique_hash)
        
        if entry:
            errors.append('Are you daft, this has already been submitted...')
        
        # Check if theres errors...
        if len(errors) > 0:
            self.render('submit', {'data': data, 'errors': errors, 'test_var': None})
        else:
            # Yes, I am very aware that the unique hash is stored THREE TIMES
            # I do this because one day the key_name and/or id format _may_ change.
            # However due to my suckyness at python and the GAE, probably not.
            entry = model.PostDB(
                key_name = unique_hash,
                id = unique_hash,
                unique_hash = unique_hash,
                type = self.param("type"),
                title = self.param("title", ''),
                url = self.param("url"),
                content = self.param("content"),
                author_name = self.param("author"),
                votes = 0,
                published = 0
            )
            entryID = entry.put()
            
            self.render('thanks', {'id': entryID, 'unique_hash': unique_hash})
