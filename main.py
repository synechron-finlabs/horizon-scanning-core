
import argparse
import importlib
import os
import json


def start():
    """
    start function
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--agency", type=str, default="")
    ap.add_argument("-o", "--output", type=str, default="agnecy.json")
    ap.add_argument("-m", "--month", type=str, default=1)
    args = ap.parse_args()

    #Checking for agnecy is passing or not
    if args.agency:
        agency=args.agency
        no_month=1

        try :
            agency_list=[]
            #If all agency is passing by user
            if agency.lower()=="all":
                dir_list = os.listdir('agencies')
                agency_list.extend(dir_list)

            else:
                agency_list.append(agency)

            results=[]
            
            if args.month:
                 
                no_month=args.month
                if isinstance(no_month, str):

                    if no_month.isdigit():
                        no_month=int(no_month)
                    else:
                        assert("Please provide month in integer")
            
            for item in agency_list:
                item=item.lower()
                module_name = "agencies.{}.{}".format(item,item)
                module = importlib.import_module(module_name)
                obj_module = getattr(module, 'scanning_engine')()
                results.append(obj_module.start_scanning(no_month))

            if args.output:
                out_file_name = args.output.split(".")[0]
                out_file_name = out_file_name + ".json"
                with open(out_file_name, 'w') as f:
                    f.write(json.dumps(results))

            #print(results)
        except Exception as ex:
            print(ex)
    else:
        assert("Please provide agency name")
        
if __name__ == "__main__":
    start()
