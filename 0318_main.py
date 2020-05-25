# 이 코드에서는 텍스트를 분석하는 다양한 기법들에 대해 알아봅니다.
# word_tokenize, TweetTokenizer, regexp_tokenize로도 처리가 어려운 한국어에 대해 토큰화를 시도해 봅니다. (많이 쓰는 조합, 패턴, 형태로부터 빈도를 세고 순서를 주어 의미적으로 통용되는 어근 분리)

from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from konlpy.corpus import kolaw, kobill
from nltk import Text
from matplotlib import font_manager, rc
import os, re
from collections import defaultdict

txtfilespath = "./0314_DownloadedNewstxts" # 긁어왔던 기사가 저장되어 있는 폴더

path = "C:/windows/fonts/HMKMRHD.ttf" # matplot의 폰트를 지정하기 위한 경로 설정
font = font_manager.FontProperties(fname=path).get_name() # 폰트매니저 객체 생성
rc("font", family=font) # 폰트 변경

# 지난시간 복습 (Korpus 길이 출력)
kcorpus = kolaw.open(kolaw.fileids()[0]).read()
ktokens = word_tokenize(kcorpus) # Korpus에 대해 토큰화 수행
print(len(ktokens), len(set(ktokens)))

corpus = gutenberg.open(gutenberg.fileids()[0]).read()
tokens = word_tokenize(corpus) # 토크나이즈 수행
print(len(tokens), len(set(tokens)))
txt = Text(tokens) # 어휘 단위로 잘라줌.
ktxt = Text(ktokens) # 어휘 단위로 잘라줌.




# ------------------------------ 각 토큰에 어떤 단어가 몇번씩 나왔는지 분포 확인해보기. -------------------------------------------------
print(txt, txt.vocab()) # <Text: Emma by Jane Austen 1816> <FreqDist with 8406 samples and 191785 outcomes>
print(txt, txt.vocab().most_common()) # 가장 많이 나온 요소들을 표시
print(ktxt.vocab().most_common())
txt.plot(50) # 빈도수를 plot으로 표시
ktxt.plot(50) # 한글의 경우 폰트가 깨진다. matplot의 폰트 경로 설정을 해 주어야 함.(코드 상단 14~16라인 참고)

# 빈도만 갖고 emma가 나온 확률을 따진다면 전체 19만여개의 단어 중 855개는 빈도수가 낮아 무작정 빈도로만 학습하는 것은 잘못된 학습을 야기할 수 있다.
print(txt.count("Emma")) # 단어를 주면 몇번 나왔는지 반환하는 함수. (855개)
print(txt.concordance("Emma")) # 특정 window 내에서 검색. 이 문서에서 텍스트를 추렸는데, 엠마가 어느 부분에서 나타나는지 확인할 목적. (ex. '아, 엠마가 여기서 이렇게 쓰이는구나. 여기에 맞게 트리를 짜야겠다.')
print(txt.similar("Emma")) # emma가 있는 자리와 유사한 위치엔 어떤 단어가 있는지 출력 (ex. 'she it he weston i ~가 나왔으니 Emma는 여자구나. 주로 주어 위치에서 누군가를 지칭할때 쓰이는구나?')
txt.dispersion_plot(["Emma", "Jane"]) # 전체 문서를 하나의 x축으로 표현했을때 내가 지칭하는 단어들이 얼만큼의 분포를 갖는지 그려줌.
# 분포도 그래프를 통해 Jane은 주인공과 중간서부터 만나서 이야기를 끌어 나가는 역할을 하는 인물임을 알 수 있음. 이처럼 정확하지는 않아도 유의미한 피쳐를 유추할 수 있도록 도와준다.

print(ktxt.count("국민")) # '국민의', '국민에'와 같은 결합형태소들에 대한 형태소분석이 안되었으므로 2번밖에 출력되지 않음.
print(ktxt.concordance("국민의")) # '국민의' 라는 단어가 문법적으로 어떻게 사용되는지 유추해볼 수 있다.
print(ktxt.similar("헌법")) # 이 단어가 어느 곳에 위치해있고 어느 역할을 하는 단어들과 함께 배치되어 있는지 확인 가능.
ktxt.dispersion_plot(["국민의", "국무총리"]) # '국민의' 는 '국무총리'보다 상대적으로 중요도가 더 높다고 할 수 있다.
# -----------------------------------------------------------------------------------------------------------------------------------------




# ----------------------------- 0314_practice_main.py에서 수집한 뉴스 기사들을 분석해 보기 -------------------------------------------------

FileList = [file for file in os.listdir(txtfilespath)
    if file.startswith("생활문화") and file.endswith(".txt")]
