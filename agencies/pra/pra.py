
from bs4 import BeautifulSoup
import requests
from datetime import datetime

from agencies.pra import config
import uuid

import importlib
import services.log as log
custom_logger = log.get_logger(__name__)
class scanning_engine:
    def __init__(self):
        self.agency_name="PRA"
    
    def start_scanning(self,no_month):
        custom_logger.info("Scanning started for {}.".format(self.agency_name))
        data=[]

        url_list=config.pra

        try :
            for url in url_list:                
                custom_logger.info("Scanning Started for {}.".format(url))
                module_name = "agencies.{}.{}".format("pra",url)
                # nosemgrep
                module = importlib.import_module(module_name)
                
                obj_module = getattr(module, 'scanning_notice')()
                result=obj_module.start_scanning(url_list[url],no_month)
                
                data.append(result)
                custom_logger.info("Scanning Finished for {}.".format(url))
             
        except Exception as ex:
            custom_logger.error("Error while scanning {} , {}.".format(self.agency_name,ex))
            
            
   
        return {self.agency_name:data}


   