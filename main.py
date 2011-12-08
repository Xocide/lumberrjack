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
        (r'/submit', controller.PostNew)
    ]
    
    application = webapp.WSGIApplication(url_map, debug=True)
    
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
