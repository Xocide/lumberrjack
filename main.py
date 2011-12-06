#!/usr/bin/env python

#
# Lumberrjack
# Each time someone posts something stupid on Forrst
# a tree crushes a kitten.
#

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import controller

def main():
    url_map = [
        (r'/', controller.MainHandler),
        (r'/submit', controller.EntryHandler),
        (r'/([a-f\d]{32})', controller.MainHandler),
        (r'/login', controller.UserLogin),
        (r'/logout', controller.UserLogout),
        (r'/admin.php', controller.AdminDashboard),
        (r'/gtfo', controller.GTFO)
    ]
    
    application = webapp.WSGIApplication(url_map, debug=True)
    
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()