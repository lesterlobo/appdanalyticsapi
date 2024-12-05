import requests
import json
import time
import urllib
from datetime import datetime

def generate_epoch(delta):
    """Generates the current epoch timestamp."""
    return int((time.time()- delta) * 1000)

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
#                   """[{"query":"SELECT * FROM web_session_records WHERE appkey = 'AD-AAB-ADB-HMK"}]""")
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
                  """[{"query":"SELECT sessionguid, browserRecords, browser, deviceos, userdata.email, userdata.fullName, userdata.organizationId FROM web_session_records WHERE appkey = ''"}]""")

    #print(json.loads(r.content))
    output_json = json.loads(r.content)[0]
    
    results = output_json["results"]
    print("Session GUID", "Browser Page", "StartTime", "EndTime", "PageType")
    for result in results:
        sessionGuid = result[0]
        browserRecords = result[1]
        browser = result[2]
        deviceOS = result[3]
        email = result[4]
        fullName = result[5]
        orgid = result[6]

        for record in browserRecords:
            page = record[8]
            pageType = record[9]
            endTime = datetime.fromtimestamp(record[1]/1000)
            startTime = datetime.fromtimestamp(record[2]/1000)
            print(browser + " ," + deviceOS + " ," + (email or " ")+ " ," + (fullName or " ") + " ," + (orgid or " ") + " ," + str(startTime) + ", " + str(endTime) + ", " + page + ", " + pageType)
        print("#################")
    
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
