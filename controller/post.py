import model, libs, cgi, hashlib, json
from google.appengine.ext import db
from datetime import datetime
from base import *

from libs.canopy import ForrstAPI

class PostNew(Base):
    def get(self):
        self.render('submit')
        
    def post(self):
        fapi = ForrstAPI(use_SSL=False)
        
        url_bits = self.param("url").split('-')
        tiny_id = url_bits[len(url_bits)-1]
        
        post = fapi.posts_show(tiny_id=tiny_id)
        
        data = {
            'type': post['post_type'],
            'title': post['title'],
            'url': post['post_url'],
            'post_id': post['id'],
            'tiny_id': post['tiny_id'],
            'f_created_at': post['created_at'],
            'f_updated_at': post['updated_at'],
            'content': post['content'],
            'author_name': post['user']['name'],
            'author_username': post['user']['username'],
            'author_url': post['user']['url'],
            'description': post['description'],
            'formatted_description': post['formatted_description'],
            'snaps': json.dumps(post['snaps'])
        }
        
        post = model.PostDB.get_by_key_name(data['tiny_id'])
        
        if not post:
            post = model.PostDB(
                key_name = tiny_id,
                type = data['type'],
                title = data['title'],
                url = data['url'],
                post_id = data['post_id'],
                tiny_id = data['tiny_id'],
                f_created_at = data['f_created_at'],
                f_updated_at = data['f_updated_at'],
                content = data['content'],
                author_name = data['author_name'],
                author_username = data['author_username'],
                author_url = data['author_url'],
                description = data['description'],
                formatted_description = data['formatted_description'],
                votes = 0,
                published = 0
            )
            post.put()
            self.render('thanks') #, {'fucker': post})
        else:
            self.render('submit', {'exists': True})