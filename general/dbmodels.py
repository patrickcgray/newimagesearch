'''
Created on Feb 13, 2013

@author: clifgray
'''

from google.appengine.ext import ndb
from pagehandlers.basehandler import render_str

class Keyword(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add = True)
    pic_links = ndb.StringProperty(required = True, repeated = True)
    bad_pic_links = ndb.StringProperty(required = True, repeated = True)
    relevant_keywords = ndb.StringProperty(required = True, repeated = True)
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", c = self)
    
class Pic_Link(ndb.Model):
    keywords = ndb.StringProperty(required = True, repeated = True)
    quality = pic_links = ndb.IntegerProperty(required = True)
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("comment.html", c = self)