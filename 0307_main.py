# 이 코드에서는 requests 모듈의 get, post, head 키워드로 리스폰스를 받고, cookie, session 방식으로 로그인을 시도해 봅니다.
# 코드 말미에서는 공공데이터포털에서 실시간 대기오염정보를 받아와 보겠습니다.

import requests
from urllib import parse
import json

# --------------------------------- requests 모듈을 사용하여 리스폰스 받아오는 함수 만들기 ----------------------------------------------
# Get 방식을 통해 리스폰스를 받아오는 함수
def getDownload(url, param=None, retries = 3):
    resp = None
    try:
        # 주피터 노트북에서는 shift + tab을 누르면 파라미터 설명들이 나옴.
        resp = requests.get(url, param, headers={"user-agent":"Mozilla/5.0"}) # 서버를 속이기 위해 headers에 "user-agent":"Mozilla/5.0"를 넣음. (Mozilla/5.0 까지만 넣어도 대부분 ok)
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
print(getDownload("http://www.google.com/search?q=python"))
print(postDownload("http://pythonscraping.com/pages/files/form.html"))
# ----------------------------------------------------------------------------------------------------------------------------------------




# --------------------------------- requests 모듈의 get, post, head 키워드로 리스폰스 받아오기 --------------------------------------------

# http://httpbin.org/get 페이지에서 get방식으로 HTTP 리스폰스 받아보기
resp = requests.get("http://httpbin.org/get") # key-value 쌍을 딕셔너리로 넣어야 함.
print(resp.text)
print(resp.request.headers) # get방식은 body가 header에 들어가 있다. maximum length가 있기 때문에 전부 다 받아올 수가 없음.
print(resp.request.body)

# http://httpbin.org/get 페이지에서 post방식으로 HTTP 리스폰스 받아보기
resp = requests.post("http://httpbin.org/post") # post방식으로 리스폰스를 받아옴
print(resp.text)
print(resp.request.headers)
print(resp.request.body)

# http://httpbin.org/get 페이지에서 head방식으로 HTTP 리스폰스 받아보기
resp = requests.head("http://httpbin.org/head") # head만 읽어온다.
print(resp.text)
print(resp.request.headers)
print(resp.request.body)
# -----------------------------------------------------------------------------------------------------------------------------------------


# getDownload()가 에러를 잘 걸러내는지 테스트하기
url_getDownloadtest = "http://www.crawler-test.com/status_codes/status_" # retries가 3번 출력된 후 500을 반환함.
html = getDownload(url_getDownloadtest+"500", {"q":"test"})
print(html.url)



# --------------------------------- postDownload()를 이용해서 pythonscraping 받아오기 --------------------------------------------

url_postDownloadtest = "http://pythonscraping.com/pages/files/processing.php" # 서버에서 처리되서 돌아오는 값을 받아야 하므로 html이 아닌 php로 보내고 받아온다. 국내 소규모 사이트는 대부분 이런식으로 구성되어 있다.
data = {"firstname":"1234", "lastname":"TEST"} # Firstname과 lastname에 각각 값을 넘겨줌.
html = postDownload(url_postDownloadtest, data) # postDownload함수를 이용해 1234와 TEST를 보내고 리스폰스를 받아옴.
print(html.text) # http://pythonscraping.com/pages/files/processing.php로부터 받은 결과 출력
print(html.request.body)
print(html.status_code)
print(html.request.headers)
# --------------------------------------------------------------------------------------------------------------------------------




# --------------------------------- postDownload()와 cookie, session을 이용해서 로그인 후 리스폰스 받아오기 --------------------------------------------

# 로그인을 하는 방법엔 cookie를 이용하는 것과 session을 이용하는 것 두 가지 방법이 있음.
#get으로 login.html을 받아보면 Your browser must be able to use cookies in order to view our site!에러가 뜸.
url_logintest = "http://pythonscraping.com/pages/cookies/login.html"
html_logintest = getDownload(url_logintest)
print(html_logintest.text)

url_logintest = "http://pythonscraping.com/pages/cookies/welcome.php"
logintest_data = {"username":"asdf", "password":"password"}
html_logintest = postDownload(url_logintest, logintest_data) # 쿠키를 받아오려면 post를 한번은 날려 줘야 함.
print(html_logintest.status_code)
print(html_logintest.text)
print(html_logintest.cookies.get_dict())

# 위에서 ID와 PW를 str로 넘겨줄 땐 로그인이 안되지만, cookie를 넘겨줄때는 로그인이 잘 됨. (쿠키 안에 들어 있는 로그인정보를 이용해 로그인이 된 결과 페이지 접근)
html_logintest = requests.post(url_logintest, cookies = html_logintest.cookies.get_dict(), headers={"user-agent":"Mozilla/5.0"})
print(html_logintest.text)

# 세션으로 로그인하기
url_logintest_session = "http://pythonscraping.com/pages/cookies/welcome.php"
Session_logintest_data = {"username":"asdf", "password":"password"}
session = requests.session()
html_session = session.post(url_logintest_session, Session_logintest_data)
html_session = session.post(url_logintest_session)
print(html_session.text)

