import mysql.connector, os
import pandas as pd
from geopy.distance import geodesic
from dotenv import load_dotenv

load_dotenv()
DB_SERVER_CONFIG_HOST = os.getenv('DB_SERVER_CONFIG_HOST')
DB_SERVER_CONFIG_USER = os.getenv('DB_SERVER_CONFIG_USER')
DB_SERVER_CONFIG_PASSWORD = os.getenv('DB_SERVER_CONFIG_PASSWORD')
DB_SERVER_CONFIG_PORT = os.getenv('DB_SERVER_CONFIG_PORT')

db_server_config = {
    'host': DB_SERVER_CONFIG_HOST,
    'user': DB_SERVER_CONFIG_USER,
    'password': DB_SERVER_CONFIG_PASSWORD,
    'port': DB_SERVER_CONFIG_PORT

}

db_name = 'ev_charger_db'
full_db_config = db_server_config.copy()
full_db_config['database'] = db_name

def setup_database_and_table():
    try:
        conn = mysql.connector.connect(**db_server_config)
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE DATABASE IF NOT EXISTS {db_name}
            DEFAULT CHARACTER SET utf8mb4
            DEFAULT COLLATE utf8mb4_general_ci;
        ''')
        conn.commit()
        cursor.close()
        conn.close()

        conn = mysql.connector.connect(**full_db_config)
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS charger_info;')

        cursor.execute('''
            CREATE TABLE charger_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                충전소명 VARCHAR(255),
                주소 VARCHAR(255),
                위도 FLOAT,
                경도 FLOAT,
                상태 VARCHAR(50),
                이용제한 VARCHAR(255),
                급속충전량 VARCHAR(255),
                충전기타입 VARCHAR(255)
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f" setup_database_and_table Error: {e}")

def clear_table():
    try:
        conn = mysql.connector.connect(**full_db_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM charger_info')
        conn.commit()
        cursor.close()
        conn.close()
    
    except Exception as e:
        print(f"clear_table Error: {e}")

def insert_data(df):
    try:
        conn = mysql.connector.connect(**full_db_config)
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO charger_info (충전소명, 주소, 위도, 경도, 상태, 이용제한, 급속충전량, 충전기타입)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (row['충전소명'], row['주소'], row['위도'], row['경도'], row['상태'], row['이용제한'], row['급속충전량'], row['충전기타입']))
        conn.commit()
        cursor.close()
        conn.close()
    
    except Exception as e:
        print(f"insert_data Error: {e}")

def fetch_all_stations():
    try:
        conn = mysql.connector.connect(**full_db_config)
        query = '''
            SELECT 충전소명, 주소, 위도, 경도, 상태, 이용제한, 급속충전량, 충전기타입 FROM charger_info
        '''
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"fetch_all_stations Error: {e}")
        return pd.DataFrame()

def calculate_distance(lat1, lon1, lat2, lon2):
    try:
        return geodesic((lat1, lon1), (lat2, lon2)).km
    except Exception as e:
        print(f"calculate_distance Error: {e}")
        return 0

def filter_nearby_stations(selected_station, all_stations, radius_km=2):
    center_lat = selected_station['위도']
    center_lon = selected_station['경도']
    nearby = []

    for _, row in all_stations.iterrows():
        dist = calculate_distance(center_lat, center_lon, row['위도'], row['경도'])
        if dist <= radius_km:
            nearby.append(row)

    return pd.DataFrame(nearby)

def sql_to_csv():
    conn = mysql.connector.connect(**full_db_config)

    query = "SELECT * FROM charger_info"
    df = pd.read_sql(query, conn)

    df.to_csv('charger_info2.csv', index=False, encoding='utf-8-sig')

    conn.close()
