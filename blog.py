import webapp2

from pagehandlers import otherhandlers
from pagehandlers import tester

#this is the information for all the handlers and their regexes and everything
app = webapp2.WSGIApplication([('/', otherhandlers.FrontPage),
                               ('/tester', tester.Tester),
                               ('/loading', otherhandlers.LoadingPage),
                               ('/purchase', otherhandlers.Purchase),
                               ('/testimonials', otherhandlers.Testimonials),
                               ('/deals', otherhandlers.Deals),
                               ('/include', otherhandlers.Include),  
                               ('/about', otherhandlers.About),
                               ('/working', otherhandlers.Working),
                               ('/noaccess', otherhandlers.NoAccess),
                               ('/try', otherhandlers.Try),                            
                               ],
                               debug=True)

############# end all code #############