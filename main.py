#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Created by Richard Glover on 2010-03-16.
Copyright (c) 2010 GloverDesigns. All rights reserved.
"""
# UNCOMMENT THIS BEFORE DEPLOYMENT TO APP SERVER
#from google.appengine.dist import use_library
#use_library('django', '1.1')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
from google.appengine.ext.webapp import util

def main():
    application = django.core.handlers.wsgi.WSGIHandler()
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

