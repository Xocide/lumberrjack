import model, libs, cgi, hashlib, yaml
from django.utils import simplejson as json
from google.appengine.ext import db
from datetime import datetime
from base import *
from urllib2 import HTTPError

from libs.pynecone.pynecone import Post as ForrstPost
from libs.pynecone.pynecone import User as ForrstUser

class PostNew(Base):
    def get(self):
        self.render('submit')
        
    def post(self):
        error = None
        
        url_bits = self.param("url").split('-')
        tiny_id = url_bits[len(url_bits)-1]
        
        # Load forrst api config
        forrstapi = open('forrstapi.yaml')
        forrstconf = yaml.load(forrstapi)
        forrstapi.close()
        
        ## try to auth the user...
        try:
            usr = ForrstUser.auth(email_or_username = forrstconf['username'], password = forrstconf['password'])
        except HTTPError, e:
            error = None
            if str(e) == "HTTP Error 401: Unauthorized":
                error = "Auth error"
            else:
                error = e
            
            self.render('submit', {'error': error})
            return
        
        # Try to fetch the page...
        try:
            post = ForrstPost.show(tiny_id = tiny_id, access_token = usr['resp']['token'])
            post = post['resp']
        except HTTPError, e:
            if str(e) == "HTTP Error 404: Not Found":
                error = "Invalid post"
            else:
                error = e
            
            self.render('submit', {'error': error})
            return
        
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
            'formatted_description': post['formatted_description']
        }
        if 'snaps' in post:
            data['snaps'] = json.dumps(post['snaps'])
        
        post = model.PostDB.get_by_key_name(data['tiny_id'])
        
        if post:
            error = 'Are you daft? thats already been submitted'
        
        if not error:
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
            
            if 'snaps' in data:
                post.snaps = data['snaps']
            
            post.put()
            self.render('thanks')
        else:
            self.render('submit', {'error': error})