import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import BeautifyIcon
from st_aggrid import AgGrid, GridOptionsBuilder

# 서비스 키
SERVICE_KEY = f'COVqDxtrNsa1PEgImSCkU%2B9ncLCoNr4m%2Bh6kiSZX%2B8dTB5pAB9VgCV1y0B8OqZvYpiMjOBMHGId7NJlJPAALwA%3D%3D'
key_decode = requests.utils.unquote(SERVICE_KEY) #무조건 디코딩된 키 사용

API_URL = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"

# 상태 매핑
status_mapping = {
    '0': '알수없음',
    '1': '통신이상',
    '2': '충전대기',
    '3': '충전중',
    '4': '운영중지',
    '5': '점검중',
    '9': '상태미확인'
}

color_mapping = {
    '2': 'blue',
    '3': 'red',
    '1': 'gray',
    '4': 'gray',
    '5': 'gray',
    '9': 'gray',
    '0': 'gray'
}

zcode_mapping = {
    '서울특별시': 11,
}

zscode_mapping = {
    '서울특별시': {
        '강남구': 11680,
        '강동구': 11740,
        '송파구': 11710,
        '종로구': 11110,
        '중구': 11140,
        '용산구': 11170,
    }
}

st.set_page_config(
    page_title='전기차',
    page_icon='⚡',
    layout='wide')

@st.cache_data(show_spinner=True)
def get_charger_info(zcode, zscode, num_of_rows=1000):
    params = {
        'serviceKey': key_decode,
        'pageNo': '1',
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
            return pd.DataFrame(items)
        except:
            return pd.DataFrame()
    else:
        return pd.DataFrame()

def preprocess_df(df):
    show_df = df[['statNm', 'addr', 'lat', 'lng', 'stat', 'limitYn', 'limitDetail']].rename(columns={
        'statNm': '충전소명',
        'addr': '주소',
        'lat': '위도',
        'lng': '경도',
        'stat': '상태코드',
        'limitYn': '이용제한여부',
        'limitDetail': '이용제한사유'
    })
    show_df['상태'] = show_df['상태코드'].astype(str).map(status_mapping)
    show_df['이용제한'] = show_df.apply(lambda row: row['이용제한사유'] if row['이용제한여부'] == 'Y' else '', axis=1)
    return show_df[['충전소명', '주소', '위도', '경도', '상태', '이용제한']]

def create_map(df, show_df, center_lat=None, center_lng=None, zoom_start=13):
    if center_lat is None or center_lng is None:
        center_lat = df['lat'].astype(float).mean()
        center_lng = df['lng'].astype(float).mean()

    m = folium.Map(location=[center_lat, center_lng], zoom_start=zoom_start)
    i = 1
    for idx, row in df.iterrows():
        lat = float(row['lat'])
        lng = float(row['lng'])
        stat_code = str(row['stat'])

        try:
            info = show_df.iloc[idx]
            station_name = info['충전소명']
            station_addr = info['주소']
            station_stat = info['상태']
        except:
            station_name = "이름없음"
            station_addr = "주소없음"
            station_stat = "정보없음"

        popup_html = folium.Popup(f"""
        <div style='width: 220px; font-size: 13px;'>
            <b>{station_name}</b><br>
            {station_addr}<br>
            상태: {station_stat}
        </div>
        """, max_width=250)
        
        if station_name == st.session_state['selected_station']:
            icon = BeautifyIcon(
                icon_shape='marker',
                border_color=color_mapping.get(stat_code, 'gray'),
                border_width=3,
                text_color='white',
                background_color=color_mapping.get(stat_code, 'gray'),
                icon_size=[40, 40]  # 크기 키움
            )
        else:
            # ✅ 나머지는 기본 작은 아이콘
            icon = BeautifyIcon(
                icon_shape='marker',
                border_color=color_mapping.get(stat_code, 'gray'),
                border_width=1,
                text_color='white',
                background_color=color_mapping.get(stat_code, 'gray'),
                icon_size=[20, 20]  # 기본 크기
            )

        folium.Marker(
            location=[lat, lng],
            popup=popup_html,
            icon=icon
        ).add_to(m)

    return m

# --- Streamlit 앱 시작 ---
st.title("전국 전기차 충전소 검색기")

if 'search_clicked' not in st.session_state:
    st.session_state['search_clicked'] = False
if 'selected_station' not in st.session_state:
    st.session_state['selected_station'] = None





# --- 지역 선택 ---
region = st.selectbox("시/도를 선택하세요", list(zcode_mapping.keys()))
district = None
if region in zscode_mapping:
    district = st.selectbox("구/군을 선택하세요", list(zscode_mapping[region].keys()))
else:
    st.warning("선택한 시/도에는 구/군 데이터가 등록되어 있지 않습니다.")




# --- 조회 버튼 ---
if st.button("충전소 조회하기"):
    if district:
        zcode = zcode_mapping[region]
        zscode = zscode_mapping[region][district]
        df = get_charger_info(zcode, zscode)

        if not df.empty:
            df['lat'] = df['lat'].astype(float)
            df['lng'] = df['lng'].astype(float)
            st.session_state['df'] = df
            st.session_state['show_df'] = preprocess_df(df)
            st.session_state['search_clicked'] = True
            st.session_state['selected_station'] = st.session_state['show_df']['충전소명'].iloc[0]


# --- 지도 + 상세정보 출력 ---
if st.session_state.get('search_clicked'):
    show_df = st.session_state['show_df']
    df = st.session_state['df']

    st.subheader("충전소 목록 (클릭해서 선택)")

    gb = GridOptionsBuilder.from_dataframe(show_df[['충전소명', '주소', '상태', '이용제한']])
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        show_df[['충전소명', '주소', '상태', '이용제한']],
        gridOptions=grid_options,
        update_mode='SELECTION_CHANGED',
        height = 300,
        width = '100%'
    )

    # if len(grid_response['selected_rows']) > 0:
    if grid_response['selected_rows'] is not None:
        selected_station_name = grid_response['selected_rows']['충전소명'].values[0]
        if selected_station_name != st.session_state['selected_station']:
            st.session_state['selected_station'] = selected_station_name

    col1, col2 = st.columns([5, 3])

    with col2:
        # 상세 정보 표시
        selected_row = show_df[show_df['충전소명'] == st.session_state['selected_station']].iloc[0]
        st.subheader("충전소 상세 정보")
        info_placeholder = col2.empty()
        info_placeholder.markdown(f"""
        **충전소명:** {selected_row['충전소명']}  
        **주소:** {selected_row['주소']}  
        **상태:** {selected_row['상태']}  
        **이용제한:** {selected_row['이용제한'] if selected_row['이용제한'] else '없음'}
        """)
    

    with col1:
        # 지도 출력
        m = create_map(
            df,
            show_df,
            center_lat=show_df[show_df['충전소명'] == st.session_state['selected_station']]['위도'].values[0],
            center_lng=show_df[show_df['충전소명'] == st.session_state['selected_station']]['경도'].values[0],
            zoom_start=17
        )
        map_data = st_folium(m, height = 500, use_container_width= True,key=f"map_{st.session_state['selected_station']}")

        if map_data and map_data.get('last_object_clicked'):
            lat = map_data['last_object_clicked']['lat']
            lng = map_data['last_object_clicked']['lng']
            distance = ((show_df['위도'] - lat)**2 + (show_df['경도'] - lng)**2)
            clicked_row = show_df.iloc[distance.idxmin()]
            if clicked_row['충전소명'] != st.session_state['selected_station']:
                st.session_state['selected_station'] = clicked_row['충전소명']
                selected_row = show_df[show_df['충전소명'] == st.session_state['selected_station']].iloc[0]
                info_placeholder.markdown(f"""
                    **충전소명:** {selected_row['충전소명']}  
                    **주소:** {selected_row['주소']}  
                    **상태:** {selected_row['상태']}  
                    **이용제한:** {selected_row['이용제한'] if selected_row['이용제한'] else '없음'}
                    """)
