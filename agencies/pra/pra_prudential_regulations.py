import requests
from datetime import date
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import uuid
from services.common_services import common_functions
obj_com = common_functions()
import services.log as log
custom_logger = log.get_logger(__name__)


class scanning_notice:


    def __init__(self):
        self.notice_name= "pra_prudential_regulations"
    
    def start_scanning(self, url,no_month):
        
        try:
            data_list = []
            custom_logger.info("Scanning {}.".format(self.notice_name))

            last_scan_date=obj_com.extract_month_date(no_month)
            rss_data_list = obj_com.fetch_rss(url)

            for rss_data in rss_data_list:
                topic_data = {}
                topic_data = rss_data
                details_link = rss_data["link"]

                if len(rss_data) > 0:

                    pub_date=rss_data["published_date"]
                    
                    if pub_date < last_scan_date:
                        break

                    details, topic_list = self.fetch_details(details_link)
                    topic_data['details'] = details
                    topic_data['topics'] = topic_list
                
                
                data_list.append(topic_data)
                
            
        except Exception as ex:
            custom_logger.error("Error while Scanning {}, Error {} .".format(self.notice_name,ex))
        return {self.notice_name:data_list}
            



    def fetch_details(self, url):
        data = []
        try:
            html_content = requests.get(url).text

            html_content=obj_com.remove_img_tags(html_content)
            Bsoup = BeautifulSoup(html_content, "lxml")
            main_content = Bsoup.find('main', {"id": "main-content"})
            container_nav = main_content.find('div', {"class": "container container-has-navigation"})

            if container_nav is not None:
                data = container_nav.find('div', {"class": "content-block"})
                data = str(data)
            else:
                
                column_data = main_content.find_all('div', {"class": "content-block"})
                for col in column_data:
                    data.append(str(col))
                data = "".join(data)
                data = str(BeautifulSoup(data, "lxml"))
            
        except Exception as ex:
            custom_logger.error("Error while Scanning Details {}, Error {} .".format(self.notice_name,ex))
            


        return data,[]


