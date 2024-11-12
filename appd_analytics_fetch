import requests
import json
import time
import urllib


# controller account name
ACCOUNT_NAME = ''
# dynamic key local to dev instance. Create under "configuration"
API_KEY = ''

headers = {'X-Events-API-AccountName': ACCOUNT_NAME,
           'X-Events-API-Key': API_KEY,
           'Content-type': 'application/vnd.appd.events+json;v=1'}

# Last one day of records
end_timestamp = 1000 * int(time.time())
start_timestamp = end_timestamp - 1000 * 1 * 60 * 60

MAX_RESULTS = 20000000
baseurl = 'https://analytics.api.appdynamics.com/events/query?start={}&end={}&limit={}&size={}'.format(
    start_timestamp, end_timestamp, MAX_RESULTS, MAX_RESULTS)
url = baseurl+'&mode=scroll'

# r = requests.post(baseurl, headers=headers,
#                   data=
#                   """[{"query":"SELECT * FROM web_session_records WHERE appkey = '"}]""")
# pp(json.loads(r.content))

scroll_id = None
more_data = True
i = 0
MAX_ITER = 10
while more_data and (i < MAX_ITER):
    if scroll_id is None:
        scroll_url = url
    else:
        scroll_url = url + '&' + urllib.urlencode({'scrollid': scroll_id})
    r = requests.post(scroll_url, headers=headers,
                  data=
                  """[{"query":"SELECT * FROM web_session_records WHERE appkey = ''"}]""")

   
    output_json = json.loads(r.content)[0]
    results = output_json["results"]
    print(results)
    more_data = output_json['moreData']
    #print("{} - moreData - ".format(output_json['moreData']))
    #print("{} - total - ".format(output_json['total']))
    #print("{} - numResults - ".format(len(output_json['results'])))
    if not 'scrollid' in output_json:
        print("End")
        break
    scroll_id = output_json['scrollid']
    print(scroll_id)
    i = i + 1
