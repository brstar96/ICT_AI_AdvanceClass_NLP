# 이 코드에서는 직접 네이버 뉴스 사이트의 10개 카테고리로부터 각각 60개씩 기사를 긁어옵니다.

"""
1. 뉴스 사이트 (https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001) 으로부터 requests로 긁기
2. '가장 많이 본 뉴스'의 하위 6개 카테고리 찾기 (자바스크립트때문에 눈에 보이는것이 다가 아님에 유의, 소스보기를 통해 확인해야 함.)
3. '가장 많이 본 뉴스'의 각 카테고리별 10개의 뉴스 링크 확인 (상대주소로 들어옴)
4. 뉴스링크 주소를 절대주소로 정규화 (0312_main.py 참고)
5. 각 뉴스 다운로드
6. 뉴스 본문 영역 추출
7. 텍스트만 저장
8. 파일 이름 규칙 : '카테고리-고유번호.txt' -> 고유번호는 뉴스 링크에서 확인 가능. (ex. aid=0010695577)
    get방식 파라미터 중 'aid'를 찾아서 넣으면 됨.
총 6개의 카테고리로부터 60개의 기사 수집.

"""

import requests
from bs4 import BeautifulSoup
import re # 정규식을 사용하기 위한 모듈
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

url_naverNewsMain = "https://news.naver.com/"
param_naverNewsMain = {"id":"category_ranking"}
html_naverNewsMain = getDownload(url_naverNewsMain, param_naverNewsMain)
dom_naverNewsMain = BeautifulSoup(html_naverNewsMain.text, 'html.parser') # DOM tree 구성
NaverHotNewsList = [] # 가장 많이 본 뉴스를 저장하기 위한 빈 리스트
aidNum = [] # 뉴스의 고유번호를 저장하기 위한 빈 리스트
CurrentNewsNum = 0 # 뉴스 카테고리 판단을 위한 현재 기사링크 번호

for tag in dom_naverNewsMain.select('ul.section_list_ranking'): #section_list_ranking 클래스를 갖고 있는 ul태그를 선택
    for tag2 in tag.find_all('a'): # 그 중에서 a태그를 갖고 있는 노드들을 모두 선택
        if tag2.has_attr('href'): # 노드가 href라는 attribute를 갖고 있는 경우 수행
            aidNum.append(re.findall("aid=([0-9]{10})", tag2['href'])) # 정규식을 통해 상대주소 내에 들어 있는 특정 문자열 검색. (href를 갖고 있으면서 'aid=' 뒤에 등장하는 0~9까지 숫자 범위 내에서 10개의 문자를 찾아 aidNum 리스트에 append.)
            NaverHotNewsList.append(requests.compat.urljoin(url_naverNewsMain, tag2['href'])) # 상대주소를 절대주소로 urljoin을 통해 정규화
print("Entire article number : " + str(len(aidNum))) # 전체 60개의 주소를 잘 불러왔는지 확인 (각 카테고리별 10개씩 총 6 카테고리, 60이 출력되면 정상)
# print(NaverHotNewsList) # 절대경로로 변환된 네이버 핫뉴스 목록(60개)

def txtFileIO(CurrentNewsNum, data, categoryname): # 텍스트 파일을 오픈하고 쓴 후 닫는 함수
    f = open("./0314_DownloadedNewstxts/" + categoryname + "-" + str(aidNum[CurrentNewsNum][0]) + ".txt", 'w', encoding='UTF-8') # 파일이름 에러를 피하기 위해 'w'로 열고 'UTF-8'로 인코딩
    f.write(data) # 뉴스기사 txt가 들어 있는 data 리스트를 f 핸들러를 이용해 txt에 write
    f.close() # txt파일 닫기
    print("File has been created! Saved txt path : " + "./0314_DownloadedNewstxts/" + categoryname + "-" + str(aidNum[CurrentNewsNum][0]) + ".txt" )

for title in NaverHotNewsList:
    html_naverHotNews = getDownload(title) # 뉴스 링크 하나를 getDownload 함수에 넣어 반환
    dom_naverHotNews = BeautifulSoup(html_naverHotNews.text, 'html.parser') # DOM tree 생성
    data = dom_naverHotNews.find("", {"id":"right.ranking_contents"}).text # articleBodyContents라는 id를 갖는 태그 검색한 후 text만 data 리스트에 저장
    # 네이버 뉴스기사 문서 내 id가 articleBodyContents -> right.ranking_contents으로 변경되었음

    if CurrentNewsNum < 10:
        txtFileIO(CurrentNewsNum, data, "정치")
    elif 10 <= CurrentNewsNum < 20:
        txtFileIO(CurrentNewsNum, data, "경제")
    elif 20 <= CurrentNewsNum < 30:
        txtFileIO(CurrentNewsNum, data, "사회")
    elif 30 <= CurrentNewsNum < 40:
        txtFileIO(CurrentNewsNum, data, "생활문화")
    elif 40 <= CurrentNewsNum < 50:
        txtFileIO(CurrentNewsNum, data, "세계")
    elif 50 <= CurrentNewsNum < 60:
        txtFileIO(CurrentNewsNum, data, "IT과학")
    else:
        NotImplementedError()
        break
    CurrentNewsNum = CurrentNewsNum + 1