# print(FileList)

with open("{0}/{1}".format(txtfilespath, FileList[0]), encoding='UTF-8') as fp: # fp : file pointer
    news = fp.read()
    # print(news)

ntxt = Text(word_tokenize(news))
print(ntxt.vocab().most_common())
print(len(ntxt), len(set(ntxt)))
ntxt.plot(50) # 특이하게도 어떤 기사를 그리던 간에 위에서 아래로 뚝 떨어지는 그래프임을 확인 가능.
print(ntxt.count("소변을")) # 등장횟수 출력
print(ntxt.concordance("소변을")) # 등장하는 문장들 출력
print(type(ntxt.vocab())) # <class 'nltk.probability.FreqDist'>
# ------------------------------------------------------------------------------------------------------------------------------------------




# --------------------------------------------------------------- n-gram --------------------------------------------------------------------------
# 텍스트로부터 n개의 아이템을 만들되, contiguous sequence를 만든다. (어절, 음절 단위로 만들 수도 있음.)
# 특정한 열 이후에 나올 단어가 무엇인지 예측하고 싶을때 사용.

"""
* 다음 문장('Beautiful is better than ugly.')에서 'ugly'가 나올 확률을 알고 싶다고 가정하자. 이 문장의 확률은 다음과 같이 결합확률로 표현 가능하다. 
P(ugly | Beautiful is better then)
P(than | Beautiful is better)
P(better | Beautiful is)
P(is| Beautiful)
P(Beautiful) <- 하지만 우리가 가진 것은 말뭉치뿐으로, Beautiful에 대한 확률을 알 수가 없어 빈도수를 통해 예측을 하게 된다. ( freq(is) / frec(Beautiful) )
하지만 corpus에 Beautiful라는 단어가 많이 들어 있지 않은 경우 다른 단어들의 빈도수가 가진 priori에 눌려 확률이 0에 수렴할 수도 있다. 또한 찾았다고 하더라도 확률이 굉장히 작게 나올 수 있음.

* 따라서 바로 앞에 있는 것만 뒤져 보도록 함.
P(ugly | then)
P(then | better)
이와 같은 (ugly, then)쌍이 많으면 연산량이 줄어 좋지 않을까? 라는 아이디어 -> Bigram
(ugly, then, ugly)와 같이 세 개를 사용하면 -> Trigram
(ugly, then, ... , N) -> N-gram

국민, 국민의, 국민을, 국민에게, ... 
bigram(음절 단위로 잘라 보면...) -> 국민, 국민, 민의, 국민, 민을,국민, 민에, 에게 (즉, 형태소 분석기가 없더라도 상대적으로 빈도수가 높은 단어들을 분리해 내는 방식으로 어근을 분리할 수도 있다.) 

* N-gram 적용 순서
1. 문자열 입력, N = 2
2. N 문자열을 추출
3. 2의 결과를 리스트화
4. 국민의, N = 2 0> 국민, 민의 -> (국민, 민의)
"""

def ngramUmheol(sentence, n=2): # 음절 단위로 구분하는 함수. sentence를 받아 2개(n=2)씩 쪼갠다.
        result = []
        tokens_ngram = sentence.split()

        for i in range(len(tokens_ngram) - n+1):
            # result.append(tokens_ngram[i:i+n]) # 방법1
            # result.append(tuple(tokens_ngram[i:i+n])) # 방법2(튜플로 반환 시 키값을 쓸 수 있음)
            result.append(" ".join(tokens_ngram[i:i+n])) # 방법3
        return result

print(ngramUmheol("국민을 위한", n=3)) # n 파라미터 개수에 따라 나뉘는 개수가 다름.
print(ngramUmheol("국민을 위한 정부", n=2))

ktokens_ngramUmheol = ngramUmheol(kcorpus, n=2)
print(len(ktokens_ngramUmheol)) # 4177개.
t = Text(ktokens_ngramUmheol)
print(len(t), len(set(t)))
print(t.vocab().most_common())

ktokens_news = ngramUmheol(news, n=2)
print(len(ktokens_news)) # 4177개.
t = Text(ktokens_news)
print(len(t), len(set(t)))
print(t.vocab().most_common())


"""
* 순서
1. 입력으로 문자열을 받고
2. 각 문자열을 음절로 분리, 음절 사이에 공백을 삽입
3. 공백문자가 나오면 '_'로 치환
4. 각 단어의 끝에 단어의 마지막을 알려주는 </w> 태그 부착.
   ex) low -> {l o w </w> : 5}
5. 각 음절 분리
6. 분리된 음절을 n-gram(n=2)으로 그룹화. 
   ex) l o, o w, w </w>
7. 각 그룹의 빈도를 합산
   ex) (l o):5, (o w):5, (w </w>):5
8. 최대값 찾기
9. 최대값(그룹)을 합침.
   ex) w </w> => w</w>
   ex) low => l o w</w> => l o w</w>
10. 5번부터 반복 5번.
"""

