#this file has all of the small handlers that do not need their own file

#internal imports
from basehandler import BlogHandler

import logging, scraper
from operator import attrgetter

import webapp2

#this is actually my front root page right now
class Try(BlogHandler):
    def get(self):
        keywords = self.request.get('keywords')
        if keywords:
            keywords = str(keywords)
            keyword_list = keywords.split()
            print 'keyword list right in try'
            print keyword_list
        
        url_list = self.request.get('url_list')
        if url_list:
            url_list = str(url_list)
            url_list = url_list.split(', ')
        
        img_list = []
        if keyword_list and url_list:
            img_list = scraper.get_collected_pics(keyword_list, url_list)
        elif keyword_list:
            img_list = scraper.get_collected_pics(keyword_list)
        else:
            self.redirect('/')
        
        self.render("results.html", img_list=img_list)
        

class LoadingPage(BlogHandler):
    def get(self):
        self.render("loading.html")
        keywords = self.request.get('keywords')
        url_list = self.request.get('url_list')
            
        if keywords and url_list:
            self.redirect("/try?keywords=%s&url_list=%s" % (keywords, url_list))
        elif keywords:
            self.redirect("/try?keywords=%s" % (keywords))
        else:
            self.redirect('/')
        

class FrontPage(BlogHandler):
    def get(self):
        keywords = self.request.get('keywords')
        url_list = self.request.get('url_list')
            
        if keywords and url_list:            
            self.redirect("/loading?keywords=%s&url_list=%s" % (keywords, url_list))
        elif keywords:
            self.redirect("/loading?keywords=%s" % (keywords))
        else:
            self.render("frontpage.html")

class About(BlogHandler):
    def get(self):
        self.render('about.html')
                               
class Purchase(BlogHandler):
    def get(self):
        self.render('purchase.html')

class Testimonials(BlogHandler):
    def get(self):
        self.render('testimonials.html')
        
class Deals(BlogHandler):
    def get(self):
        self.render('deals.html')

class Include(BlogHandler):
    def get(self):
        self.render('include.html')

#sent whenever a page has not been completed
class Working(BlogHandler):
    def get(self):
        self.render('working.html')
        
class NoAccess(BlogHandler):
    def get(self):
        self.render('noaccess.html')

#links to social media info
class Share(BlogHandler):
    def get(self):
        self.render('share.html')
