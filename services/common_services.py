import feedparser
from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
from datetime import timedelta , datetime
from dateutil.relativedelta import *
import uuid
import re
import os

CLEANR = re.compile('<.*?>')
class common_functions :
    def __init__(self):
        self.user_id=1

    def cleanhtml(self,raw_html):

        cleantext = re.sub(CLEANR, '', raw_html)

        return cleantext

    def remove_img_tags(self,data):
        p = re.compile(r'<figure.*?/>')
        return p.sub('', data)


    def extract_month_date(self,no_month):
        curr_date = datetime.now().date()

        
        selected_date = curr_date + relativedelta(months=-no_month)
        return str(selected_date)
    def fetch_rss(self,url):
        #url="http://feeds.finra.org/news-and-events/feed"
        feed = feedparser.parse(url)

        feed_entries = feed.entries

        feed_list = []
        feed_dict = {}
        i = 0

        for feed in feed_entries:
            # print(feed)
            link_text = ""

            feed_dict = {}
            feed_dict['id']=str(uuid.uuid4().hex)
            if 'title' in feed:

                feed_dict['title'] =self.cleanhtml( feed['title'])
            if 'link' in feed:
                feed_dict['link'] = feed['link']
            if 'summary' in feed:
                feed_dict['summary'] =self.cleanhtml( feed['summary'])
            if 'published' in feed:
                p_date = feed['published']
                n_date=parse(str(p_date), fuzzy=True).date()
                feed_dict['published_date'] = str(datetime.strptime(str(n_date), '%Y-%m-%d').date())
            feed_dict['details'] = ""
            feed_dict['topics'] = []


            feed_list.append(feed_dict)
            # if i > 1:
            #
            #     break
            i = i + 1
        return feed_list


    