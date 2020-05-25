# 이 코드에서는 builtwith, whois, urllib 모듈을 활용해 Request를 날리고 정보를 받아봅니다.

from builtwith import builtwith
from whois import whois
from urllib import robotparser, request, error, parse
import requests

# ----------------------------- builtwith과 whois로 사이트 헤더 반환받기---------------------------------------

print(builtwith('http://wordpress.com')) # 사이트 헤더를 dict형태로 반환.
print(whois('http://wordpress.com')) # whois도 builtwith와 비슷하게 사이트 헤더를 반환.
# -------------------------------------------------------------------------------------------------------------




# --------------------------------- urllib의 Robotparser 사용해보기 ------------------------------------------

robot = robotparser.RobotFileParser() # robotparser를 사용하기 위한 객체 생성
robot.set_url('https://google.com/robots.txt')
robot.read() # 리퀘스트를 날림.
print(robot.can_fetch('Agent', 'https://google.com/robots.txt')) # '내 봇의 이름이 이런데(Agent), 저 url(https://google.com/robots.txt)에 대해 크롤링해도 되는가?'

robot = robotparser.RobotFileParser() # 인스턴스 생성
robot.set_url('https://www.koipa.or.kr/robots.txt') # 가져올 사이트 정의
robot.read() # 리퀘스트를 날림.
print(robot.can_fetch('Agent', 'https://www.koipa.or.kr/robots.txt')) # 크롤링 가능 여부 판단
# koipa 사이트같은 국내 사이트의 경우 인코딩 문제가 상당히 많이 발생한다. (unicodedecodeerror)
# 이 문제를 해결하기 위해서는 헤더를 바꿔야 함.
# ------------------------------------------------------------------------------------------------------------




# --------------------------------- urllib의 request 사용해보기 ----------------------------------------------

resp = request.urlopen("https://www.google.com/search?q=ptython") # google.com에 대한 리스폰스 객체(<class 'http.client.HTTPResponse'>)를 반환받는다.
# request에 한글이 들어가게 되면 인코딩 에러 발생('ascii' codec can't encode characters)
# 영어가 들어가도 에러(urllib.error.HTTPError: HTTP Error 403: Forbidden)가 발생하는데, 이는 권한이 없는데에도 불구하고 요청했을때 발생하는 에러이다. (robots.txt에 search하지 말라고 해놨기때문)

print(resp.read()) # 인자 중 amt=none 으로 하면 전체를 read. 단 read는 stack에서 pop한것과 같기 때문에 이 다음에 또 쓰게되면 아무것도 남아있지 않음.
print(resp.read().decode("utp-8")) # byte타입을 str타입으로 바꿔주는 부분. (이렇게 하면 str이기 때문에 검색할수도 있고 str과 관련한 연산자를 사용할 수 있다.)
print(resp.getheaders()) # url 주소를 반환
print(resp.getcode()) # 다른페이지에서 응답을 받은 상태. (원래 접근하지 말아야 할 페이지에 접근하고자 했기때문에, 대신 다른 페이지의 정보를 발신.) 코드 200이 떴으므로 정상이긴 하지만 우리가 원하는 내용은 아님.

agent = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"}
request.Request() # 기존까지는 url을 str로 직접 넘겼지만 헤더를 고치기 위해서는 이제부터 request 오브젝트로 넘겨야 함.
# bot은 user-agent가 None이라 권한이 없음. 따라서 46번라인처럼 헤더에 user-agent 정보를 넣어서 속여야 함. (user-agent 정보는 크롬 F12 개발자도구->Network 열어두고 구글검색 한번 하면 TCP/IP 주고받은 내역이 뜸. 그 중에서 맨 첫번째 ?search부분에 있음.)
# ------------------------------------------------------------------------------------------------------------




# ----------------------------- url을 받아 HTTP 리스폰스를 받아오는 함수 ------------------------------------

def download(url, retries=3):
    resp = None # except에 없으면 None이 반환될 것이기 때문에, 이게 반환되면 다른 에러가 발생했다는 뜻.
    req = request.Request(url, headers=agent) # 이제는 리퀘스트할때 str이 아니라 req 객체가 넘어감.
    try:
       # resp = request.urlopen(url)
       resp = request.urlopen(req)
    except error.HTTPError as e: # 에러에 대한 이벤트 핸들러를 만듬.
        if 500 <= e.code < 600 and retries >0: # 500 <= e.code < 600 이고 retries >0인 경우에 실행
            return download(url, retries-1)
        else:
            print(e.code) # 에러 코드가 뭐임?
            print(e.reason) # 이유가 뭐임?
            print(e.headers) # 헤더가 뭐였음?
    return resp

