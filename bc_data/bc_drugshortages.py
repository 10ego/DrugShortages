import requests
import datetime
import json

c_url = "http://www.health.gov.bc.ca/pharmacare/drug-shortage/drugshortageupdate.xls"
r_url = "http://www.health.gov.bc.ca/pharmacare/drug-shortage/resolvedshortages.xls"

def data_miner(url, filename):
	r = requests.get(url)
	if r.status_code == 200:
		print('Connection OK!')
		f_size = r.headers['Content-Length']
		etag = r.headers['ETag'][1:-1] #Raw ETag datais wrapped in ""
		date = r.headers['Date']
		f_date = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
		f_date = f_date.strftime('%Y-%m-%d')
		
		new_log={}
		new_log['File Size'] = f_size
		new_log['ETag'] = etag
		new_log['Date'] = f_date
		print(new_log)
		with open(filename+'_metadata.json', 'r+') as l:
			log = json.load(l)
			if  log == new_log:
				print("No new data to download..")
			else:
				with open(filename+f_date+'.xls','w+b') as datafile:
					datafile.write(r.content)
					print("New data downloaded for {}({})".format(filename, f_date))
				
				l.seek(0)
				json.dump(new_log, l)
				l.truncate()
							
	else:
		print('Connection Error: {}'.format(r.status_code))
	
data_miner(c_url, 'bc_current')
data_miner(r_url, 'bc_resolved')
