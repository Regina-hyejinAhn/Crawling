import ssl, certifi
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import string
import requests
import json

ssl._create_default_https_context = ssl._create_unverified_context
# NLTK 불용어 다운로드
nltk.download('stopwords')  # stopwords 데이터셋 다운로드
stop_words = set(stopwords.words('english'))

# Scale SERP API 요청 설정
params = {
    'api_key': 'A014CB488595423BA3C451AE5EA833AC',
    # 'search_type': 'autocomplete',
    'q': 'AI,quality,requirements',
    # 'scholar_year_min': '2010',
    # 'scholar_year_max': '2024'
}

# HTTP GET 요청을 통해 검색 결과 가져오기
api_result = requests.get('https://api.scaleserp.com/search', params)

# JSON 응답 파싱
api_data = api_result.json()
print(f'api_data: {api_data}')


# 논문 제목과 초록에서 단어를 수집하는 함수
def collect_words_from_results(search_results):
    words = []

    # 검색 결과의 'organic_results'에서 각 항목 처리
    for result in search_results.get('organic_results', []):
        title = result.get('title', '')
        snippet = result.get('snippet', '')  # 초록 대신 사용
        content = title + ' ' + snippet
        words += preprocess_text(content)

    return words


# 텍스트 전처리 함수
def preprocess_text(text):
    text = text.lower()  # 소문자 변환
    text = text.translate(str.maketrans("", "", string.punctuation))  # 구두점 제거
    words = text.split()  # 단어로 분리
    words = [word for word in words if word not in stop_words]  # 불용어 제거
    return words


# 단어 빈도를 계산하는 함수
def get_word_frequencies(words):
    return Counter(words)


# 단어 빈도를 시각화하는 함수
def plot_word_frequencies(word_frequencies, top_n):
    # most_common이 빈 리스트일 경우 처리
    if not word_frequencies:
        print("No words were collected. Please check your data source.")
        return

    most_common = word_frequencies.most_common(top_n)

    # 빈 결과를 처리
    if not most_common:
        print("No frequent words found.")
        return

    words, frequencies = zip(*most_common)

    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color='skyblue')
    plt.title(f"Top {top_n} Most Frequent Words in AI Quality Requirements")
    plt.xlabel("Words")
    plt.ylabel("Frequencies")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 메인 함수
if __name__ == "__main__":
    # 논문 제목과 초록에서 단어 수집
    words = collect_words_from_results(api_data)

    # 단어 빈도 계산
    word_frequencies = get_word_frequencies(words)

    # 단어 빈도 상위 10개를 시각화
    plot_word_frequencies(word_frequencies, top_n=30)