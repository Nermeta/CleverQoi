
from oauthlib.oauth2 import BackendApplicationClient
import requests
import json
import pandas as pd
from requests_oauthlib import OAuth2Session
import os
import var




url = var.Aspireurl
client_id = var.Aspireclient_id
client_secret = var.Aspireclient_secret
OAuthurl = var.AspireOAuthurl



def AspireApiAuth():
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=OAuthurl, client_id=client_id,
            client_secret=client_secret)
    auth = token['access_token']
    return auth




auth = AspireApiAuth()




def Aspirecl():
    requrl = url + "classes"
    data = {}
    
    headers = {'Authorization': 'Bearer %s' % auth}
    response = requests.get(requrl, headers=headers).json()
    df = pd.json_normalize(response['classes'])
    df1 = pd.json_normalize(response['classes'], record_path= "grades", errors='ignore')
    df["grades"] = df1[0]
    df1 = pd.json_normalize(response['classes'], record_path= "subjects", errors='ignore')
    df["subjects"] = df1[0]
    df1 = pd.json_normalize(response['classes'], record_path= "terms", errors='ignore')
    df["terms"] = df1["sourcedId"]
    df1 = pd.json_normalize(response['classes'], record_path= "subjectCodes", errors='ignore')
    df["subjectCodes"] = df1[0]
    df1 = pd.json_normalize(response['classes'], record_path= "periods", errors='ignore')
    df["periods"] = df1[0]
    
    return df




def Aspireco():
    requrl = url + "courses"
    data = {}
    lst = ['subjects']
    
    headers = { 'Authorization': 'Bearer %s' % auth}
    response = requests.get(requrl, headers=headers).json()
    df = pd.json_normalize(response['courses'])
    df1 = pd.json_normalize(response['courses'], record_path= "grades", errors='ignore')
    df["grades"] = df1[0]
    df1 = pd.json_normalize(response['courses'], record_path= "subjects", errors='ignore')
    df["subjects"] = df1[0]
    
    return df



def Aspiredemo():
    requrl = url + "demographics"
    data = {}
    headers = { 'Authorization': 'Bearer %s' % auth}
    response = requests.get(requrl, headers=headers).json()
    df = pd.json_normalize(response['demographics'])
    return df




def Aspireen():
    requrl = url + "enrollments"
    data = {}
    headers = { 'Authorization': 'Bearer %s' % auth}
    response = requests.get(requrl, headers=headers).json()
    df = pd.json_normalize(response['enrollments'])
    return df




def Aspireo():
    requrl = url + "orgs"
    data = {}
    lst = ['children']
    headers = { 'Authorization': 'Bearer %s' % auth}
    response = requests.get(requrl, headers=headers).json()
    df = pd.json_normalize(response['orgs'])
    
    return df   



def Aspireus():
    requrl = url + "users"
    data = {}
    headers = { 'Authorization': 'Bearer %s' % auth}
    response = requests.get(requrl, headers=headers).json()
    df = pd.json_normalize(response['users'])
    df1 = pd.json_normalize(response['users'], record_path= "orgs", errors='ignore')
    df["orgs"] = df1["sourcedId"]
    df1 = pd.json_normalize(response['users'], record_path= "grades", errors='ignore')
    df["grades"] = df1[0]
   
    df1 = pd.json_normalize(response['users'], record_path = 'userIds')
    df['metadata.stateId'] = df1['identifier']
    return df

def Aspireas():
    requrl = url + "academicSessions"
    data = {}
    headers = { 'Authorization': 'Bearer %s' % auth}
    response = requests.get(requrl, headers=headers).json()
    df = pd.json_normalize(response['academicSessions'])
    return df

