# 이 코드에서는 긁어온 리스폰스 정보를 통해 Dom tree를 구성하고 특정 태그나 키워드를 통해 원하는 부분만 스크랩하는 방법에 대해 알아봅니다.

from bs4 import BeautifulSoup # Dom tree를 탐색하고 수정하는 기능을 제공하는 모듈로 웹 데이터 크롤링 또는 스크래핑을 할 때 사용.
import requests

# --------------------------------- requests 모듈을 사용하여 리스폰스 받아오는 함수 만들기 ----------------------------------------------
# Get 방식을 통해 리스폰스를 받아오는 함수
def getDownload(url, param=None, retries = 3):
    resp = None
    try:
        # 주피터 노트북에서는 shift + tab을 누르면 파라미터 설명들이 나옴.
        resp = requests.get(url, param, headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}) # 서버를 속이기 위해 headers에 "user-agent":"Mozilla/5.0"를 넣음. (Mozilla/5.0 까지만 넣어도 대부분 ok)
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

# 함수 작동여부 테스트
# print(getDownload("http://www.google.com/search?q=python"))
# print(postDownload("http://pythonscraping.com/pages/files/form.html"))
# ----------------------------------------------------------------------------------------------------------------------------------------



# --------------------------------- BeautifulSoup으로 HTML 정보 긁어오기 ----------------------------------------------------------

# 실제로 관심있는 부분은 아래 링커 태그(<a>)이다. 이 앵커 태그를 통해 이 링크 저 링크 옮겨다니면서 파싱을 수행.
# 지금은 실제 웹을 구현할 수는 없으므로, 아래와 같이 임시 str을 만들어 진행하자.
html = """
<html>
    <head>
    </head>
    <body>
        <div id="result">
            <p class = "row">
                <a href = "/?" class = "red">go to page1!</a>
                <a href = "/?" class = "blue">go to page2!</a>
            </p>
        </div>
    </body>
</html>
"""

dom = BeautifulSoup(html, "lxml") # lxml parser를 활용해 html 문자열을 분석한 후 Dom tree가 생성된다.
print(dom.html.body.div.p.a["href"]) # Pip install lxml을 통해 설치해주어야 제대로 작동함. 계층구조 확인해서 트리를 구성할것!
print(dom.a.name) # 이런식으로 트리 구조에 따라 element들을 호출할 수 있다.
print(dom.body.text) # \n이 3번 나오는 이유는 <p>를 넣어 개행을 했기 때문. (그래서 표준 HTML에서는 p를 가급적 쓰지 말라고함)
# dom은 Tag라고 하는 객체들(<class 'bs4.element.Tag'>)로 구성되어 있고, Tag에 대한 전후 관계가 트리 안에 들어 있음.
print(len(dom.a)) # 두번째 a태그는 불러올 수 없다.
# ----------------------------------------------------------------------------------------------------------------------------------




# ----------------------------------------- find와 fina_all 함수를 통해 태그의 내용을 dom 트리로부터 불러오기 -------------------------------------------------------------------------------------------------

# ID나 class값을 통해 가져올 순 없을까? 또는 ID나 클래스 값을 출력해볼 순 없을까?
#
# dom과 관련된 함수는 원노트에 첨부된 슬라이드 참고. 아래와 같이 find함수를 이용하면 전부 또는 인덱스 단위로 불러올 수 있다. (dom.a == dom.find("a")과 같음.)
print(dom.find("a", {"class":"red"})) # <a> 태그 중 class가 red인 것을 찾아라. (Tag를 리턴함. <class 'bs4.element.Tag'>)
print(dom.find_all("a")) # resultset을 리턴하며(<class 'bs4.element.ResultSet'>), resultset은 list처럼 사용할 수 있음.
print(type(dom.h1)) # dom트리에 없는 태그라도 Nonetype으로 노드를 하나 만듬. (<class 'NoneType'>)
try:
    print(dom.h1.text) # Attribute 에러를 피하기 위해 예외처리. 그러나 이 방법은 상당히 귀찮기 때문에 아래 방법을 사용.
except AttributeError as e:
    print("Not found!") # dom트리에 없는 태그라도 Nonetype으로 노드를 하나 만듬. (<class 'NoneType'>)

