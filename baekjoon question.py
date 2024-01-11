import json
import requests
import csv
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pandas as pd
import os
import time

for i in range(1, 31065, 1):
    num = i
    url = f'https://solved.ac/api/v3/problem/show?problemId={i}'
    try:
        result = requests.get(url)
        response_json = json.loads(result.content)
        

        problemId = response_json['problemId']
        
        titleKo = response_json['titleKo']
        acceptedUserCount = response_json['acceptedUserCount']
        level = response_json['level']
        tags = response_json['tags']
        if tags == '':
                tags_key.append('')
                tags_bojTagId.append('')
                break;
        
        tags_key = []
        tags_bojTagId = []
        for k in tags:
            if tags == '':
                tags_key.append(' ')
                tags_bojTagId.append(' ')
                break;
            tags_key.append(k['key'])
            tags_bojTagId.append(k['bojTagId'])

        # 6개
        df = pd.DataFrame({'problemId':[problemId],'titleKo':[titleKo], 'acceptedUserCount':[acceptedUserCount],
                       'level':[level],'tags_key':[tags_key],'tags_bojTagId':[tags_bojTagId]})
        df.to_csv('problemList.csv', header=False, mode='a', encoding='cp949')
        # header=False
        print(df)
        if num%100==0:
            time.sleep(20)
    except Exception as e:
        print(e)
        print(f"Error with {i}")
        time.sleep(0.5)
        i = i-1
        pass
        
    
