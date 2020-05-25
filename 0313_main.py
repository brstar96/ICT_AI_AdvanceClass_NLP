# 이 코드에서는 셀레니움 모듈을 이용해 동적 컨텐츠(ex. 네이버 스팸메일함)를 긁어오는 방법에 대해 알아봅니다.

import requests
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException # 셀레니움에서 발생된 에러들을 관리
from selenium.webdriver.support.ui import WebDriverWait

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


# ----------------------------- 셀레니움 모듈을 활용해 렌더링이 끝난 브라우져 결과물로 DOM트리를 만들고 내용 가져오기 ----------------------------------------
url = "http://example.webscraping.com/places/default/search"
url2 = "http://example.webscraping.com/places/ajax/search.json"
header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
param = {"search_term" :" korea"}
param2 = {"search_term" :" korea",
          "page_size" : 10,
          "page" : 0}
html = getDownload(url2, param2)
result = json.loads(html.text) # json.loads로 받으면 dictionary 객체(dict)이므로 Key:value 쌍으로 찾을 수 있다.

# 보통 다른 사이트는 Header의 Referer도 체크를 해서 내 사이트에서 온 요청이 아니면 block한다.
# 즉 가짜 도메인을 섞어 보내봐야 함. 헤더 변조가 먹히지 않는 경우 다른 방법 사용해야 함.
for row in result["records"]:
    print(row)

# pip install selenium으로 셀레니움 모듈 설치 후 http://chromedriver.chromium.org/downloads 에서 ChromeDriver 72.0.3626.69 (Windows 32bit) .exe를 코드가 있는 경로에 복사.
# chromedriver.exe는 실행용이 아니며, 아래와 같이 셀레니움용 크롬을 사용하기 위한 드라이버이므로 실행하지 말것.
browser = webdriver.Chrome() # chrome브라우저를 관리하기 위한 인스턴스 생성
browser.get(url) # 크롬브라우저가 켜지며 url 링크로 이동.

browser.find_element_by_id("search_term").clear() # find_element는 하나만, find_elements는 다중 검색.
browser.find_element_by_id("search_term").send_keys("korea") # 브라우져가 실행되며 search_term ID로 찾은 검색창에 korea라는 텍스트를 자동으로 입력해준다.
browser.find_element_by_id("search").click() # search라는 아이디를 가진 부분을 마우스로 클릭한다.


# 간혹 검색을 완료한 화면일지라도 결과를 자바스크립트가 채워넣은 경우 get_dowmnload함수로는 원하는 검색결과를 받아올 수 없다.
# 셀레니움을 사용하면 페이지 소스를 사용하지 않고, 수정된 DOM을 받아오기 때문에 최종 렌더링 결과물을 사용할 수 있게 된다.
print(browser.page_source) # 셀레니움을 통해 리스폰스받은 HTML정보 확인 가능
result2 = browser.find_element_by_id("results") # results라는 id를 가진 엘리먼트를 하나 검색
for tag in result2.find_elements_by_tag_name("a"): # results가 갖고 있는 하위 구조 중 'a'라는 태그를 가진 모든 엘리먼트를 검색
    print(tag.text) # 찾은 엘리먼트의 내용을 출력
    print(tag.get_attribute("href"))
print(len(browser.find_element_by_css_selector("#results a"))) # css를 활용해 찾을때는 왼쪽과 같이 하면 된다.


# attribute 중 id를 갖고 있어야하며 그 값은 results이고, 그 중 a인 것들을 받아옴. 2개가 나와야 정상.
# beautifulsoup이나 셀레니움 브라우져를 활용하는 방법 모두 css를 지원하므로, css문법에 익숙해지면 편함.
results = browser.find_elements_by_xpath("//divf[@id='results']//a").text # browser가 DOM의 최상위이므로 //으로부터 시작.
for tag in browser.find_elements_by_xpath("//divf[@id='results']//a"):  # DOM tree가 생성되어 있어야만 XPath가 돌아감.
    print(tag.text)
    print(tag.get_attribute("href"))


# 정규식을 활용하는 방법 소개(정규식은 속도가 제일 빠르다.)
# 우리가 원하는 패턴과 일치하는 경우를 모두 찾고자 함. (정규식과 css를 활용하는 것이 어느 언어이던간에 공통되는 부분이 많아 편리함)
print(re.findall("<a href=\"(.+)\">(.+)</a>", result["records"][0]["pretty_link"])) # 정규식 패턴(<a href=\"(.+)\">(.+)</a>)과 원본 문자열(result["records"][0]["pretty_link"]) 입력.
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------




# ------------------------------------- 셀레니움의 다양한 기능을 통해 네이버 로그인 및 스팸메일 리스트 불러오기 ---------------------------------------------------
browser.get("https://nid.naver.com/nidlogin.login")
accountInfo = {"id":"aaaaaa", "pw":"bbbbbb"} # ID, PW는 개인 ID와 PW 입력.

