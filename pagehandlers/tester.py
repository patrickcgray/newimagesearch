from basehandler import BlogHandler

class Tester(BlogHandler):
    def get(self):
        self.render("working.html")         