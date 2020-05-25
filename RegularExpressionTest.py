import re

# 검증할 문자열
myStr = u"김구라abcd해골^^^^원숭이1234가adad나다라이혜리ㅇㄴ러ㅐㅁ러ㅏ;ㅏㅣㅓ"
pattern = re.compile(r'이혜리') # 검색을 위한 정규식 패턴 정의 ('이혜리' 텍스트만 뽑아내고자 함)

# 한글만 뽑아낸 후 이혜리 텍스트 검색
FindKor = re.findall(u"[가-힝]+", myStr) # 자모를 포함하지 않고 음절 단위로만 뽑고 싶을때 (가~힣 범위 내의 모든 문자를 검색하는 패턴)
print(FindKor)
FindHyeri = re.findall(pattern, myStr)
print(FindHyeri)