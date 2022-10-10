from konlpy.tag import Komoran
from collections import Counter

def extract_keywords (article_content, article_title):
    # 키워드로 제외되는 명사
    black_list = [
        # 보편성 의존명사
        '이', '것', '데', '바', '따위', '분',
        # 주어성 의존명사
        '지', '수', '리', '나위',
        # 서술성 의존명사
        '때문', '나름', '따름', '뿐', '터',
        # 부사성 의존명사
        '만큼', '대로', '듯', '양', '체', '채', '척', '등', '뻔', '만',
        # 단위성 의존명사
        '개', '마리', '장', '권', '켤레', '줄', '몰', '명', '여명', '씨', '전',
        '미터', '킬로그램', '리터', '달러', '칼로리', '쿼터', '바이트', '파스칼', '헤르츠', '데시벨',
        '년', '월', '일', '시', '분', '초', '개월',
        # 경험적 제외 명사
        '.net', '.com', '.co', '.kr', '이다', '뉴시스', '뉴스1',
    ] # 숫자
    for i in range(5001):
        if len(str(i)) == 1:
            black_list.append('0' + str(i))
            black_list.append('00' + str(i))
            black_list.append('000' + str(i))
        elif len(str(i)) == 2:
            black_list.append('0' + str(i))
            black_list.append('00' + str(i))
        elif len(str(i)) == 3:
            black_list.append('0' + str(i))
        black_list.append(str(i))
    # 직책 명사
    roles = [
        '대통령', '장관', '여사', '위원장', '위원', '비대위원', '원내대표', '의원', '시장', '도지사', '구청장', '청장', '총장' # 정치
        '회장', '사장', '부회장', '부사장', '원장', '부장', 'PD', 'pd', '대표', # 경제
        '판사', '검사', '변호사', '변호인', # 사회
        '감독', '선수', '코차', # 스포츠
    ]
    # 대한민국 순위 성씨 43 - SGIS (통계지리 정보 서비스)
    # https://sgis.kostat.go.kr/statbd/family_01.vw
    last_name = [
        '강', '고', '곽', '구', '권',
        '김', '나', '남', '문', '민',
        '박', '배', '백', '서', '성',
        '손', '송', '신', '심', '안',
        '양', '엄', '오', '우', '원',
        '유', '윤', '이', '임', '장',
        '전', '정', '조', '주', '지',
        '진', '차', '최', '하', '한',
        '허', '홍', '황',
    ]

    komoran = Komoran()

    # article_title로부터 명사 추출
    print(article_title)
    keyword_from_title = komoran.nouns(article_title)
    # article_content로부터 명사 추출
    print(article_content)
    keyword_from_content = komoran.nouns(article_content)

    # 제목으로부터 나온 키워드는 2의 가중치를 둠
    # 내용으로부터 나온 키워드는 1의 가중치를 둠
    # 명사가 사용된 빈도수를 계산
    keyword_from_article = keyword_from_title * 2 + keyword_from_content
    keyword_dic = Counter(keyword_from_article)

    sorted_keyword_dic = sorted(keyword_dic.items(), key = lambda item: -item[1])

    # 성 + 직책 -> 이름 변경
    keyword_count = len(keyword_from_content)
    for i in range(keyword_count):
        if keyword_from_content[i] in roles:
            if i > 0 and len(keyword_from_content[i - 1]) == 1:
                for keyword, count in sorted_keyword_dic:
                    if keyword_from_content[i - 1] in last_name and len(keyword) > 1 and keyword not in black_list and keyword.startswith(keyword_from_content[i - 1]):
                        # print(keyword_from_content[i - 1] + ' + ' + keyword_from_content[i] + '-> ' + keyword)
                        keyword_from_article.remove(keyword_from_content[i - 1])
                        keyword_from_article.remove(keyword_from_content[i])
                        keyword_from_article.append(keyword)
                        break

    keyword_dic = Counter(keyword_from_article)

    sorted_keyword_dic = sorted(keyword_dic.items(), key = lambda item: -item[1])

    # 가장 많이 인용된 명사 중 블랙리스트에 없고 명사의 1글자가 아니라면 기사에 대한 키워드
    # 기사에 대한 키워드 총 3개를 뽑아냄
    limit = 0
    keywords = []
    for keyword, count in sorted_keyword_dic:
        if len(keyword) != 1 and keyword not in black_list and keyword not in roles and keyword not in last_name:
            keywords.append(keyword)
            limit += 1
        if limit == 3:
            break
    try:
        return keywords[0], keywords[1], keywords[2]
    except:
        return '', '', ''