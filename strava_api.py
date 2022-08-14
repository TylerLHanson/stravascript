import requests
import urllib3
requests.packages.urllib3.disable_warnings()
import pandas as pd 
from pandas.io.json import json_normalize
from tqdm import tqdm


# post request with your client info and refresh token to obtain updated access token (access tokens expire every 6 hours)
# Note you need to use a 'read_all' scope refresh token (vs. just 'read') which is not provided by default
# more info here: https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde
my_creds = {
    'client_id': "xxxx",
    'client_secret': 'xxxx',
    'refresh_token': 'xxxx',
    'grant_type': "refresh_token",
    'f': 'json'
}
access_token = requests.post("https://www.strava.com/oauth/token", 
    data=my_creds,
    verify=False
).json()['access_token']


# store the data passed back from get request in mydata object
mydata = requests.get(
    "https://www.strava.com/api/v3/athlete/activities",
    headers={'Authorization': 'Bearer ' + access_token},
    params={'per_page': 200, 'page': 1}
).json()


activities = json_normalize(mydata)
print(activities)
print(activities.columns)
print(activities.sport_type)

# search for comments
examplecomments = requests.get(
    "https://www.strava.com/api/v3/activities/xxxx/comments",
    headers={'Authorization': 'Bearer ' + access_token},
    params={'per_page': 200, 'page': 1}
).json()

print(examplecomments)


activities['comments'] = None
for a, b in tqdm(activities.iterrows(), total=activities.shape[0]):
    get_comments_url = "https://www.strava.com/api/v3/activities/{}/comments".format(b['id'])
    print(get_comments_url)
    if b['type'] == 'Surfing':
        print(b)
