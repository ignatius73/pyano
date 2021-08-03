import os
import csv
import json
import requests
import pandas as pd
from dotenv import load_dotenv


class Merge_Csv:
    files = []
    data = {}
    
    def __init__(self, filea, fileb):

        self.files.append(filea)
        self.files.append(fileb)

        #print(self.files)

      

    

    def load_data(self):
        load_dotenv()

        '''I was infered from the documentation what type of object responds the endpoint,
        i get a json formatted object formated as:
            {
                'status_code':0,
                'data':[
                    { 'user_id': 'value'.
                       'email': 'value',
                       'first_name':'value',
                       'last_name': 'value'
                    }
                ]
            }

        


        '''
        r = requests.post('sandbox.tinypass.com/publisher/users/get', data={ "aid": os.getenv('AID'), "api_token":os.getenv('api')})
        
        
       
        
        if r.status_code == 200:
            resp = r.json()

            if resp['status_code'] == 0:
                self.data = r.json()
            
        else:
            #Raise and exception
            return(r.raise_for_status())
        

    #Merge two Csv, return a new Csv named merged.csv
    def merge_data(self):

        fieldnames = []

        for filename in self.files:
            with open(filename) as File:
                
                reader = csv.reader(File, delimiter=",")
                headers = next(reader)
                print(headers)

                for h in headers:
                    if h not in fieldnames:
                        fieldnames.append(h)
                
        with open('merged.csv', 'w') as newFile:
            writer = csv.DictWriter(newFile, fieldnames= fieldnames)
            for filename in self.files:
                with open(filename,'r') as File:
                    reader = csv.DictReader(File)
                    for line in reader:
                        if 'email' in line.keys():
                            
                            for user in self.data['data']:
                                if user['email'] == line['email']:
                                    print(user['email'])
                                    
                                    if line['user_id'] != user['user_id']:
                                        line['user_id'] = user['user_id']
                                        break
                                    
                            

                        else:
                            for user in self.data['data']:
                                if line['first_name'] == user['first_name'] and line['last_name'] == user['last_name']:
                                    if line['user_id'] != user['user_id']:
                                        line['user_id'] = user['user_id']
                                        break
                                                                    
                        
                        writer.writerow(line)
                        #print(line)
    
#Call to the construct with two csv files, hardcoded       
a = Merge_Csv('filea.csv','fileb.csv')
a.load_data()
a.merge_data()