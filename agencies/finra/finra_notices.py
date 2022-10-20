import requests
from datetime import date
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import uuid
from services.common_services import common_functions
obj_com = common_functions()


class scanning_notice:


    def __init__(self):
        pass

        #start function
    def start_scanning(self,url,no_month):
        
        try:
            rss_list=[]

            
            last_scan_date=obj_com.extract_month_date(no_month)

            rss_data_list=obj_com.fetch_rss(url)         
            
            #print(rss_data_list)
            for rss_data in rss_data_list:
                topic_data={}
                topic_data=rss_data

                if len(rss_data)>0 :

                    pub_date=rss_data["published_date"]
                    
                    if pub_date < last_scan_date:
                        break    


                    details_link = rss_data["link"]

                    details,topic_list=self.fetch_details(details_link)
                    topic_data['details'] = details
                    topic_data['topics'] = topic_list
                    rss_list.append(topic_data)

                 

            
        except Exception as ex:
            print(ex)
        return {"finra_notices":rss_list}

    def fetch_details(self,url):
        link_text=""

        html_content = requests.get(url).text
        Bsoup = BeautifulSoup(html_content, "lxml")
        input_tag = Bsoup.find_all(attrs={"id" : "block-finra-bootstrap-sass-system-main"})
        if len(input_tag) > 0:
            link_text = str(BeautifulSoup(str(input_tag[0]), "lxml"))
        else:
            link_text = ""


        topic_tag = Bsoup.find_all(attrs={"class": "field--name-field-notice-topic-tax"})
        topic_type_list=[]
        if len(topic_tag) == 1:
            topic_list = topic_tag[0].find_all(attrs={"class": "field__item"})
            if len(topic_list) > 0:
                for topic in topic_list:

                    topic_name = str(topic.text).title()
                    topic_type_list.append(topic_name)
                    

        return link_text ,topic_type_list