import requests
import json

url = "https://www.drugshortagescanada.ca/api/v1"
uid = 'LOGIN'
pwd = 'PWD'

r = requests.post(url+'/login',data={'email':uid,'password':pwd})

offset = 0
page = 0
total_pages = 0

#RUN AUTH BEFORE REQUESTING FOR TOKEN
r = requests.post(url+'/login',data={'email':uid,'password':pwd})

def data_query():
    global page
    global total_pages
    global offset
    onetime_param = {
        'orderby':'id'
        'order':'asc',
        'limit':100,
        'offset':offset
    }
    r = requests.get(url+'/search', headers={'auth-token':token}, params=onetime_param)
    if r.status_code == 200:
        data = json.loads(r.text)
        page = data['page']
        total_pages = data['total_pages']
		offset+=100
        with open('all_shortages_page_{}.json'.format(page,'w') as f:
            json.dump(data['data'], f)
        print("Data dumped successfully for page {} of {}".format(page, total_pages))
    elif r.status_code == 429:
        with open('failed_request.txt', 'w') as fa:
            fa.write('Requested overloaded on page {} of {}'.format(page+1, total_pages))
			offset+=data['total'] #in case it get stuck in infinite loop of errors
    else:
        with open('failed_request.txt', 'w') as fa:
            fa.write('Request failed due to error {}'.format(r.status_code))
			offset+=data['total'] #in case it get stuck in infinite loop of errors

if r.status_code == 200:
    token = r.headers['auth-token']
    data_query()
    while data['page'] <= data['total_pages']:
        data_query()

else:
    print("Failed to get token due to HTTP connection error {}".format(r.status_code))
