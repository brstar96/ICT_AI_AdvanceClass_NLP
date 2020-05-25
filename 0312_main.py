# 이 코드에서는 BeautifulSoup을 이용해 정적 컨텐츠(ex. 뽐뿌 사이트)를 긁어오는 방법에 대해 알아봅니다.

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time
import random

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}

def getDownload(url, param=None, retries=3):
    resp = None
    try:
        resp = requests.get(url, params=param, headers=header)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if 500 <= resp.status_code < 600 and retries > 0:
            print('Retries : {0}'.format(retries))
            return getDownload(url, param, retries - 1)
        else:
            print(resp.status_code)
            print(resp.reason)
            print(resp.request.headers)

    return resp


# ------------------------ 검색, 선택, 이미지 크롤링하기 -------------------------------------
url = 'http://example.webscraping.com/places/default/index'
html = getDownload(url)
dom = BeautifulSoup(html.text,'lxml')

# 검색하기 (Find)
results = dom.find('', {'id':'results'})
for tag in results.find_all('a'):
    print(tag.text)

# 선택하기 (Select)
for tag in dom.select('#results a'):
    print(tag.text)

# 이미지 긁기
for tag in dom.select('#results a > img'):
    if tag.has_attr('src'):
        print(requests.compat.urljoin(url, tag['src']))

html = getDownload('http://example.webscraping.com/places/static/images/flags/af.png')
html.headers['Content-Type'] # 'image/png'
# ---------------------------------------------------------------------------------------------



# ------------------------코드가 위치한 경로에 이미지 생성하고 다운받아 저장하기-------------------------------
imgSrc = 'http://example.webscraping.com/places/static/images/flags/af.png'

imgName = imgSrc.split('/')[-1]
with open(imgName, 'wb') as f:
    f.write(html.content)


for tag in dom.select('#results a > img'):
    if tag.has_attr('src'):
        src = requests.compat.urljoin(url, tag['src'])

        time.sleep(random.randint(1, 3)) # Too many requests에러 방지를 위한 구문

        html = getDownload(src)
        if html.headers['Content-Type'].split('/')[0] == 'image':
            with open('./0312_downloadedimgs/' + src.split('/')[-1], 'wb') as f:
                f.write(html.content)
# -------------------------------------------------------------------------------------------------------------


# ---------------------------------------- 뽐뿌 사이트 긁어오기 -----------------------------------------------
url2 = 'https://www.ppomppu.co.kr/zboard/zboard.php'
param2 = {'id': 'ppomppu'}
html2 = getDownload(url2, param2)
req = Request(url2, headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}) # 리스폰스를 보내기 위한 req 객체 생성
resp = urlopen(req) # HTML 리스폰스 객체 생성


encoding = html2.headers['Content-Type'].split('=')[-1]
# html2.content.decode(encoding, 'ignore')
dom2 = BeautifulSoup(html2.text, 'lxml')
print(len(dom2.find_all('', {'class':'list_title'})))

dom2 = BeautifulSoup(html2.text, 'lxml')
print(len(dom2.select('.list_title')))

dom2 = BeautifulSoup(html2.text, 'html.parser')
print(len(dom2.find_all('', {'class':'list_title'})))

dom2 = BeautifulSoup(html2.text, 'html.parser')
print(len(dom2.select('.list_title')))

for tag in dom2.select('.list_title'):
    print(tag.text)


# 상대주소로 접근하기 (사이트 내 주소)
for tag in dom2.select('.list_title'):
    if tag.find_parent().has_attr('href'):
        print(tag.find_parent()['href'])

# 절대주소로 접근하기
for tag in dom2.select('.list_title'):
    if tag.find_parent().has_attr('href'):
        link = requests.compat.urljoin(url2, tag.find_parent()['href'])
        print(link)

# 썸네일 이미지들의 리스트 받기
for tag in dom2.select('img.thumb_border'):
    print(tag['src'])

# 작성시간(?) 받아오기
for tag in dom2.select('td.eng.list_vspace'):
    if tag.has_attr('title'):
        print(tag['title'])


# 광고글 링크, 링크타이틀, 작성시간, 조회수 받아오기
for tag in dom2.select('.list1'):
    tdList = tag.find_all('td', recursive=False)  # row에 있는 td 수
    #     print(len(tdList))
    #     print(tdList[3].text.strip()) 밑에처럼 분석
    print('http:' + tdList[3].find('img')['src'])
    salesComplete = tdList[3].select_one('.list_title')
    if salesComplete != None:  # 판매 종료시 None 값이 나와서 추가 시켜줬습니다.
        print(tdList[3].select_one('.list_title').text)

    # print(tdList[4].text.strip())
    print(tdList[4]['title'])

    # print(tdList[5].text.strip())
    print(tdList[5].text.split('-')[0].strip())

    # print(tdList[6].text.strip())
    print(tdList[6].text.strip(), end='\n\n')
# --------------------------------------------------------------------------------------------------------------



# ------------------------------------ 뽐뿌 사이트의 자유게시판 글 긁어오기 -----------------------------------------------
url2 = 'https://www.ppomppu.co.kr/zboard/zboard.php'
param2 = {'id': 'freeboard'}
html2 = getDownload(url2, param2)
dom2 = BeautifulSoup(html2.text, 'html.parser')
links = [] # 빈 리스트 생성


# 자유게시판 리스트를 주소와 함께 받아오기
for tag in dom2.select('font.list_title'): # 폰트 클래스 중 list_title가 달린 태그 선택
    print(tag.text) # font 클래스 중 list_title가 달린 태그의 text를 출력
    print(tag.find_parent()['href']) # 해당 글의 상대주소 출력
    print(requests.compat.urljoin(url2, tag.find_parent()['href'])) # 해당 글의 절대주소 출력
    links.append(requests.compat.urljoin(url2, tag.find_parent()['href']))


# 최신 게시글(1개)의 내용 받아오기
for link in links:
    html2 = getDownload(link)
    dom2 = BeautifulSoup(html2.text, 'html.parser')
    print('내용 : ' + dom2.select_one('table.pic_bg td.han').text.strip())
    #     for tag in dom2.select('td,han'):
    #         print(tag.text)
    break


# 댓글 긁어오기
for tag in dom2.select('#quote div.han'):
    print('댓글 : ' + tag.text.strip(), end='\n\n')


# 내용 + 댓글 한번에 긁어오기
for link in links:
    html2 = getDownload(link)
    dom2 = BeautifulSoup(html2.text ,'html.parser')
    print('내용 : ' + dom2.select_one('table.pic_bg td.han').text.strip(), end='\n\n')

    reply = dom2.select('#quote div.han')

    if len(reply) > 0:
        for tag in reply:
            print('댓글 : ' + tag.text.strip(), end='\n\n')
    print('=======================================')
# -------------------------------------------------------------------------------------------------------------------------