print(dom.find("a", {"class": "blue"}))
print(dom.find_all({"div", "a"}, {"class":"blue"})) # 여러 태그의 내용을 동시에 가져오기. and연산처럼 동작한다. DIV도 갖고오고 a인 애들만 갖고오되 class가 blue인 것만 가져옴.
print(dom.find("", {"class":"blue"})) # 전체 클래스 중에 tag가 blue인 모든 내용들을 가져옴. (태그 객체 자체를 가져오므로 노드가 살아있음. 즉 노드를 통해 부모, 형제를 탐색 가능.  <class 'bs4.element.Tag'>)
print(dom.find("", text="go to page1!")) # Go to page1 텍스트가 들어간 태그를 가져옴 (노드 안의 값을 가져오므로 더이상 Dom tree를 탐색할 수 없다. <class 'bs4.element.NavigableString'>)
print(dom.find_all("a", limit=1)) # "a" 태그를 가진 한개의 내용만 가져옴. (limit=1 == find()가 같은 역할을 함.) 파라미터를 통해 find_all도 find처럼 사용할 수 있다.
print(dom.find_all("", {"class":{"red", "blue"}}))  # 여러 태그의 내용을 동시에 가져오기. or연산처럼 동작한다. Tag의 class가 red이거나(or) blue인 것들을 가져옴.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# ----------------------------------------------------- dom트리를 활용해 계층 구조 탐색해 보기 ------------------------------------------------------------------------------

# http://pythonscraping.com/pages/page3.html을 get방식으로 download하고 str로 받아진 이 페이지를 dom트리로 만들어 계층 구조 탐색해 보기
url = "http://pythonscraping.com/pages/page3.html"
html = getDownload(url) # response object (text = str, content = bytes).
dom = BeautifulSoup(html.content, "lxml") #BeautifulSoup을 통해 분석하여 Dom트리 생성
# print(dom.prettify())를 쓰면 print(dom)보다는 약간 깔끔하게 개행까지 포함해서 출력해준다.

# 웹 페이지에서 ID가 footer인 노드를 찾기
node = dom.find("", {"id":"footer"}) #<class 'bs4.element.Tag'>
# 이때 lxml과 html.parser의 성능이 다르기 때문에 둘이 다른 결과를 보임. 국내의 경우 html.parser가 잘 작동할 때가 많다.
# lxml은 xml처럼 잘 정의된 사이트에서 빠르고 정확하게 작동한다.
parent = node.find_parent() # Wrapper를 알고 싶다면 개발자도구->Elements 기능을 활용하면 알 수 있음.
parents = node.find_parents() # limit 파라미터를 활용하면 find_all에서 limit로 하나만 불러왔던것과 똑같이 사용할 수 있다.
print(len(parents)) # 4개.
print(node.name, node.attrs, parent.name, parent.attrs)

print(parent.find_all()) # parent노드에서 시작하는 전체 자식들을 반환. (49개) 즉 자식의 자식까지 모두 찾으며, 너비 우선이 아닌 깊이 우선으로 서치한다.
print(parent.find_all(recursive=False)) # recursive는 딱 자식 노드만 찾겠다는 옵션
#
for tag in parent.find_all(recursive=False): # 하위 자식 태그들의 이름을 모두 출력.
    print(tag.name)

# 작업을 하기 전 태그들의 개수와 구조를 알고 있어야 작업이 편하다. (수업에서는 사전에 준비해 오셔서 접근이 쉽지만, 실전에서는 실제 구조를 파악한 후 크롤링해야함.)
print(parent.find_all(recursive=False)[2].name ) # 예상대로라면 div가 나와야 함. Dom->HTML->body->div(ID:wrapper)->div 구조.
print(parent.find_all(recursive=False)[2].find().text) # 내용까지도 접근할 수 있다. find().text)는 Dom->HTML->body->div(ID:wrapper)->div->p 구조.

# 형제 노드 찾기
divNode = parent.find_all(recursive=False)[2]
print(divNode.find_previous_siblings(limit=1)[0].name) # (왼쪽)형제 노드를 검색. (h1)
print(node.find_previous_sibling().find_previous_sibling().find().name) # sibling's'와 sibling 혼동 주의! (결과 : p)

# 위에서 배운 내용들 연습해보기 >>
# http://pythonscraping.com/pages/page3.html에서 가격 정보 5개만 불러와보기 (내 방식)
urlPythonscraping = "http://pythonscraping.com/pages/page3.html"
htmlPythonscraping = getDownload(urlPythonscraping)
domPythonscraping = BeautifulSoup(htmlPythonscraping.content, "lxml")
nodePythonscraping = domPythonscraping.find_all("", {"class":"gift"})
pricenode = nodePythonscraping[0].find_all("td")[2]
print(pricenode) # len = 1, <class 'bs4.element.Tag'>
# 이후 정규식을 활용해 $로 시작하는 부분만 긁어온다.

# http://pythonscraping.com/pages/page3.html에서 가격 정보 5개만 불러와보기 (정답)
# div id가 footer인 노드로부터 시작해 부모로 올라간 다음 class="gift"인 tr태그를 찾는 방식.
nodePythonscraping2 = domPythonscraping.find("", {"id":"footer"})
for tag in nodePythonscraping2.find_parent().find_all("", {"class":"gift"}):
    print(tag.find_all()[3].text.strip()) # [3]을 넣어준 것은 ','를 기준으로 파싱하기 위해서이고, 이후 strip를 이용해 앞뒤 개행문자 공백을 날려준 결과를 출력.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
