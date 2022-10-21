import requests
from datetime import date
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import uuid
from agencies.esma import config
from services.common_services import common_functions
import services.log as log
custom_logger = log.get_logger(__name__)
obj_com = common_functions()


class scanning_notice:


    def __init__(self):
        self.notice_name= "esma_news"

    def start_scanning(self, page_url,no_month):
        page_no = 0
        today = date.today()
        go_ahead_flag = True
        is_main_break = False
        news = []
        last_scan_date=obj_com.extract_month_date(no_month)
        news_list=[]
        custom_logger.info("Scanning {}.".format(self.notice_name))
        try:
            while True:
                if is_main_break == True:
                        break
                if page_no < 1:
                    url = page_url
                else:
                    url = page_url + str(page_no)
                html_content = requests.get(url).text
                soup = BeautifulSoup(html_content, "lxml")

                if go_ahead_flag == False:
                    # print("older News")
                    break

                """ 
                if you want braking the loop, uncomment the below line 
                """
                # if page_no > 0:
                #     break

                """
                define the scraping date
                """
                today = date.today()
                scrapping_date = today.strftime("%d-%m-%Y")
                record_date = (datetime.strptime(scrapping_date, '%d-%m-%Y') - timedelta(days=1)).date()
                scrapping_date = datetime.strptime(scrapping_date, '%d-%m-%Y').date()

                """
                select all the divs with class
                """
                table = soup.find("table", attrs={"class": "views-view-grid cols-2"})
                if table is None:
                    break
                rows = table.tbody.find_all("tr")

                """
                news published date
                """
                esma_news_date=""
                for tr in rows:
                    if is_main_break == True:
                        break
                    cols = tr.findAll('td')

                    for col in cols:
                        if col.find("div", attrs={"field field-type-ds"}) is not None:
                            news_date = col.find("div", attrs={"field field-type-ds"}).text.strip()
                            esma_news_date = datetime.strptime(news_date, '%d %B %Y').date()
                            #esma_news_date = datetime.strptime(str(esma_news_date, '%d-%m-%Y').date())

                        if str(esma_news_date) < last_scan_date:
                            is_main_break=True
                            break
                        
                                  

                        """ 
                        news title and link
                        """
                        title=""
                        link=""
                        if col.find('a') is not None:
                            title = col.find('a').text.strip()
                            

                            link = config.esma_url + col.find('a').get('href')

                        """ 
                        Extracting the news content or summary 
                        """
                        news_summary = col.find(attrs={"class": "news_cartouche-text"})
                        if news_summary is not None:
                            news_summary = news_summary.text.strip()
                        else:
                            news_summary = ""

                        """ 
                        news tag
                        """
                        section = col.find_all("div", attrs={"section_link"})
                        section_list = []
                        if section is not None:
                            for section in section:
                                section_list.append(section.text.strip().title())
                            else:
                                section = []

                        
                        """ 
                        Extract the news content from news link
                        """
                        details = ""
                        try:
                            if len(link):
                                news_content = requests.get(link, timeout=15).text
                                soup_details = BeautifulSoup(news_content, "lxml")
                                summary_details = soup_details.find_all("div", attrs={"id": "esmapage_main-content"})
                                details = ""
                                if (summary_details):
                                    news_text = str(summary_details[0])
                                    details = details + news_text
                                    details = BeautifulSoup(details, "lxml")
                                    details = str(details)
                                else:
                                    details = ""
                        except Exception as e:
                            details = ""

                        """
                        Extracting the news category for insuring into the database
                        """
                        news_dict = {
                            "id": str(uuid.uuid4().hex),
                            "title": title,
                            "link": link,
                            "summary": news_summary,
                            "published_date": str(esma_news_date),
                            "details": details,
                            "topics": section_list
                        }                        
                        news_list.append(news_dict)
                page_no = page_no + 1
                
           
        except Exception as ex:
            custom_logger.error("Error while Scanning {}, Error {} .".format(self.notice_name,ex))
        return {self.notice_name:news_list}