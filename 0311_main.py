# 이 코드에서는 Selector를 사용하여 웹을 크롤링하는 방법에 대해서 알아봅니다.

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import time, random


# Get 방식을 통해 리스폰스를 받아오는 함수
def getDownload(url, param=None, retries = 3):
    resp = None
    try:
        # 서버를 속이기 위해 headers에 "user-agent":"Mozilla/5.0"를 넣음. (Mozilla/5.0 까지만 넣어도 대부분 ok)
        resp = requests.get(url, param, headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"})
        resp.raise_for_status() # 에러를 담고 있음.
    except requests.exceptions.HTTPError as e: # e라는 변수에 에러들을 담을 예정.
        if 500 <= resp.status_code < 600 and retries > 0 : # 500<=resp.status_code < 600이고 최소 0번보다 클때만 반복.
            print("Retries : " + str(retries)) # 현재 몇번 반복되었는지 출력하기 위한 print문
            return getDownload(url, param, retries-1) # 자기 자신을 리턴한 후 retries의 횟수를 줄여줌.
        else: # 만약 500대 에러가 아니고 다른 에러라면 print문 실행
            print(resp.status_code) # 현재 상태를 코드값으로 알려줌. 200:정상, 404:접근금지됨 등등.
            print(resp.reason) # 에러에 대한 상세한 메시지 출력
            print(resp.request.headers) # 에러가 발생했을때의 헤더 출력
    # 아무 문제가 없을경우 resp 객체 반환
    return resp



# Post 방식을 통해 리스폰스를 받아오는 함수
def postDownload(url, param=None, retries = 3):
    resp = None
    try:
        # 주피터 노트북에서는 shift + tab을 누르면 파라미터 설명들이 나옴.
        resp = requests.post(url, param, headers={"user-agent":"Mozilla/5.0"}) # 서버를 속이기 위해 headers에 "user-agent":"Mozilla/5.0"를 넣음. (Mozilla/5.0 까지만 넣어도 대부분 ok)
        resp.raise_for_status() # 에러를 담고 있음.
    except requests.exceptions.HTTPError as e: # e라는 변수에 에러들을 담을 예정.
        if 500 <= resp.status_code < 600 and retries > 0 : # 500<=resp.status_code < 600이고 최소 0번보다 클때만 반복.
            print("Retries : " + str(retries)) # 현재 몇번 반복되었는지 출력하기 위한 print문
            return postDownload(url, param, retries-1) # 자기 자신을 리턴한 후 retries의 횟수를 줄여줌.
        else: # 만약 500대 에러가 아니고 다른 에러라면 print문 실행
            print(resp.status_code) # 현재 상태를 코드값으로 알려줌. 200:정상, 404:접근금지됨 등등.
            print(resp.reason) # 에러에 대한 상세한 메시지 출력
            print(resp.request.headers) # 에러가 발생했을때의 헤더 출력
    # 아무 문제가 없을경우 resp 객체 반환
    return resp

# ----------------------------------------------- selector 사용하기 ----------------------------------------------
# Selector 사용해서 구글로부터 'python' 검색결과의 제목만 10페이지정도 긁어오기
htmlGoogleSearch = getDownload("https://www.google.com/search", {"q":"파이썬"})
domGoogleSearch = BeautifulSoup(htmlGoogleSearch.text, "lxml")
for tag in domGoogleSearch.select(".r h3"): # r 클래스 하위의 모든 h3 태그가 달린 10개를 들고옴.
    print(tag.text)
    print(tag.find_parent()["href"])


# Selector 사용해서 네이버로부터 'python' 검색결과의 제목만 10페이지정도 긁어오기
htmlNaverSearch = getDownload("https://search.naver.com/search.naver", {"query":"파이썬"})
domNaverSearch = BeautifulSoup(htmlNaverSearch.text, "lxml")
for tag in domNaverSearch.select(".blog dt > a"):
    print(tag.text)
    print(tag["href"])


# 네이트에서 'python' 블로그 검색결과의 제목 가져오기
htmlNateSearch = getDownload("https://search.daum.net/nate?thr=sbma&w=tot", {"q":"파이썬"})
domNateSearch = BeautifulSoup(htmlNateSearch.text, "html.parser")
nodeNateSearch = domNateSearch.find_all("", {"id" : "blogColl"}) # 테스트를 위한 임시 print문
# 사이트 검색 부분의 유일한 key-value쌍인 "disp-attr":"IVR"으로 find한 후 find_all을 통해 해당 트리 아래에 있는 모든 "class":"wrap_tit"를 가져옴.
for tag in domNateSearch.select("#blogColl a.f_link_b"):
    print(tag.text)
    print(tag["href"])
# ---------------------------------------------------------------------------------------------------------------



# ----------------------------------------- Crawling -----------------------------------------------------
urlExWebscraping = "http://example.webscraping.com/places/default/index"
urlGoogleSearch = "https://www.google.com/search"
param = {"q":"파이썬"}

# url을 받아서 a 태그가 들어간 링크들만 뽑아내는 함수 (Link extractor)
def getUrls(url, depth): # 3단계정도 깊이를 거쳤으면 그만하라고 함수 인자로 알려줌
    # url는 전체 http로 시작되는 주소이다.
    if depth > 3: # 과도한 탐색을 막기 위해서 탐색 깊이를 지정
        return None
    html = getDownload(url) # 시드 url로부터 a태그만 긁어오기 위해서 getDownload 함수를 통해 HTML 리스폰스를 받아옴.
    if html.status_code != 200: # 에러코드가 200이면 작업을 하지 않음. (None 반환후 함수 종료)
        return None
    dom = BeautifulSoup(html.text, "lxml") # 받아온 HTML 리스폰스를 lmxl 크롤러를 이용해 dom tree로 전환
    urls = [] # 분석이 끝난 url 리스트를 담기 위한 빈 리스트 생성

    for tag in dom.select("a"): # dom tree 내의 모든 a 태그에 대해 반복 수행
        if(tag.has_attr("href")): # href라는 attribute를 가진 tag가 있는지 검사. (href가 없는 사이트도 있기 때문에 외부 사이트를 크롤링할땐 검사를 해 주고 예외처리를 해 주는 것이 좋다.)
            href = tag["href"] # href 키워드를 가진 tag를 href에 넣어줌.
            # print(href)
            if href.startswith("http"): # http로 시작하는 경우에 실행
                urls.append({"url" : href, "depth" : depth + 1}) # 그대로 탐색하도록 append. 이때 너무 과도한 트래픽을 유발하지 않도록 depth를 증가시킴.
            elif href.startswith("/"): # /로 시작하는 경우에 실행
                if len(href) > 2: # 길이가 1인 경우 스킵
                    newUrl = requests.compat.urljoin(url, href) # url뒤에 href를 이어붙임. (urllib.parse의 urljoin보다 requests.compat.urljoin를 쓰는 것이 python 2, 3 호환성 유지에 좋음.)
                    if url != newUrl: # 중복되는 링크 검사 후 목록에서 같은 링크가 나오면 스킵.
                        urls.append({"url" : newUrl, "depth" : depth + 1})
                    elif href.startswith("//"): # //로 시작하는 경우에 실행
                        urls.append({"url" : "http" + href, "depth" : depth + 1})
    print("{0} {1} / {2}".format(">" * depth, url, len(urls))) # 진행도를 위한 구문. ">" 텍스트가 depth 개수만큼 찍히므로 이를 통해 단계를 확인 가능.
    return urls
# --------------------------------------------------------------------------------------------------------------------------------------------




# ------------------------ http://example.webscraping.com/places/default/index 로부터 웹스크롤링 해보기 -------------------------------------------------

queue = getUrls(urlExWebscraping) # while문 돌면서 url를 getUrls함수에 pop해 넣어주기 위한 리스트 (첫페이지에서 가져온 모든 링크를 저장)
visited = [] # 이미 한번 방문한 링크를 관리하는 리스트. 지금은 리스트이지만, 현업에서는 Timestamp와 DB를 활용해서 관리해야 한다.

while queue:
    time.sleep(random.randint(1,3)) # 비주기적으로 랜덤하게 sleep을 걸기 위한 작업. Too many requests 에러를 막기 위한 것

    seed = queue.pop(0)
    links = getUrls(seed)
    visited.append(seed)
    target = [tag for tag in links if tag not in queue and visited] # 만약 tag가 한번이라도 queue와 visited에 안나타났으면 넣으라는 뜻. (queue는 계속 늘어남)

    print("Queue: {0}, Links:{1}".format(len(queue), len(target))) # 현재 큐에 몇개가 남아있고 남은 링크가 무엇인지 출력
    # queue.extend(links) # 주소를 추가해야지, 리스트를 추가하면 안되므로 append대신 extend를 사용
# -------------------------------------------------------------------------------------------------------------------------------------------------




htmlGoogleSearch = getDownload(urlGoogleSearch, param)
domGoogleSearch = BeautifulSoup(htmlGoogleSearch.text, "lxml")
queueGoogleSearch = []

for tag in domGoogleSearch.select(".r a > h3"): # h3 태그 중 r 키워드를 갖는 구문들에 대해 반복문 수행
    queueGoogleSearch.append({"url" : tag.find_parent()["href"], "depth" : 0})

while queueGoogleSearch:
    seedGoogleSearch = queueGoogleSearch.pop(0)
    time.sleep(random.randint(1, 3))
    linksGoogleSearch = getUrls(seedGoogleSearch["url"], seedGoogleSearch["depth"])

    if linksGoogleSearch != None:
        queueGoogleSearch.extend(linksGoogleSearch)

print(len(getUrls(linksGoogleSearch[0])))
