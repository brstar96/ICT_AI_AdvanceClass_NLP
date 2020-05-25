# 이 코드에서는 다음과 KT 사이트에 로그인해봅니다.

import requests
from selenium import webdriver


def getDownload(url, param=None, retries=3):
    resp = None
    try:
        resp = requests.get(url, params=param, headers = header)
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

header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}


# 다음 로그인해보기(간단버전)
browser = webdriver.Chrome() # chrome브라우저를 관리하기 위한 드라이버 인스턴스 생성
browser.get("https://www.daum.net")
print(browser.window_handles()) # 현재 떠 있는 브라우져창의 정보를 출력
browser.switch_to_window(browser.window_handles[0]) # 브라우져 창을 첫 번째로 전환

# iframe을 만난 경우 해결법
iframe = browser.find_element_by_id("loginForm").get_attribute("outerHTML")
browser.switch_to_frame(iframe)
print(browser.find_element_by_id("id").send_keys("TEST"))
browser.switch_to_default_content()



# 기존에 핸들링하던 창 말고 새 창을 띄워서 핸들링하기(KT 사이트 로그인해보기)
# KT의 경우 로그인 버튼을 누르면 새 창이 뜨는데, 때문에 윈도우 창 핸들러를 통해 새창으로 전환 후 기존 작업을 진행해야 함.
browser.get("http://www.kt.com")
print(browser.window_handles) # 현재 떠 있는 창의 정보를 출력 (ex. ['CDwindow-7D8862923043552361CA406415B5E5FD'])
browser.switch_to_window(browser.window_handles[-1]) # 새 창으로 전환하여 핸들러 접근 권한을 가짐.
browser.find_element_by_id("userId").send_keys("TEST") # 로그인창의 userId에 TEST라는 str 전달.
browser.switch_to_window(browser.window_handles[0]) # 원본 창으로 다시 switch


