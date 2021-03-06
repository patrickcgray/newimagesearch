'''
Created on Feb 6, 2013

@author: clifgray
'''

import urllib2, urlparse, httplib, pickle
import imageInfo, scrape_bing
from BeautifulSoup import BeautifulSoup
from collections import deque
from google.appengine.api import urlfetch

urlfetch.set_default_fetch_deadline(15)

from google.appengine.ext import ndb

def get_collected_pics(input_keywords, link_list=[]):

    visited_pages = []
    visit_queue = deque([])
    collected_pages = []
    collected_pics = []
    
    def scrape_pages(url, root_url, keywords=[], recurse=True):
        #variables
        max_count = 8
        pic_num = 100
        
        print 'the keywords and current url are'
        print keywords
        print url
        if url[0:4] != 'http':
            url = 'http://' + url
    
        #this is all of the links that have been scraped
        the_links = []
        
        soup = soupify_url(url)
        if not soup and visit_queue:
            link = visit_queue.popleft()
    #        print link
            scrape_pages(link, root_url, keywords)
            return
        
        #only add new pages onto the queue if the recursion argument is true    
        if recurse and soup:
            #find all the links on the page
            try:
                for tag in soup.findAll('a'):
                    the_links.append(tag.get('href'))
            except AttributeError:
                return
            try:
                print categorize_links(the_links, url, root_url)
                external_links, internal_links, root_links, primary_links = categorize_links(the_links, url, root_url)
            except TypeError:
                print 'couldn not categorize'
                return
            
        #    print 'current url'
        #    print url
        #    print 'external links'
        #    print external_links
        #    print 'internal links'
        #    print internal_links
        #    print 'root links'
        #    print root_links
        
            #change it so this depends on the input                
            
            links_to_visit = external_links + internal_links + root_links
            
            #build the queue
            for link in links_to_visit:
                if link not in visited_pages and link not in visit_queue:
                    visit_queue.append(link)
        
        visited_pages.append(url)
    #    print 'number of pages visited'
    #    print count
        
        #add pages to collected_pages depending on the criteria given if any keywords are given
        if keywords:
            page_to_add = find_pages(url, soup, keywords)
            
    #        print 'page to add'
    #        print page_to_add
            if page_to_add and page_to_add not in collected_pages:
                collected_pages.append(page_to_add)
            
        pics_to_add = add_pics(url, soup)
    #    print 'pics to add'
    #    print pics_to_add
        if pics_to_add:
            collected_pics.extend(pics_to_add)
        
        #here is where the actual recursion happens by finishing the queue
        print 'recursing down to next level'
        while visit_queue:
            if len(visited_pages) >= max_count:
                print 'enough pages visited'
                return
            
            if len(collected_pics) > pic_num:
                print 'enough pics'
                return
            
            link = visit_queue.popleft()
    #        print link
            print 'calling myself again'
            scrape_pages(link, root_url, keywords)
            
    #    print '***done***'
        ###done with the recursive scraping function here        
        
                
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
    
    def categorize_links(the_links, url, root_url):
        external_links = []
        internal_links = []
        root_links = []
        primary_links = []
        
        for link in the_links:
            try:
                parsed_url = urlparse.urlparse(url)
                netloc = parsed_url.netloc
                try:
                    site_name = (netloc.split('.')[1]) + '.' + (netloc.split('.')[2])
                except IndexError:
                    #I am sure this is missing some important page but it is alright for now.
                    print 'indexerror in categorizing the links'
                    return
    
                if 'http' in link and site_name not in link:
                    external_links.append(link)
                elif site_name in link:
                    internal_links.append(link)
                else:
                    root_links.append('http://' + netloc + link)
                    
                if root_url in link:
                    primary_links.append(link)
                    
            #dangerous
            except TypeError:
                print 'typeerror in categorizing the links'
                something = None
                
        return external_links, internal_links, root_links, primary_links
    
    #need to think about this and fix it up
    def add_pics(url, soup):
        more_pics = []
        if url[-3:] == 'jpg' or url[-3:] == 'png' or url[-3:] == 'gif':
            filtered_pic = filter_pic(url)
            if filtered_pic:
                more_pics.append(filtered_pic)
        
        parsed_url = urlparse.urlparse(url)
        #need to add img tags
        for tag in soup.findAll('img'):
            img_url = tag.get('src')
            if img_url:
                if img_url[-3:] == 'jpg' or img_url[-3:] == 'png' or img_url[-3:] == 'gif':
                    filtered_pic = filter_pic(img_url)
                    if not filter_pic:
                        result = parsed_url.scheme + '://' + parsed_url.netloc + '/' + img_url
                        filtered_pic = filter_pic(result)
                    if filtered_pic:
                        more_pics.append(filtered_pic)
                        
        for tag in soup.findAll('a'):
            img_url = tag.get('href')
            if img_url:
                if img_url[-3:] == 'jpg' or img_url[-3:] == 'png' or img_url[-3:] == 'gif':
                    filtered_pic = filter_pic(img_url)
                    if not filter_pic:
                        result = parsed_url.scheme + '://' + parsed_url.netloc + '/' + img_url
                        filtered_pic = filter_pic(result)
                    if filtered_pic:
                        more_pics.append(filtered_pic)
                    
        return more_pics
    
    def filter_pic(url):
        try:
            file = urllib2.urlopen(url).read()
            
            content_type, width, height = imageInfo.getImageInfo(file)
            if width > 200 and height > 200:
                return url
            else:
                print 'image didnt pass the filter'
                print url
                return None
            
        except ValueError:
            print 'could not filter'
            print url
            return None
        except urllib2.HTTPError:
            print 'could not filter'
            print url
            return None
        except AttributeError:
            print 'could not filter'
            print url
            return None
        except:
            print 'could not filter'
            print url
            return None
    
    def find_pages(url, soup, keywords):
        #collect something from the pages right here...
        #currently I am testing for keywords and adding the page to a list if they contain them
    #    print 'testing the page for keywords'
        all_text = soup.getText()
    
        counter = 0
        for item in keywords:
            if item in all_text:
                counter += 1
        if counter > 0:
            return url, counter
        else:
            return None
        
    def store_kewords_and_pics():
        store = None
        
        
    def update_pics(collected_pics, main_path, save_path):        
        stored_pictures = []
        try:
            main_file = open(main_path, 'r')
            stored_pictures = pickle.load(main_file)
            main_file.close()
        except EOFError:
            saved_file = open(save_path, 'r') 
            saved_pics = pickle.load(saved_file)
            stored_pictures = saved_pics
            saved_file.close()
        
        for pic in collected_pics:
            if pic not in stored_pictures:
                stored_pictures.append(pic)
        
        main_file = open(main_path, 'w')
        save_file = open(save_path, 'w') 
        pickle.dump(stored_pictures, main_file)
        pickle.dump(stored_pictures, save_file)
        main_file.close()
        save_file.close()
    
    #I could find frequency of words on pages or crawl the web to see how often a page is referenced or
    #I could let the users have a say in the ranking and I could take some new attributes into consideration like image quality and size and frequency of visitation
    
    ###other random functions
    
    def countTags(soup, tag):
        tags = soup.findAll(tag)
        return tags.length    
    
    def printText(tags):     
        for tag in tags:         
            if tag.__class__ == BeautifulSoup.BeautifulSoup.NavigableString:             
                print tag 
            else: 
                printText(tag)
    
    if not link_list:
        print 'no link list'
        visit_queue, the_url = scrape_bing.get_links(input_keywords, a_list = False)
        scrape_pages(visit_queue.popleft(), the_url, input_keywords, recurse=True)
        
    #search with a suggested link and keywords
    else:
        print 'link list'
        for link in link_list:
            visit_queue.append(link)
        first_link = visit_queue.popleft()
        scrape_pages(first_link, first_link, input_keywords, recurse=True)

    print visited_pages
    return list(set(collected_pics))

#print get_collected_pics(['motorcycles'], ['http://www.reddit.com/r/motorcycles', 'http://www.imgur.com/r/motorcycles'])