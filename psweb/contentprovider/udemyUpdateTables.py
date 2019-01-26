import psycopg2
import json
import ssl
from http.client import HTTPSConnection
from base64 import b64encode
#This sets up the https connection
c = HTTPSConnection("www.udemy.com", context=ssl._create_unverified_context())
#we need to base 64 encode it 
#and then decode it to acsii as python 3 stores it as a byte string
userAndPass = b64encode(b"GpxNVedkBslJE6CTga0f56iRG4vzzmYU24gzH0g5:FGMx5x8Vjr7LyBokikzIT9t4uFSSa30HMhMGcEHZBy38FV2snjwew0l9o3ctugs1KRcIvBQyZDidYKuMKrWUGHCA0qRNYMvFg859QhpatbpBPZW3QNAeJzpHBAYNkBoy").decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  userAndPass }
#then connect
c.request('GET', '/api-2.0/courses', headers=headers)
#get the response back
res = c.getresponse()
# at this point you could check the status etc
# this gets the page text
data = res.read()  


conn = psycopg2.connect(database='purpleskillsdb', user='psroot', password='pswhatever1', host='127.0.0.1', port='')

data = json.loads(data)
results = data['results']
# data here is a list of dicts
#data = res.json()['data']

print (data)
cur = conn.cursor()

fields = [
     'id',
     'title'
    # 'archive_time'
]

for item in results:
    my_data = {field: item[field] for field in fields}
    print (my_data)
    #cur.execute("INSERT INTO contentprovider_udemycourse VALUES \'(%s)\'", (json.dumps(my_data),))
    cur.execute("INSERT INTO contentprovider_udemycourse (id,title) VALUES (%s, %s)", (my_data['id'],my_data['title']))


# commit changes
conn.commit()
# Close the connection
conn.close()
