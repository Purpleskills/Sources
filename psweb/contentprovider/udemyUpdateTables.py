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
c.request('GET', '/api-2.0/courses?page_size=100', headers=headers)
#get the response back
res = c.getresponse()
# at this point you could check the status etc
# this gets the page text
data = res.read()  


conn = psycopg2.connect(database='purpleskillsdb', user='psroot', password='pswhatever1', host='127.0.0.1', port='')

data = json.loads(data)
results = data['results']
#print (results)
# data here is a list of dicts
udemyPrefix = "https://www.udemy.com"
#print (data)
cur = conn.cursor()

fields = [
     'id',
     'title',
     'url'
]


cur.execute("INSERT INTO learn_courseprovider (name, status, logo) SELECT %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM learn_courseprovider where name = \'Udemy\') ", ("Udemy","0","https://www.udemy.com/staticx/udemy/images/v6/mstile-144x144.png"))

for item in results:
    my_data = {field: item[field] for field in fields}
    cur.execute("INSERT INTO contentprovider_udemycourse (id,title,url) VALUES (%s, %s, %s) ON CONFLICT(id) DO NOTHING ", (my_data['id'],my_data['title'],udemyPrefix+my_data['url']))
    cur.execute("INSERT INTO learn_course (title,url, provider_id) SELECT  %s, %s, ID FROM learn_courseprovider where name = \'Udemy\' AND  NOT EXISTS (SELECT 1 FROM learn_course where title=%s)", (my_data['title'],udemyPrefix+my_data['url'], my_data['title'])) 




# commit changes
conn.commit()
# Close the connection
conn.close()
