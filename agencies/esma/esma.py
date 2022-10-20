from logging import exception
import requests
from datetime import date
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import uuid
from agencies.esma import config
import importlib



class scanning_engine:
    def __init__(self):
        pass


    #temprory function only for demo
    def start_scanning(self,no_month):
        print("Scanning started for ESMA")
        
        data=[]

        url_list=config.esma

        try :
            for url in url_list:
                
                module_name = "agencies.{}.{}".format("esma",url)
                module = importlib.import_module(module_name)
                
                obj_module = getattr(module, 'scanning_notice')()
                result=obj_module.start_scanning(url_list[url])
                
                data.append(result)
                print("Done {}".format(url))
             
        except exception as ex:
            
            print(ex)
            
        #print(data)
        return {"esma":data}

