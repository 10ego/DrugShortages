import requests
import json
from datetime import datetime

url = "https://www.drugshortagescanada.ca/api/v1"
uid = 'LOGIN'
pwd = 'PASSWORD'
offset = 0
counter = 0
today = datetime.today().strftime('%Y-%m-%d')
r = requests.post(url+'/login',data={'email':uid,'password':pwd})


def data_query():
    global counter
    global updated_date
    searchparam = {
        'orderby':'updated_date',
        'order':'desc',
        'limit':50,
        'offset':offset
        }

    r = requests.get(url+'/search', headers={'auth-token':token}, params=searchparam)
    data = json.loads(r.text)
    data = data['data']
    
    for report in data:
        
        updated_date = datetime.strptime(report['updated_date'],'%Y-%m-%dT%H:%M:%S%z')
        updated_date = datetime.strftime(updated_date, '%Y-%m-%d')
        if updated_date == today:
            counter+=1
            with open('drugshortagescanada.json','a') as f:
                    json.dump(report,f)
                    f.write(',')
        else:
            print("Total of {} reports found today (dated {})".format(counter, today))
            break

if r.status_code == 200:
    token = r.headers['auth-token']
    data_query()
    while updated_date == today:
        offset+=50
        data_query()

else:
    print("Connection HTTP error {}".format(r.status_code))