def makeTerm(sentence):
    terms = sentence.split() # 3번과정(공백문자가 나오면 '_'으로 치환
    result = []

    for term in terms:
        result.append(" ".join(list(term) + ["</w>"])) # 4번과정(term을 list에 넣어 조각낸 후 공백을 삽입한 다음 문장의 끝을 나타내는 태그를 삽입)

    return "_".join(result)

print(makeTerm("low lower")) # makeTerm함수 테스트

def ngramSplit(data, n=2): # 각 음절 분리
    result = defaultdict(int)
    for k, v in data.items(): # data는 key-value 쌍으로 이루어져 있다.
        token = k.split()

        for i in range(len(token)-n+1):
            pair = (token[i], token[i+1]) # 새로운 쌍을 만듬.
            result[pair] += v
    return result


# 튜플로 만들었으므로 키를 통해 접근하여 사용할 수 있다.
data = {makeTerm("low"):5,
        makeTerm("lowest"):2,
        makeTerm("newer"):6,
        makeTerm("wider"):3
        }


def mergeTokens(maxToken, data): # 9번과정 (많이 나온 두 개가 하나의 토큰으로 합쳐지게 된다.)
    key = " ".join(maxToken) # 찾아야 하는 이 key와 일치하는 것을 합쳐야 함. (정규식을 활용)
    result = defaultdict(int)
    """
    우리가 찾아야 하는 문자열이 "l o w e r </w>", key = "e r" 이라고 해 보자. 
    자세히 보면 문자 앞뒤로 whitespace가 존재함을 알 수 있으며, whitespace로 시작하지 않아야 하며 끝나지도 않는 것을 찾아야 함. 즉 ·가나다·라·마· 처럼 완벽하게 떨어져 있는 것을 찾음.
    # regexr.com에서 만든 정규식 패턴을 테스트 가능.  
    """
    # \S는 'Not whitespace', \s는 'whitespace'를 의미.
    pattern = re.compile(r"(?!=\S)" + key + r"(?!\S)") # 공백(whitespace)으로 시작하지 않고 공백으로 끝나지 않는 패턴 중에서 key를 찾음. (이때 S는 문자가 아닌 모든 집합을 의미)

    for k, v in data.items():
        new = pattern.sub("".join(maxToken), k) # sub() -> 정해진 패턴에 교체할 문자의 원본을 주면 패턴에 맞게 돌려줌. (replace할것과 원본 ste 두개가 인자로 들어감) 이제 새로운 쌍이 된다.
        result[new] = v

    return result

for _ in range(5): # 이터레이션을 통해 빈도를 파악
    tokens_ngramtest = ngramSplit(data)
    maxToken = None # 빈도수가 최대로 많은 토큰 찾기 용도
    maxFreq = 0

    # maxToken 찾기
    # for k, v in tokens_ngramtest.items():
    #     if v > maxFreq:
    #         maxFreq = v
    #         maxToken = k

    # 하지만 우리는 dict에 저장을 해 두었으므로 max 함수를 사용하면 편하게 구현 가능(아래 세개 중 하나 사용)
    # maxToken = max(tokens_ngramtest, key=lambda x:tokens_ngramtest[x])
    # maxToken = max(tokens_ngramtest, key=lambda x:tokens_ngramtest.get(x))
    maxToken = max(tokens_ngramtest, key=tokens_ngramtest.get)

    data = mergeTokens(maxToken, data)
    print(maxToken)
    print(data)

'''
*정리 : 
- 반복을 통해서 많이 나오는 패턴의 알파벳을 합쳐 어근을 뽑아낸다. 이것을 통해 feature를 뽑아낼 수 있음.
- 어근만 추출하면 이 어근은 우리가 모델에 돌릴 수 있을 정도의 범위에 들어올 것이고, 이렇게 쌓인 어근들로 학습에 활용할 수 있다. 많이 쓰이는 어근들의 패턴을 파악하므로, 어느 문화권이던지 간에 학습이 가능함.
- 띄어쓰기 패턴을 검사해서 띄어쓰기 규칙 검사기도 만들 수 있음. 또, '시@발'처럼 욕 사이에 특수문자를 섞는 케이스도 stopword를 사용해 불용어를 처리함으로서 걸러낼 수 있다.
'''
# ------------------------------------------------------------------------------------------------------------------------------------------------------