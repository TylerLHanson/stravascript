import requests
import urllib3
requests.packages.urllib3.disable_warnings()
import pandas as pd 
from pandas.io.json import json_normalize


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
my_activities = requests.get(
    "https://www.strava.com/api/v3/athlete/activities",
    headers={'Authorization': 'Bearer ' + access_token},
    params={'per_page': 200, 'page': 1}
).json()

# see activities list
print('See activities list:')
print(my_activities)
# my_activities_df = json_normalize(my_activities)
# print(my_activities_df)
# print(my_activities_df.columns)
# print(my_activities_df.sport_type)


comments = []
for x in my_activities:
    if x['sport_type'] == 'Surfing':
        url = "https://www.strava.com/api/v3/activities/{}/comments".format(x['id'])
        activity_comments = requests.get(url, headers={'Authorization': 'Bearer ' + access_token}).json()
        # unpack extra layer (list of lists of dictionaries -> list of dictionaries) upfront
        for d in activity_comments:
            comments.append(d)

print(' ')
print('See comments list:')
print(comments)
