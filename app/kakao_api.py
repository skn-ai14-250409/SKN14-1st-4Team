import os
import requests
from dotenv import load_dotenv


load_dotenv()
KAKAO_API_KEY = os.getenv("KAKAO_REST_API_KEY")
RADIUS = 500

def get_nearby_places(lat, lng, category_code, radius=RADIUS, size=5):
    """
    Kakao Local API를 통해 좌표 기준으로 반경 내 장소 검색
    - lat, lng: 중심 좌표
    - category_code: 카테고리 코드 (예: CE7 = 카페)
    - radius: 반경(m)
    - size: 결과 수 (최대 15)
    """
    url = "https://dapi.kakao.com/v2/local/search/category.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {
        "category_group_code": category_code,
        "x": lng,  # 경도(x), 위도(y)
        "y": lat,
        "radius": radius,
        "size": size,
        "sort": "distance"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("documents", [])
    except Exception as e:
        print(f"[Kakao API 오류] {e}")
        return []
