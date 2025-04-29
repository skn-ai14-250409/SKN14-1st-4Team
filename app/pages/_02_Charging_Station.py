import streamlit as st
import requests, folium, sys, os
import pandas as pd
from streamlit_folium import st_folium
from dotenv import load_dotenv
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db_utils import setup_database_and_table, clear_table, insert_data, fetch_all_stations, filter_nearby_stations, sql_to_csv
from kakao_api import get_nearby_places


load_dotenv()
SERVICE_KEY = os.getenv("API_SERVICE_KEY")
key_decode = requests.utils.unquote(SERVICE_KEY) #무조건 디코딩된 키 사용

API_URL = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"

cfg = config.load_config()

STATUS_MAPPING = cfg['status_mapping']
ZCODE_MAPIING = cfg['zcode_mapping']
ZSCODE_MAPPING = cfg['zscode_mapping']
CHARGER_TYPE_MAPPING = cfg['charger_type_mapping']
CATEGORY_MAPPING = cfg['CATEGORY_MAPPING']

st.set_page_config(
    page_title='전기차',
    page_icon='⚡',
    layout='wide')


setup_database_and_table()

@st.cache_data(show_spinner=True)
def get_charger_info(zcode, zscode, num_of_rows=1000):
    all_items = []
    page_no = 1

    while True:
        params = {
            'serviceKey': key_decode,
            'pageNo': str(page_no),
            'numOfRows': str(num_of_rows),
            'zcode': str(zcode),
            'zscode': str(zscode),
            'dataType': 'JSON'
        }
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                items = data.get('items', {}).get('item', [])

                if isinstance(items, dict):
                    items = [items]

                all_items.extend(items)

                if len(items) < num_of_rows:
                    break
                
                else:
                    page_no += 1
            
            except Exception as e:
                print("Error parsing response:", e)
                break
        else:
            print(f"API request failed with status code {response.status_code}")
            break

    return pd.DataFrame(all_items)

def preprocess_df(df):

    show_df = df[['statNm', 'addr', 'lat', 'lng', 'stat', 'limitYn', 'limitDetail', 'output', 'chgerType']].rename(columns={
        'statNm': '충전소명',
        'addr': '주소',
        'lat': '위도',
        'lng': '경도',
        'stat': '상태코드',
        'limitYn': '이용제한여부',
        'limitDetail': '이용제한사유',
        'output' : '급속충전량',
        'chgerType': '충전기타입'
    })

    show_df['충전기타입'] = show_df['충전기타입'].astype(str).map(CHARGER_TYPE_MAPPING)
    show_df['상태'] = show_df['상태코드'].astype(str).map(STATUS_MAPPING)
    show_df['이용제한'] = show_df.apply(lambda row: row['이용제한사유'] if row['이용제한여부'] == 'Y' else '', axis=1)
    return show_df[['충전소명', '주소', '위도', '경도', '상태', '이용제한', '급속충전량', '충전기타입']]

def show_ui_with_other_info():
    st.markdown("<h1 style='text-align: center;'>🔌전기차 충전소 및 편의시설 검색</h1>",
                unsafe_allow_html=True)

    region = st.selectbox("시/도를 선택하세요", list(ZCODE_MAPIING.keys()))
    district = None
    if region in ZSCODE_MAPPING:
        district = st.selectbox("구/군을 선택하세요", list(ZSCODE_MAPPING[region].keys()))
    else:
        st.warning("선택한 시/도에는 구/군 데이터가 없습니다.")
    
    if st.button("충전소 조회하기"):
        if district:
            zcode = ZCODE_MAPIING[region]
            zscode = ZSCODE_MAPPING[region][district]
            df = get_charger_info(zcode, zscode)

            if not df.empty:
                df['lat'] = df['lat'].astype(float)
                df['lng'] = df['lng'].astype(float)

                st.session_state['df'] = df
                st.session_state['show_df'] = preprocess_df(df)
                st.session_state['search_clicked'] = True

                clear_table()
                
                insert_data(st.session_state['show_df'])
                
                st.session_state['stations'] = fetch_all_stations()
            else:
                st.warning("⚠️ 충전소 데이터를 가져오지 못했습니다.")

    if st.session_state.get('search_clicked', False):

        stations = st.session_state['stations']

        stations['표시문구'] = stations['충전소명'] + " (" + stations['상태'] + ")" +  "  " + stations['주소']

        selected_station = st.selectbox("🔍 충전소를 선택하세요", stations['표시문구'])

        selected_categories = st.multiselect( "📂 주변 편의시설을 선택하세요 (복수 선택 가능)", options=list(CATEGORY_MAPPING.keys()), default=["편의점"])

        selected_station = stations[stations['표시문구'] == selected_station].iloc[0]
        selected_lat = selected_station['위도']
        selected_lng = selected_station['경도']

        left_col, right_col = st.columns([2, 1])

        with left_col:
            m = folium.Map(location=[selected_lat, selected_lng], zoom_start=17)

            if selected_station['이용제한'] == '' or selected_station['이용제한'] is None:
                selected_station['이용제한'] ='이용가능'
                
            folium.Marker(
                location=[selected_lat, selected_lng],
                icon=folium.Icon(color="blue", icon="flash", prefix="fa"),
                icon_size = [40, 40],
                tooltip=f"🔋 {selected_station['충전소명']} 🔋",
                popup=folium.Popup(f"""
                    <div style="font-size: 14px;">
                    <b>충전소명:</b> {selected_station['충전소명']}<br><br>
                    <b>주소:</b> {selected_station['주소']}<br><br>
                    <b>상태:</b> {selected_station['상태']}<br><br>
                    <b>급속충전량:</b> {selected_station.get('급속충전량', '정보없음')}kW<br><br>
                    <b>충전기 타입:</b> {selected_station.get('충전기타입', '정보없음')}<br><br>
                    <b>이용자 제한:</b> {selected_station.get('이용제한', '없음')}<br><br>
                </div>
                """, max_width=250)
            ).add_to(m)

            places_list = []
            places = None
            for category in selected_categories:
                category_code, color = CATEGORY_MAPPING[category]
                places = get_nearby_places(selected_lat, selected_lng, category_code)

                if places is not None:
                    places_list.append(places)

                    for place in places:
                        html_popup = f"""
                            <div style='width: 200px; font-size: 14px;'>
                                <b>{place['place_name']}</b><br>
                                <span style='color: #555'>{place['road_address_name']}</span><br>
                                <span>📞 {place.get('phone', '없음')}</span>
                            </div>
                        """
                        iframe = folium.IFrame(html=html_popup, width=200, height=100)
                        popup = folium.Popup(iframe, max_width=200)

                        folium.Marker(
                            location=[float(place["y"]), float(place["x"])],
                            icon=folium.Icon(color=color, icon="info-sign"),
                            tooltip=f"{category} - {place['place_name']}",
                            popup=popup
                        ).add_to(m)

            st_folium(m, width=700, height=500)    

        with right_col:

            for i, places in enumerate(places_list):
                if places is not None and len(places) > 0:
                    places = pd.DataFrame(places)
                    st.markdown(f"<h4>🏪 {selected_categories[i]} ({len(places)}곳)</h4>", unsafe_allow_html=True)
                    st.dataframe(places[['place_name', 'phone', 'distance']])
                else:
                    st.markdown(f"<h4>🏪 {selected_categories[i]} (0곳)</h4>", unsafe_allow_html=True)
                
show_ui_with_other_info()
