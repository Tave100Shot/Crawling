from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import tqdm
import re
import requests

# 드라이버 옵션 설정 (창 안띄우기)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)

info = ["id", "tier", "rank","rightCnt", "wrongCnt", "time out", "memory exceed", "print exceed",
        "runTime error", "compile error", "solvedProblemList", "triedNotsolvedList"]
table_data = []
data = pd.read_csv("ranklist.csv", low_memory=False)
df = data.id[80001:100001]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}

num=0
# ranklist.csv 파일이 없으면 생성
try:
    data1 = pd.read_csv("userList.csv")
except:
    data1 = pd.DataFrame(columns=info)
    data1.to_csv("userList.csv", index=False, encoding="utf-8-sig")
num = 0
for i in tqdm(df):
    a = 0
    print(i)
    url = ("https://www.acmicpc.net/user/" + str(i))
    result = requests.get(url, headers=headers)
 #   driver.implicitly_wait(10)
 #   html = result.page_source
    soup = BeautifulSoup(result.content, "html.parser")
    try:
        img_tag = soup.find('img', {'class': 'solvedac-tier'})
        if img_tag and 'src' in img_tag.attrs:
            # 이미지 URL에서 숫자 추출
            match = re.search(r'/tier/(\d+)\.svg', img_tag['src'])
            if match:
                number = match.group(1)
                print("숫자 추출함:", number)
            else:
                print("매치된 거 없음")
        else:
            print("Image tag 못찾음")

        table1 = soup.find("table", {"id": "statics"})
        trs1 = []

        table1_tag = ['등수', '맞았습니다', '틀렸습니다', '시간 초과', '메모리 초과', '출력 초과',
                      '런타임 에러', '컴파일 에러']
        noTable1_tag = ['맞은 문제', '맞았지만 만점을 받지 못한 문제', '시도했지만 맞지 못한 문제',
                        '제출', '대회 우승', '대회 준우승', '문제집', '만든 문제', '번역한 문제', '오타를 찾음',
                        '잘못된 데이터를 찾음', '잘못된 조건을 찾음', '데이터를 추가', '빠진 조건을 찾음',
                        '잘못된 번역을 찾음', '데이터를 만듦', '스페셜 저지를 만듦', '내용을 추가', '문제를 검수',
                        '출력 형식', '학교/회사', 'Topcoder', 'Codeforces', 'Atcoder']
        # print(table1.find_all('tr'))
        a=0
        for tr_tag in table1.find_all('tr'):  # tr을 포함하는 것들
            th_tags = tr_tag.find_all('th')  # 그것 중에 th를 포함하는 것들
            row_data = [th.get_text(strip=True) for th in table1.find_all('th')] #row data로 text 변환
            row_d = [th.get_text(strip=True) for th in th_tags] # 하나만 포함
            if table1_tag[a] in row_data:
                td_tags = tr_tag.find_all('td')
                row_data1 = [td.get_text(strip=True) for td in td_tags]
                trs1.append(row_data1)
                print(row_data1)
            elif table1_tag[a] not in row_data:
                print('none')
                trs1.append('none')
            a+=1
            if a == len(table1_tag):
                break
                    
                
        #print(trs1)

        all_panel_elements = soup.select('.panel.panel-default')

        table2 = all_panel_elements[1]
        trs2 = [a.text for a in table2.find_all("a")]


        for t in all_panel_elements:
            title_tag = t.find("h3", {"class": "panel-title"})
            
            table3 = []
            if "시도했지만 맞지 못한 문제" in title_tag:
                table3 = t
                trs3 = [a.text for a in table3.find_all("a")]
                if trs3 == '':
                    trs3 = ' '
        table_data = []
        table_data.append(i)
        table_data.append(number)
        for k in trs1:
            table_data.append(k)
        table_data.append(trs2)
        table_data.append(trs3)
        
        print(num)
        num+=1
        time.sleep(1)
        df = pd.DataFrame([table_data], columns=info)
        print(df)
        df.to_csv("userList.csv", index=False, encoding="utf-8-sig", mode='a', header=False)
    except Exception as e:
        print(e)
        print(f"error with {i}")
        pass

driver.close()