# 세션으로 로그인이 안되는 케이스
url_logintest_session_https = "https://lms.koipa.or.kr/auth/login"
Session_logintest_data_https = {"next":"/", "email":"brstar96@naver.com", "password":"01082343179", "remember":"on"}
session_https = requests.session()
html_session = session_https.post(url_logintest_session_https, Session_logintest_data_https)
print(html_session.cookies.get_dict()) # HTTPSConnectionPool 발생.
# HTTPSConnectionPool에러는 수신자와 발신자 간 인증서를 교환하지 못해 handshake를 할 수 없어 로그인에 실패한다.
# 로그인 스텝이 복잡한 경우 빠르게 포기하거나 다른 방법을 찾아봐야 함.
# ------------------------------------------------------------------------------------------------------------------------------------------------------



# --------------------------------- 공공데이터포털에서 실시간 대기오염정보 받아오기 --------------------------------------------
# 실시간 대기정보 받아오는 함수
def getAirKorea(url, param):
    html = getDownload(url, param)
    result = json.loads(html.text)
    # 작성중...


# '공공데이터포털'의 '대기오염정보 조회 서비스'에서 '시도별 실시간 측정정보 조회'에 '서울'넣고 json으로 받아오기.
# 주소 뒤에 &_returnType=json를 넣어서 json형식으로 요청한 후 파싱하면 대기 정보를 실시간으로 얻어올 수 있다.
# ? 까지가 사이트 주소, 그 뒤로 이어지는 내용들을 파라미터로 활용하면 됨.
SeoulAirUrl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
param = {"serviceKey":"9XtVuLvOwav9xyTaj3A%2BPJo%2BHv9%2BdRZtmY0%2B05eFMYE6UcSlE%2Be%2B9T2Qd5KH1Uh9TxUMAQgInmZjqZEyhb9F7A%3D%3D", "numOfRows":10, "pageNo":1, "sidoName":"서울", "ver":"1.3", "_returnType":"json"}

# get방식으로 데이터를 주고받으면 아스키코드가 아닌것을 자동으로 헥사바이트코드와 %가 붙도록 인코딩한다. 따라서 SERVICE KEY IS NOT REGISTERED ERROR가 발생.
# 처음 받은 서비스 key가 깨진 상태이기 때문에 올바른 정보를 받아올 수 없는 상태. (UTF-8로 인코딩된 서비스키를 이미 제공하고 있는데, 또 인코딩해서 발생하는 에러)
SeoulAir_html = getDownload(SeoulAirUrl, param) # 개발자도구를 통해 SeoulAirUrl 페이지의 request method를 확인해보면 GET으로 주고받기 때문에 get method로 받아오는 것.
print(SeoulAir_html.text)

# 따라서 인코딩을 안시키고 서비스를 보내던가, 디코딩을 한 후 다시 get방식으로 보내는 방법 두 가지가 있다. (urllib의 parse를 활용하거나 requests.utils.unquote활용. )
print(param["serviceKey"])
print(parse.unquote(param["serviceKey"]))
print(parse.quote(parse.unquote(param["serviceKey"])))

# 그러나 urilib의 parse를 사용하는 것은 여러모로 불필요하므로, requests의 unquote 사용.
param["serviceKey"] = requests.utils.unquote(param["serviceKey"])
FinalHtml = getDownload(SeoulAirUrl, param)
print(FinalHtml.text) # json으로 받아오므로, 이것을 api 기술문서를 참조해 해석하고 딕셔너리로 바꾸면 됨. 그 전에 오브젝트화를 시켜야 하는데, json 패키지를 사용하면 됨.

APIresult = json.loads(FinalHtml.text) # 이미 값들이 메모리에 올라가 있을때는 loads를 사용.
print(len(APIresult["list"])) # row를 10개 가져옴을 알 수 있음.
for row in APIresult["list"]: # 데이터의 개수가 10개보다 적을때(마지막 페이지)까지 가져옴. (또는 list에 none객체가 나오거나, length가 0이거나, key value가 없을때까지 가져옴.
    print(row["stationName"], row["pm25Value"]) # 중구의 현재 pm 2.5 미세먼지 농도를 출력.
    # 잘 응용하면 한시간마다 대기농도, 풍향 등의 정보를 자동으로 수집하여 CSV 등의 정형 데이터로 저장하고 시각화하고 머신러닝하는 등 다양한 방법으로 이것을 활용할 수 있다.

# 마지막 페이지까지 전부 긁어와보기 (param 중에 "pageNo":1를 이용해서 다음 페이지를 참조 가능)
    ## 함수화를 하거나 for문을 돌리거나 짜기 나름
    # getAirKorea() 호출.
# ------------------------------------------------------------------------------------------------------------------------------




# ---------------------- timetime 사이트로 배운 내용 복습하기 ----------------------------
url_timetime = "http://timetime.kr/user/login"
data_timetime = {
    "username": "asdfggh",
    "password":"bjxjjJzPdm2Tq9e"
}
session_timetime = requests.Session() # 세션 객체를 통해 로그인 정보를 넘김
html_timetime = session_timetime.post(url_timetime, data_timetime)
print(html_timetime.status_code)
print(html_timetime.request.body)
print(html_timetime.cookies.get_dict()) # 쿠키는 사용하지 않는 사이트인듯.
print(html_timetime.text)
# ---------------------------------------------------------------------------------------