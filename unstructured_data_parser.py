import re
import json
from collections import defaultdict
from typing import Dict, List

# 예시 캡션
caption = """
((저장 필수💖)) 찰떡 아이스의 계절이 돌아왔다💝

혜화로 놀러간다면
들르기 좋은 카페❣

예쁘고 맛있는 아이스 모찌와
생과일 음료들도 좋고

창가쪽 바테이블과
내부 거울 테이블까지 완벽한 공간✨

귀여운 산딸기 찰떡 아이스가 있는 이곳은?
#카페 #혜화역
___________________
📍#일월일일 (@@1o1o_hh)
위치: 경기 평택시 포승읍 하만호길 237
시간: 매일 12:00-21:00
___________________
📷@phocat_magazine

📸요즘 핫플 빠르게 알고 싶다면?
@phocat_magazine
"""

# 키워드 사전
keyword_dict = {
    "뷰맛집": "뷰좋음",
    "카공족": "조용함",
    "조용한카페": "조용함",
    "노트북가능": "콘센트",
    "콘센트많음": "콘센트"
}


def extract_info_from_caption(caption: str) -> Dict[str, List[str]]:
    result = defaultdict(list)

    # 1. 해시태그 추출
    hashtags = re.findall(r"#\w+", caption)
    result["hashtags"] = [tag.lower() for tag in hashtags]

    # 2. 키워드 정규화
    keywords = []
    for tag in result["hashtags"]:
        clean_tag = tag.replace("#", "")
        if clean_tag in keyword_dict:
            keywords.append(keyword_dict[clean_tag])
    result["keywords"] = list(set(keywords))

    # 3. 카페 이름 추출 (짧은 단어 + "카페" 패턴)
    cafe_names = re.findall(r"(\w{2,10}카페)", caption)
    if cafe_names:
        result["cafe_name"] = list(set(cafe_names))

    # 4. 주소 추출 (지번 + 도로명 주소 통합 대응)
    pattern = (
        r"(?P<province>[가-힣]+[도시남북원주])\s*"                 # 도, 특별시, 광역시 (ex. 서울특별시, 경기도)
        r"(?P<city>[가-힣]+[시군구])?\s*"                  # 시, 군, 구 (ex. 평택시, 강남구)
        r"(?P<town>[가-힣]+[읍면동리])?\s*"                 # 읍, 면, 동, 리 (ex. 포승읍, 수지면, 논현동)
        r"(?P<village>[가-힣0-9\-]+[동리가로길])\s*"          # 법정동 단위 (optional, ex. 성수동2가)
        r"(?P<number>\d?+(?:-\d+)?)\s*"                      # 번지 번호 (ex. 646-1)
        r"(?P<building>[^\n]*)?"                        # 건물명, 상세주소 (optional)  
        r"(?:\s*\((?P<extra>[^)]+)\))?"                      # 괄호 안 추가 정보 (optional)
    )

    match = re.search(pattern, caption)
    if match:
        result["address"] = match.group()
        result["address_components"] = match.groupdict()
    else:
        result["address"] = "주소 인식 실패"

    return result


# 테스트 실행
info = extract_info_from_caption(caption)
print(json.dumps(info, indent=2, ensure_ascii=False))