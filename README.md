# ICT_AI_AdvanceClass_NLP
* KOIPA의 ICT 인공지능 고급반(NLP class) 수업 코드 정리용 리포지토리입니다.<br>
* 스터디 중 필사한 코드이기 때문에 설명용 주석이 난잡하게 달려 있으며, 실습 위주로 진행되었기 때문에 특정 기능을 확인하실 땐 새 .py를 만들어서 테스트를 진행하시기 바랍니다. (수정 없이 run하실 경우 에러가 발생할 수 있습니다.) <br>
* 실제 응용 시에는 본인 프로젝트에 맞게 리팩토링하신 후 사용하시기 바랍니다.<br>
* 3월 19일 이후 코드부터는 유지보수 편의를 위해 Jupyter notebook으로 작성되어 있습니다.<br><br>

1. 3월 5일 : 비정형 HTTP 데이터를 다루는 기초적인 방법에 대해 배웠습니다. (HTTP, Urllib, Requests)
2. 3월 7일 : 웹 크롤링 - requests모듈을 사용해 웹 페이지로부터 리스폰스를 받고 cookie와 session 방식으로 로그인을 시도해 보았습니다. 또, 공공데이터포털로부터 대기오염지수를 .json으로 불러와 파싱하는 방법에 대해 배웠습니다. (requests, json)
3. 3월 8일 : DOM tree를 구성하고 태그와 키워드를 통해 원하는 정보를 스크랩하는 방법에 대해 배웠습니다. (requests, BeautifulSoup)
4. 3월 11일 : Selector를 사용한 웹 크롤링 방법(CSS 정보로부터 탐색)에 대해 배웠습니다. (requests, BeautifulSoup)
5. 3월 12일 : BeautifulSoup을 이용해 정적 컨텐츠(ex. 뽐뿌 사이트)를 긁어오는 방법에 대해 알아봅니다. (BeautifulSoup)
6. 3월 13일 : selenium을 이용해 동적 컨텐츠(ex. 네이버 스팸메일함)를 긁어오는 방법에 대해 알아봅니다. (selenium)
7. 3월 14일(프로젝트) : 다음과 KT 사이트에 로그인해보고(Selenium) 네이버 뉴스 사이트에서 핫한 기사 60개를 카테고리별로 긁어오는 프로젝트를 수행했습니다. 
8. 3월 15일 : NLTK, Konlpy 형태소 분석기와 간단한 정규식을 사용하여 토큰화를 수행해 봅니다. (Konlpy, NLTK, re, sent_tokenize)
9. 3월 18일 : 텍스트를 분석하는 다양한 기법들에 대해 알아보고(concordance, similar 등), 14일에 긁은 뉴스 기사들을 실제로 분석해 봅니다. N-gram 기법을 통해 빈도수를 기반으로 어근을 분리해 봅니다. 
10. 3월 19일 : 말뭉치로부터 최빈 단어를 그래프로 시각화하고(matplotlib) 다양한 불용어(구두점, Stopwords)를 처리하는 방법에 대해 알아봅니다.(punctuation)
11. 3월 20일 : 다양한 방법을 사용하여 Text로부터 형태소 분석을 수행해 봅니다. (English : nltk.pos_tag, Kor : Hannanum, Kkma, Komoran, Okt)
12. 3월 21일 : 구문 분석을 수행한 후 형태소를 분석하여(POS Taggers) 시각화(ParseTree, WordCloud)하는 방법에 대해 알아봅니다. 
13. 3월 22일 : 주어진 텍스트 데이터를 이용해 정보 검색(색인)을 수행하는 방법에 대해 알아보았습니다. (collections.defaultdict 사용, Document-Term Matrix, invertedDocument)
14. 3월 26일 : 정규식을 이용해 한국어 텍스트 문서의 전처리를 수행하고 lexicon을 만들어 봅니다. (N-gram, Regular expression)
15. 3월 27일 : 벡터 공간에 문서를 임베딩하고 term에 가중치를 적용해 IR(Information Retrieval)을 수행하는 방법에 대해 알아봅니다. (VS model, TF, IDF)
16. 3월 28일 : TF(Term Frequency), IDF(Inverse Document Frequency)를 구하고 Euclidian distance와 Coisne simmilarity로 IR(Information retrieval)을 수행해 봅니다.
17. 3월 29일(프로젝트) : 그동안 배운 내용 중 3월 28일 코드를 기반으로 정보 검색기를 만들어 봅니다. (4/3 코드와 통합되어 있습니다.)
18. 4월 1일(특강) : Tensorflow로 간단한 선형 회귀 문제를 구현해 보고, Keras를 이용해 간단한 이미지 분류(MNIST) 및 영화 데이터를 통한 감정 분류(IMDB)를 수행해 봅니다. 
19. 4월 2일 : 유클리디안 거리와 코사인 각도를 이용한 유사도 비교 알고리즘을 구현하고 KNN 알고리즘을 통해 주어진 벡터로부터 가장 유사한 벡터를 3개를 찾아 봅니다.
20. 4월 3일(프로젝트) : 3월 29일 코드에 cosine simmilarity와 KNN search 알고리즘을 적용하여 3월 14일에 긁은 네이버 뉴스 기사의 카테고리를 분류해 봅니다. (쿼리 뉴스 기사를 텍스트 전문을 받아 정치, IT/과학 등의 카테고리를 분류합니다.)  
21. 4월 4일 : 확률을 기반으로 문서 분류를 수행하고 네이버 메일함의 메일들을 크롤링해 봅니다. 
    * 0404_main.ipynb : Naive Bayes 기법을 통해 확률을 기반으로 문서를 분류해 봅니다.
    * 0404_NaverMailCrawler.py.ipynb : Selenium과 requests 모듈을 이용하여 HTTP response 객체를 생성합니다.
