import requests, re, os
from bs4 import BeautifulSoup
from string import punctuation
import pandas as pd

header = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
NaverMovieUrl = 'https://movie.naver.com/movie/point/af/list.nhn?st=mcode&sword=183136&target=after'
ReviewSavingPath = os.path.join(os.getcwd(), 'CrawledNaverNewsReview')

# Params for crawling
PageNo = 1
maxPageNo = 1001
lastReviewNo = 0

# 불용어 처리를 위한 정규식 패턴 정의
def getPatternList():
    patternList = dict()
    pattern = re.compile(r"[%s]{1,}" % re.escape(punctuation))  # punctuation 안의 특수문자가 두번이상 반복되는 모든 문자에 대해 패턴 정의
    patternList["Punctuation"] = pattern

    pattern2 = re.compile(r"\s{2,}")  # 두칸짜리 공백제거
    patternList["Whitespace"] = pattern2

    pattern3 = re.compile(r"([^ㄱ-ㅎㅏ-ㅣ가-힣0-9]+)")  # 한글이 아닌 영어 기호 제거
    patternList["Korean"] = pattern3

    pattern4 = re.compile(r'[A-Za-z-_]{8,}')  # 영어 (대소문자) +\-\_ 제거 (8글자 이상)
    patternList["ElimLongEng"] = pattern4

    pattern5 = re.compile(r'[0-9]')  # 숫자만 제거
    patternList["ElimNumOnly"] = pattern5

    pattern6 = re.compile(r"\s{1,}")  # 한칸짜리 공백제거
    patternList["Whitespace_one"] = pattern6

    return patternList

def getResponse(url, param=None, retries=3):
    resp = requests.get(url, params=param, headers=header)
    resp.raise_for_status()
    return resp

def getContent(file):
    with open(file, encoding="UTF-8") as f:
        content = f.read()
    return content

html = getResponse(NaverMovieUrl + str(PageNo))

# 정상 Response이면서 PageNo < maxPageNo인 동안만 수행
while html.status_code == 200 and PageNo < maxPageNo:
    dom = BeautifulSoup(html.text, "html.parser")
    pointList = dom.select(".list_netizen tbody > tr")

# patternList = getPatternList()
# for _ in ["Korean", "Whitespace", "Punctuation", "ElimLongEng", "Email", "Domain", "ElimRecWord"]:
#     for i in range(len(FileList)):
#         NewsContent[i] = patternList[_].sub(" ", NewsContent[i])
# print(NewsContent[0]) # 불용어 처리가 모두 끝난 뉴스기사 목록

try:  # output_path 디렉토리 존재 여부 확인 후 없으면 디렉토리 생성(makedirs)
    if not (os.path.isdir(ReviewSavingPath)):  # 디렉토리 존재여부 확인
        os.makedirs(os.path.join(ReviewSavingPath))
        print(os.makedirs(os.path.join(ReviewSavingPath)) + "Has been created.")
except OSError as e:
    print("Failed to create directory!!!!!")
    raise


# with open(file, encoding="UTF-8") as txt: