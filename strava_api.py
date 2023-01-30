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

my_activities_df = json_normalize(my_activities)


comments = []
for x in my_activities:
    if x['sport_type'] == 'Surfing':
        url = "https://www.strava.com/api/v3/activities/{}/comments".format(x['id'])
        activity_comments = requests.get(url, headers={'Authorization': 'Bearer ' + access_token}).json()
        # unpack extra layer (list of lists of dictionaries -> list of dictionaries) upfront
        for d in activity_comments:
            # use dict comprehension to grab only the necessary data
            data = {k:v for (k,v) in d.items() if k=='activity_id' or k=='text'}
            # data = {}
            # for k,v in d.items():
            #     if k=='activity_id' or k=='text':
            #         data[k] = v
            comments.append(data)


my_comments_df = json_normalize(comments)


def read_comments(row):
    if row['text'].isdigit():
        return 'wave_count'
    elif 'ft.' in row['text']:
        return 'surf_report'
    else:
        return 'surf_spot'
    
my_comments_df['comment_category'] = my_comments_df.apply(lambda  row: read_comments(row), axis=1)
my_comments_pivoted = pd.pivot(my_comments_df, index="activity_id", columns="comment_category", values="text")
surf_activity_data = my_comments_pivoted.merge(my_activities_df, left_index=True, right_on="id")
surf_activity_data = surf_activity_data.reset_index(drop=True)
print(surf_activity_data)
# test 2
