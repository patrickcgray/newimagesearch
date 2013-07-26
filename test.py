'''
Created on Feb 6, 2013

@author: clifgray
'''
import httplib, urllib2, urlparse

from BeautifulSoup import BeautifulSoup

alist = [u'http://i.imgur.com/nLP1c.jpg', u'http://i.imgur.com/sFMYAVy.jpg', u'http://i.imgur.com/sFMYAVy.jpg', u'http://i.imgur.com/lRrRXEi.jpg', u'http://i.imgur.com/lRrRXEi.jpg', u'http://i.imgur.com/mlWFMLq.jpg', u'http://i.imgur.com/mlWFMLq.jpg', u'http://i.imgur.com/hgGNHiR.jpg', u'http://i.imgur.com/hgGNHiR.jpg', u'http://i.imgur.com/AZiyUmi.jpg', u'http://i.imgur.com/AZiyUmi.jpg', u'http://i.imgur.com/sJiH5iF.jpg', u'http://i.imgur.com/sJiH5iF.jpg', u'http://i.imgur.com/l6SMYf2.jpg', u'http://i.imgur.com/l6SMYf2.jpg', u'http://i.imgur.com/UXHativ.jpg', u'http://i.imgur.com/UXHativ.jpg', u'http://i.imgur.com/CsH3C60.jpg', u'http://i.imgur.com/CsH3C60.jpg', u'http://i.imgur.com/7ZtKkwm.jpg', u'http://i.imgur.com/7ZtKkwm.jpg', u'http://i.imgur.com/eaoIlMr.jpg', u'http://i.imgur.com/eaoIlMr.jpg', u'http://i.imgur.com/8tvEq3z.jpg', u'http://i.imgur.com/8tvEq3z.jpg', u'http://i.imgur.com/nLP1c.jpg', u'http://i.imgur.com/sFMYAVy.jpg', u'http://i.imgur.com/lRrRXEi.jpg']


def soupify_url(url):
    try:
        hdr = {'User-Agent': 'newimagesearchapp-urllib2'}
        req = urllib2.Request(url,headers=hdr)
        page = urllib2.urlopen(req)
        return BeautifulSoup.BeautifulSoup(page)
    except urllib2.URLError, e:
        print e
        print "URLError in soupifying"
        return 
    except ValueError:
        print "ValueError in soupifying"
        return
    except httplib.InvalidURL:
        print "InvalidURL error in soupifying"
        return
    except httplib.BadStatusLine:
        print "BadStatusLine error in soupifying"
        return
    except:
        print "some other error in soupifying"
        return
    
#print soupify_url('reddit.com/r/motorcycles/')

string = 'asad/'

print string[-1]