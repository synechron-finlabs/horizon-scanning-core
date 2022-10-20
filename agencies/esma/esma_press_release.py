import requests
from datetime import date
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import uuid
from agencies.esma import config


class scanning_notice:

    def __init__(self):
            pass

    def start_scanning(self, page_url):
        page_no = 0
        go_ahead_flag = True        
        press_release_list = []        
        last_scraped_date = None
        
        try:
            while True:
                url = page_url + str(page_no)
                html_content = requests.get(url).text
                soup = BeautifulSoup(html_content, "lxml")

                if go_ahead_flag == False:
                    print("older News")
                    break

                """ 
                if you want braking the loop, uncomment the below line 
                """
                # if page_no > 0:
                #     break

                """
                define the scraping date
                """

                today = datetime.today()
                scrapping_date = today.strftime("%d-%m-%Y")
                record_date = (datetime.strptime(scrapping_date, '%d-%m-%Y') - timedelta(days=1)).date()
                scrapping_date = datetime.strptime(scrapping_date, '%d-%m-%Y').date()

                """
                select all the divs with class
                """
                table = soup.find("table", attrs={"class": "esma-library_table"})
                if table is None:
                    break
                rows = table.tbody.find_all("tr")

                """ 
                Finding the consultation duration date along with Title 
                """
                for tr in rows:
                    if tr is None:
                        continue
                    str_tr = str(tr)
                    if len(str(str_tr.strip())) == 0:
                        continue
                    cols = tr.find_all("td")
                    reference_number = cols[1].text.strip()
                    date = cols[0].text
                    news_date = datetime.strptime(date.split()[0], "%d/%m/%Y").strftime("%d-%m-%Y")
                    press_release_date = datetime.strptime(news_date, '%d-%m-%Y').date()

                    if config.since_start == False:

                        if last_scraped_date is not None:

                            if last_scraped_date.date() > press_release_date:
                                go_ahead_flag=False
                                break

                    title = cols[2].text.strip()
                    print("Title ESMA Press Release Category :", title)
                    types = cols[4].text.strip()

                    """
                    consultation link
                    """
                    link = cols[2].find('a').get('href')
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
                            summary_details = soup_details.find_all("article", attrs={"class":"node node-consultation view-mode-full"})
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
                    section_list = []
                    if len(cols[3].text.strip()) > 0:
                        section = cols[3].text.strip()
                        section_list = section.split(",")
                        for i in range(len(section_list)):
                            section_list[i] = section_list[i].strip().title()
                    elif len(cols[3].text.strip()) == 0:
                        section_list = []

                    

                   

                    """ 
                    Extracting the news category for insuring into the database
                    """
                    press_release_dict = {
                        "id": str(uuid.uuid4().hex),
                        "title": title,
                        "link": link,
                        "published_date": str(press_release_date),
                        "reference_number": reference_number,
                        "details": details,
                        "topic": section_list,
                    }
                    press_release_list.append(press_release_dict)

                page_no = page_no + 1
                break
            
        except Exception as ex:            
            print(ex)
        return  {"esma_press_release":press_release_list}