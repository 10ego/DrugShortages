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
            with open('drugshortagescanada.json','r+') as f:
                    f.seek(0,2)
                    f.seek(f.tell()-1,os.SEEK_SET)
                    f.write(',')
                    json.dump(report,f)
                    f.write(']')
        else:
            break

if r.status_code == 200:
    token = r.headers['auth-token']
    data_query()
    while updated_date == today:
        offset+=50
        data_query()
    print("Total of {} reports found today (dated {})".format(counter, today))
else:
    print("Connection HTTP error {}".format(r.status_code))