# find_element_by_name과 같이 함수로만 쓰게 되면 셀레니움을 안쓰거나 브라우져가 바뀌는 순간 사용이 어렵게 됨. 따라서 다음과 같이 CSS나 xpath를 사용하는 방법을 알아야 함.
# 1) CSS를 사용하는 경우 : browser.find_element_by_css_selector("#id).clear()
# 2) XPath를 사용하는 경우 : browser.find_element_by_xpath("//input[@name='id']").clear()
# 3) 그냥 함수만 사용하는 경우 : browser.find_element_by_name("id").clear()

# 네이버 로그인 과정이 복잡하므로, Pycharm 등의 IDE를 사용하는 경우 중단점을 걸고 디버그 모드에서 한줄한줄 네이버가 시키는대로(캡차입력 등) 진행 후 코드를 실행할것.
# 자동으로 ID와 PW를 로그인창에 입력
browser.find_element_by_xpath("//input[@name='id']").clear()
browser.find_element_by_xpath("//input[@name='pw']").clear()
browser.find_element_by_xpath("//input[@name='id']").send_keys(accountInfo["id"])
browser.find_element_by_xpath("//input[@name='pw']").send_keys(accountInfo["pw"])

# 디버그 모드에서 F8을 누르면 로그인 버튼을 누르는 과정으로 넘어감. 여기서부터 네이버 보안절차를 수기로 입력 진행
browser.find_element_by_xpath("//input[@title='로그인']")
browser.find_element_by_css_selector("input[title='로그인").click()

browser.get("https://mail.naver.com") # 다시 한번 F8을 누르면 메일함으로 이동
browser.find_element_by_css_selector("span.item_wrap.bu6").click() # 스팸메일함으로 이동.
for tag in browser.find_elements_by_css_selector("strong.mail_title"): # 메일함 리스트 불러와 출력
    print(tag.text)

# 쿠키값을 그대로 전달할 수 있다면 로그인 정보를 넘길 수 있을 것이고, 후속 url들을 원활히 탐색할 수 있을 것이다.
session = requests.Session() # 쿠키를 만들기 위해 세션 생성
for c in browser.get_cookies(): # 브라우져로부터 쿠키 로그를 불러와 출력.
    print(c["name"], c["value"])
    session.cookies.set(c["name"], c["value"]) # browser.get_cookie()로 받은 내용이 F12->Application->cookies에 있는 내용과 동일해야 함.
html = session.get("https://mail.naver.com") # 만들어진 쿠키를 통해 https://mail.naver.com의 정보를 받음.
print(html.text) # 받아온 내용 출력


# 자바스크립트가 가득한 사이트는 정보를 받아오는데에 일정 시간이 걸리거나 절차가 까다롭다. (non-visible인 기간 동안 또는 특정 이벤트를 통해서만 트리거가 발동되는 경우 클릭을 할 수 없기 때문.)
# 따라서 셀레니움은 두 가지 기능 제공 : 1) 단순히 sleep 거는 것, 2) 특정한 무언가가 모습을 나타날 때까지 pending. (sleep을 걸면 모든 사이트가 멈추기 때문에 비동기적으로 작업하기 위해선 안쓰는것이 좋음.)
browser.find_element_by_css_selector(".gnb_btn_login").click() # not visible exception 에러 발생. 하지만 .get_attribute()를 붙여 받아보면 존재는 하는 것을 확인 가능.

# 따라서 아래와 같이 특정 태그가 나타날때까지 비동기적으로 기다릴 수 있게 해줌. 드라이버(browser)를 받아 1초동안 10번 확인하되 ElementNotVisibleException 가 발생할 시엔 그냥 넘어간다.
browserWait = WebDriverWait(browser, 10, 1, ElementNotVisibleException) # wait를 위한 인스턴스 생성

# 우리가 전달한 browser를 x라고 했을때(Lambda), is_displayed 가 참/거짓인지를 검사. 구문 실행중 10초 이내에 프로필 영역을 클릭해서 로그아웃 버튼이 렌더링되어 검출된 경우 true를 반환.
browserWait.until(lambda x:x.find_element_by_css_selector("#gnb_logout_button").is_displayed())
browser.find_element_by_css_selector("#gnb_logout_button").is_displayed() # 구문 실행중 10초 이내에 프로필 영역을 클릭해서 로그아웃 버튼이 렌더링된 경우 true를 반환.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# 기타 유용한 셀레니움 기능
print(browser.window_handles()) # 현재 떠 있는 브라우져창의 정보를 출력
browser.switch_to_window(browser.window_handles[0]) # 브라우져 창을 첫 번째로 전환