22. 4월 5일(프로젝트) : 4월 4일의 코드를 기반으로 네이버 메일함으로부터 정상 메일과 스팸 메일을 각각 15개씩 크롤링하고, 확률에 기반하여 정상 메일인지 스팸 메일인지 분류해 봅니다. (Naive Bayes)
23. 4월 9일 : Information Retrieval에서 사용되는 성능평가 기법에 대해 알아봅니다. (Precision, Recall)
24. 4월 10일(프로젝트, 미완) : 4월 5일의 코드를 업그레이드하여 쿼리 기사 문서에 대해 카테고리별 다중 분류를 수행하고(Bimodal to Multimodal) 4월 9일에 배운 성능평가 기법을 적용하여 정확도 테스트를 수행해 봅니다. (Cosine similarity, KNN Search, Precision and Recall)
25. 4월 11일 : 군집화 방법 중 하나인 Kmeans 알고리즘에 대해 알아봅니다. 2차원 유클리드 공간에서의 Kmeans 군집화를 수행해 보고 다차원으로 확장하여 군집화를 적용해 봅니다. (K-means, clustering)
26. 4월 12일 : 어휘 클러스터를 만들고 word cloud 형태로 시각화를 수행해 봅니다. (wordcloud)
 

* 0307_main.py, 0410_main_practice.ipynb is under maintenance
<br>

| 사용한 Package | Version | 설명 |
|:-------:|:-------:|:-------|
|   beautifulsoup4    |   4.7.1    |HTML 문서를 DOM(Document Object Model) 구조로 해석하는 데 도움을 주는 모듈입니다. |
|   JPype1    |   0.6.3    |자바 클래스 라이브러리에 대해 full-access가 가능하게 해 주는 모듈입니다.|
|   Keras    |   2.2.4   |쉬운 고수준 API를 제공하는 딥러닝 프레임워크입니다. |
|   konlpy      |   0.5.1   |한국어 정보처리를 위한 파이썬 패키지입니다. |
|   lxml    |   4.3.2    |속도가 빠른 Parser입니다. 보통 beautifulsoup4과 lxml을 함께 사용하며, 다른 Parser로는 html.parser가 있지만 속도가 빠른 lxml을 자주 사용합니다.|
|   matplotlib    |   3.0.3    |자료를 chart나 plot으로 시각화하는 패키지입니다.|
|   nltk      |   3.4    |영문 자연어처리 교육용으로 개발된 Natural Language Package입니다.|
|   numpy      |   1.16.2    |파이썬 기반의 데이터 분석 환경에서 행렬 연산을 위한 핵심 라이브러리입니다.|
|   requests    |  2.21.0    |간편하게 HTTP 요청 처리를 하기 위해 주로 사용하는 모듈입니다.|
|   scipy     |   1.2.1   |파이썬 환경에서 과학, 분석 및 엔지니어링을 위한 라이브러리입니다.|
|   seaborn     |   0.9.0   |matplotlib을 기반으로 다양한 색상 테마와 통계용 차트 등의 기능을 추가한 시각화 패키지입니다.|
|   selenium     |   3.141.0   |webdriver라는 API를 통해 Chrome 등의 브라우저를 제어할 수 있으며, 주로 웹앱을 테스트하는데 이용하는 프레임워크입니다. DHTML 웹 크롤러를 만들 때 가장 많이 사용됩니다.|
|   soupsieve     |   1.8   |beautifulsoup4와 함께 사용되도록 만들어진 CSS selector 라이브러리입니다. modern CSS selector를 활용해 selecting, matching, filtering 등을 수행할 수 있도록 해 줍니다.|
|   urllib3      |   1.24.1   |web의 source code를 읽어올 수 있도록 도와주는 모듈입니다. requests를 사용하면 간혹 보안으로 인하여 웹의 코드를 읽어오지 못할 수 있기 때문이며, urllib3으로 읽어온 값은 binary이므로 decoding을 한 후 beautifulsoup4으로 파싱해야 합니다.|
|   wordcloud    |   1.5.0   |발생 빈도가 높은 품사 순으로 wordcloud를 만들어 주는 모듈입니다.(단 matplotlib처럼 한국어도 사용할 수 있도록 폰트를 설정해 주어야 합니다.) |
