
from bs4 import BeautifulSoup
import requests
from datetime import datetime

from agencies.pra import config
import uuid

import importlib

class scanning_engine:
    def __init__(self):
        pass
    #temprory function only for demo
    def start_scanning(self,no_month):
        print("Scanning started for PRA")
        data=[]

        url_list=config.pra

        try :
            for url in url_list:                
                
                module_name = "agencies.{}.{}".format("pra",url)
                module = importlib.import_module(module_name)
                
                obj_module = getattr(module, 'scanning_notice')()
                result=obj_module.start_scanning(url_list[url],no_month)
                
                data.append(result)
                print("Done {}".format(url))
             
        except exception as ex:
            
            print(ex)
            
        #print(data)
        return {"pra":data}


   