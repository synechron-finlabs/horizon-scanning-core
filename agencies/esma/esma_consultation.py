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
        self.notice_name= "esma_consultation"
        
    def start_scanning(self, page_url,no_month):
        page_no = 0
        go_ahead_flag = True
        today = datetime.today()
        last_scan_date=obj_com.extract_month_date(no_month)
        consultation_list = []
        is_main_break = False
        custom_logger.info("Scanning {}.".format(self.notice_name))
       
        try:
            while True:
                if is_main_break == True:
                    # print("older News")
                    break
                url = page_url + str(page_no)
                
                html_content = requests.get(url).text
                soup = BeautifulSoup(html_content, "lxml")
                
                """ 
                if you want braking the loop, uncomment the below line 
                """
              
                """
                define the scraping date
                """
                today = datetime.today()
                scrapping_date = today.strftime("%d-%m-%Y")
                record_date = (datetime.strptime(
                    scrapping_date, '%d-%m-%Y') - timedelta(days=1)).date()
                scrapping_date = datetime.strptime(
                    scrapping_date, '%d-%m-%Y').date()


                """
                select all the divs with class
                """
                contents = soup.find_all("div", attrs={"class": "view-content"})
                if contents is None:
                    break
                if len(contents) == 0:
                    break
                html = str(contents[0])
                soup2 = BeautifulSoup(html, 'html.parser')
                table = soup2.find("table", attrs={"id": "footable"})
                rows = table.tbody.find_all("tr", attrs={"class": "odd"})
                rows += table.tbody.find_all("tr", attrs={"class": "even"})

                """ 
                Finding the consultation duration date along with Title 
                """
                for tr in rows:
                    cols = tr.findAll('td')
                    
                    date = cols[0].text
                    start_date = datetime.strptime(
                        date.split()[1], "%d/%m/%Y").strftime("%d-%m-%Y")
                    end_date = datetime.strptime(
                        date.split()[3], "%d/%m/%Y").strftime("%d-%m-%Y")
                    start_date = datetime.strptime(
                        start_date, '%d-%m-%Y').date()
                    end_date = datetime.strptime(end_date, '%d-%m-%Y').date()
                    
                    if str(start_date) < last_scan_date:
                        is_main_break=True
                        break


                    title = cols[1].text.strip()

                    """
                    consultation link
                    """
                    link = config.esma_url + \
                        cols[1].find('a').get('href')
                    if link is None:
                        link = ""

                    """ 
                    Extract the news content from news link
                    """
                    details = ""
                    try:
                        if len(link):
                            news_content = requests.get(link, timeout=15).text
                            soup_details = BeautifulSoup(news_content, "lxml")
                            summary_details = soup_details.find_all(
                                "article", attrs={"class": "node node-consultation view-mode-full"})
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
                    section 
                    """
                    section = ""
                    if len(cols[2].text.strip()) > 0:
                        section = cols[2].text.strip()
                    elif len(cols[2].text.strip()) == 0:
                        section = ""
                    section_list = section.split(",")
                    section_list = [x.strip().title() for x in section_list]


                    """
                    Summary of the consultation
                    """
                    summary = cols[5].text.strip()
                    if summary is not None:
                        summary = summary.strip()
                    else:
                        summary = ""

                    """ 
                    Extracting the news category for insuring into the database
                    """
                    consultation_dict = {
                        "id": str(uuid.uuid4().hex),
                        "title": title,
                        "link": link,
                        "summary": summary,
                        "start_date": str(start_date),
                        "end_date": str(end_date),
                        "details": details,
                        "topics": section_list,
                    }
                    consultation_list.append(consultation_dict)
                    

                page_no = page_no + 1
                
        except Exception as ex:
            
            custom_logger.error("Error while Scanning {}, Error {} .".format(self.notice_name,ex))
        return {self.notice_name:consultation_list}
