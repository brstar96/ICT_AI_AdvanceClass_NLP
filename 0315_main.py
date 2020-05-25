# 이 코드에서는 형태소 분석기를 응용하여 간단한 정규식을 사용하여 토큰화를 수행해 봅니다.

from konlpy.tag import Kkma
from konlpy.corpus import kolaw, kobill # 법률 관련 말뭉치 임포트(사실상 테스트 데이터.)
import nltk
nltk.download("punkt") # 구두점 정의에 필요한 모듈. (※ 다운로드는 최초 1회만 하면 됨)
from nltk.corpus import brown, gutenberg
from nltk.tokenize import sent_tokenize # 문장 단위 tokenize를 수행
from nltk.tokenize import word_tokenize, TweetTokenizer, regexp_tokenize # regexp_tokenize는 내가 정의한 정규식 표현으로 tokenizing을 수행함.
from nltk.corpus import stopwords # 불용어 사전
# brown corpus : 만들어진지 30년이 지났지만 밸런스가 좋아서 교과서처럼 사용하는 Corpus. tagged corpus(어절분류 후 품사까지 붙어 있는)이다.
# gutenberg corpus : 소설 말뭉치.
nltk.download() # Korpus를 다운받을 수 있는 GUI창을 띄워줌. nltk.download("brown")을 치면 GUI가 뜨지 않고 다운로드됨. (※ 다운로드는 최초 1회만 하면 됨)


# ------------------------------------------------- Konlpy 사용해보기 ---------------------------------------------------------------------
ma = Kkma()
print(ma.pos("오늘은 불금입니다.")) # 테스트

print(kolaw.fileids()) # txt 하나만 있음.
print(kobill.fileids()) # 의안과 관련된 txt파일 10개 제공

c = kolaw.open(kolaw.fileids()[0]).read() # 파일포인터를 통해 첫번째 파일 오픈
print(len(c)) # 18884개의 character를 갖고 있음.
print(len(c.split())) # 몇 개의 어절이 있는지 확인해보기(단순 띄어쓰기로 세었기때문에 중복 허용.) (4178개/정식 corpus는 보통 100만~1000만 단위의 어절 제공.)
print(len(c.splitlines()))  # 몇 개의 엔터가 들어가 있는지 확인
d = kobill.open(kobill.fileids()[0]).read()
print(d.splitlines()[:2]) # 처음 두 요소만 출력
# -------------------------------------------------------------------------------------------------------------------------------------------



# ------------------------------- NLTK 말뭉치 사용해보기(brown, gutenberg corpus) ----------------------------------------
print(len(brown.fileids()))
a = brown.open(brown.fileids()[0]).read()
print(len(a), len(a.split()), len(a.splitlines()), a.splitlines()[:3])

b = gutenberg.open(gutenberg.fileids()[0]).read()
print(len(b), len(b.split()), len(b.splitlines()), b.splitlines()[:3])
# ------------------------------------------------------------------------------------------------------------------------



# ------------------------------------------- Tokenize 해보기 -------------------------------------------------------
s = sent_tokenize(b) # 공식적으로 10개의 언어를 지원하지만 한국어, 일본어, 중국어는 없다. 구두점을 기준으로 분석.
print(len(s), len(b.splitlines()))
print(s[:3], b.splitlines()[:3])
print(sent_tokenize("Hello world, Hello world! Hello........?"))
print(sent_tokenize("집에 가고?싶다.....")) # 구두점 다음에 스페이스가 있으면 문장의 경계로 인식.(없으면 하나의 문장으로 인식.) 즉 구두점 다음에 스페이스가 있어야 한다.
print(word_tokenize(d)) # 어절 단위로 인식했으나 띄어쓰기 단위는 아님
print(word_tokenize("10분만 버티자 :) ")) # ':)'는 트위터 등과 같이 몇자 안되는 글자에서 감정을 표현하는 중요한 수단이므로 어절 단위로 분리되면 안된다.
# 따라서 TweetTokenizer라는 모듈이 제공되며, word_tokenize와 특징이 다르므로 인스턴스로 받아서 사용해야 함.
print(TweetTokenizer().tokenize("10분만 버티자 :)")) # ':)'도 분류가 잘 되는 것을 확인할 수 있음.
stopwords.fileids() # 사용자 정의 사전을 추가해서 패턴을 찾고 싶을때 사용.
stopwords.open("english").read()

pattern = r"([가-힣]+)" # 자모를 포함하지 않고 음절 단위로만 뽑고 싶을때 (가~힣 범위 내의 모든 문자를 검색하는 패턴)
print(regexp_tokenize("가123족이 있는 집으로", pattern))
# -------------------------------------------------------------------------------------------------------------------