def download2(method, url, param, retries=3): # requests 모듈을 사용하여 수정한 download함수
    resp = None # except에 없으면 None이 반환될 것이기 때문에, 이게 반환되면 다른 에러가 발생했다는 뜻.
    try:
       resp = requests.get(url, params=param, headers=agent)
       resp.raise_for_status() # HTTP에러가 한번이상 발생하면, 이 raise_for_status가 정보를 다 담고 있음. 이를 통해 에러를 핸들링할 수 있다.
    except requests.exceptions.HTTPError as e:
        if 500 <= e.code < 600 and retries >0: # 500 <= e.code < 600 이고 retries >0인 경우에 실행
            return download(url, retries-1)
        else:
            print(e.code) # 에러 코드가 뭐임?
            print(e.reason) # 이유가 뭐임?
            print(e.headers) # 헤더가 뭐였음?
            print(resp.request.headers) # 모든 정보를 출력(에러 메시지까지)
    return resp
# -----------------------------------------------------------------------------------------------------------

html = download("https://www.google.com/search?q=python") #위에서 만든 download 함수 테스트해보기
html.read().decode("utp-8") # 받아온 HTTP 리스폰스를 utf-8 형식으로 디코딩




# ------------------------------------ urllib의 parse 활용해보기 --------------------------------------------

print(parse.urlparse("https://www.google.com/search?q=python")) # url을 넣으면 6개의 컴포넌트로 쪼개어 반환(ParseResult(scheme='https', netloc='www.google.com', path='/search', params='', query='q=python', fragment=''))
print(parse.urljoin("https://www.google.com/search?q=python", "search/about")) # base를 넣으면 새로운 url과 함쳐서 리턴. (내가 상대주소를 넣으면 뒤에 새롭게 넣은 상대주소와 합쳐서 새 주소를 만듬.)
# urljoin를 반복문과 함께 적절히 응용하면 봇이 사이트의 앵커 태그를 통해 네트워크를 돌아다닐 수 있게 된다. (ex. https://www.google.com/search/about)

print(parse.quote("파이썬")) # 글자를 받으면 웹에서 사용할 수 있는 형태로 바꿔줌. (%ED%8C%8C%EC%9D%B4%EC%8D%AC, 파이썬3은 기본적으로 UTF-8이라 인코딩 신경 안써도 됨)
print(parse.quote_plus("파 이 썬")) # 띄어쓰기가 들어가 있는 경우 표준에 맞게 +를 삽입해줌. (%ED%8C%8C+%EC%9D%B4+%EC%8D%AC)
print(parse.unquote_plus("%ED%8C%8C+%EC%9D%B4+%EC%8D%AC"))
print(parse.urlencode({"q":"파이썬"})) # 딕셔너리 구조이며, &를 붙여가며 key/value쌍으로 변환해줌. (q=%ED%8C%8C%EC%9D%B4%EC%8D%AC)
# -----------------------------------------------------------------------------------------------------------




# ------------------------------- urllib 대신에 requests 모듈을 활용해보기 ---------------------------------

# requests는 편하게 크롤링을 할 수 있도록 도와주는 모듈. (원노트 참고)
# 위에서 했던 것을 requests를 이용해 바꿔보기
resp = requests.request("get",
                        "https://www.google.com/search?q=파이썬", #requests 모듈은 심지어 한글을 넣어도 잘 작동한다.
                        headers = agent)
# requests 모듈은 다양한 기능들을 제공한다 : print(resp.text), print(resp.status_code), print(resp.reason), print(resp.headers), print(resp.request.headers) 등등

resp.encoding = "utf-8" # utf-8로 인코딩된 값을 받겠다는 선언
resp.content # 사실 알아서 바이트로 받아옴. (바이트타입으로 변환된 결과물을 들고 있으므로 굳이 변환 안해줘도 됨.)
html = download2("get",
                "http://httpbin.org/get", # 이것저것 리퀘스트를 날리고 테스트해볼 수 있는 사이트.
                {"q":"파이썬", "a":"asdf"}, # 자동으로 주소를 조합해서 파라미터를 download2 함수로 넘겨줌.
                 agent)
print(html.text)
# ----------------------------------------------------------------------------------------------------------