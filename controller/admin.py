from base import *

class AdminDashboard(Base):
    def get(self):
        if not self.current_user['is_admin']:
            self.redirect('/gtfo')
            return
        
        posts = model.PostDB.all().order('-created') #gql("WHERE published = 0 ORDER BY created DESC")
        self.render('admin/dashboard', {'cu': self.current_user, 'posts': posts})
    
    def post(self):
        if not self.current_user['is_admin']:
            self.redirect('/gtfo')
            return
        
        post = model.PostDB.get_by_key_name(self.param("post_id"))
        
        if post and self.param("approve"):
            post.published = 1
            post.put()
            self.redirect('/admin.php')
        elif post and self.param("delete"):
            post.delete()
            self.redirect('/admin.php')