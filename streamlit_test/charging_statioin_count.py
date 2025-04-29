import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ChargningStationCount:

    def __init__(self):
        self.csv_dir = './EV_charging_station_info.csv'
        self.csv_data = pd.read_csv(self.csv_dir, encoding='cp949')
        self.keys = ['서울', '인천', '경기', '강원', '충남', '충북', '대전', '세종', '경북', '대구', '전북', '전남', '광주', '경남', '부산', '울산', '제주']

        self.count = self.count_station(self.csv_data)
        self.count_no = self.count_no_station(self.csv_data)
        

    def count_station(self, data):
        ers = []

        count_seoul = 0
        count_incheon = 0
        count_gyeonggi = 0
        count_gangwon = 0
        count_chungnam = 0
        count_chungbuk = 0
        count_daejeon = 0
        count_sejong = 0
        count_gyengbuk = 0
        count_daegu = 0
        count_jeonbuk = 0
        count_jeonnam = 0
        count_gwangju = 0
        count_gyengnam = 0
        count_busan = 0
        count_ulsan = 0
        count_jeju = 0

        for index, i in data.iterrows():

            if '서울' in i['시도']:
                count_seoul += 1

            elif '인천' in i['시도']:
                count_incheon += 1

            elif '경기' in i['시도']:
                count_gyeonggi += 1

            elif '강원' in i['시도']:
                count_gangwon += 1

            elif '충청남' in i['시도']:
                count_chungnam += 1

            elif '충청북' in i['시도']:
                count_chungbuk += 1
            
            elif '대전' in i['시도']:
                count_daejeon += 1

            elif '세종' in i['시도']:
                count_sejong += 1

            elif '경상북' in i['시도']:
                count_gyengbuk += 1

            elif '대구' in i['시도']:
                count_daegu += 1

            elif '전북' in i['시도']:
                count_jeonbuk += 1 

            elif '전라남' in i['시도']:
                count_jeonnam += 1

            elif '광주' in i['시도']:
                count_gwangju += 1

            elif '경상남' in i['시도']:
                count_gyengnam += 1

            elif '부산' in i['시도']:
                count_busan += 1

            elif '울산' in i['시도']:
                count_ulsan += 1

            elif '제주' in i['시도']:
                count_jeju += 1

            else:
                ers.append(i)

        
        values = [count_seoul, count_incheon, count_gyeonggi, count_gangwon, count_chungnam, count_chungbuk, count_daejeon, count_sejong, count_gyengbuk, count_daegu, count_jeonbuk, count_jeonnam, count_gwangju, count_gyengnam, count_busan, count_ulsan, count_jeju]

        dict_count = dict(zip(self.keys, values))
        
        return dict_count
    
    def count_no_station(self, data):
        
        ers = []
        count_no = 0
        count_seoul_no = 0
        count_incheon_no = 0
        count_gyeonggi_no = 0
        count_gangwon_no = 0
        count_chungnam_no = 0
        count_chungbuk_no = 0
        count_daejeon_no = 0
        count_sejong_no = 0
        count_gyengbuk_no = 0
        count_daegu_no = 0
        count_jeonbuk_no = 0
        count_jeonnam_no = 0
        count_gwangju_no = 0
        count_gyengnam_no = 0
        count_busan_no = 0
        count_ulsan_no = 0
        count_jeju_no = 0

        for index, i in data.iterrows():

            if i['시설구분(대)'] == '공동주택시설' or i['이용자제한'] == '이용자제한' or i["이용자제한"] == '비공개':
                count_no += 1
                if '서울' in i['시도']:
                    count_seoul_no += 1

                elif '인천' in i['시도']:
                    count_incheon_no += 1

                elif '경기' in i['시도']:
                    count_gyeonggi_no += 1

                elif '강원' in i['시도']:
                    count_gangwon_no += 1

                elif '충청남' in i['시도']:
                    count_chungnam_no += 1

                elif '충청북' in i['시도']:
                    count_chungbuk_no += 1
                
                elif '대전' in i['시도']:
                    count_daejeon_no += 1

                elif '세종' in i['시도']:
                    count_sejong_no += 1

                elif '경상북' in i['시도']:
                    count_gyengbuk_no += 1

                elif '대구' in i['시도']:
                    count_daegu_no += 1

                elif '전북' in i['시도']:
                    count_jeonbuk_no += 1 

                elif '전라남' in i['시도']:
                    count_jeonnam_no += 1

                elif '광주' in i['시도']:
                    count_gwangju_no += 1

                elif '경상남' in i['시도']:
                    count_gyengnam_no += 1

                elif '부산' in i['시도']:
                    count_busan_no += 1

                elif '울산' in i['시도']:
                    count_ulsan_no += 1

                elif '제주' in i['시도']:
                    count_jeju_no += 1

                else:
                    ers.append(i)

        values = [count_seoul_no, count_incheon_no, count_gyeonggi_no, count_gangwon_no, count_chungnam_no, count_chungbuk_no, count_daejeon_no, count_sejong_no, count_gyengbuk_no, count_daegu_no, count_jeonbuk_no, count_jeonnam_no, count_gwangju_no, count_gyengnam_no, count_busan_no, count_ulsan_no, count_jeju_no]

        dict_count = dict(zip(self.keys, values))
        
        return dict_count
    

    def make_graph(self):

        total_values = list(self.count.values())
        restricted_values = list(self.count_no.values())
        labels = self.keys

        plt.rc('font', family='Malgun Gothic')
        plt.rcParams['axes.unicode_minus'] = False

        fig, ax = plt.subplots(figsize=(16, 8))

        max_total = max(total_values)  
        scale_factor = 1  


        for i, (total_value, restricted_value, label) in enumerate(zip(total_values, restricted_values, labels)):
            available_value = total_value - restricted_value
            
            ax.add_patch(plt.Rectangle((i, 0), 0.8, total_value * scale_factor, edgecolor='black', facecolor='none', linewidth=1.5))
            
            ax.add_patch(plt.Rectangle((i, 0), 0.8, restricted_value * scale_factor, color='darkorange'))
            
            ax.add_patch(plt.Rectangle((i, restricted_value * scale_factor), 0.8, available_value * scale_factor, color='royalblue'))
            
            ax.text(i + 0.4, restricted_value * scale_factor / 2, f'{restricted_value}', 
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold')
            
            ax.text(i + 0.4, restricted_value * scale_factor + available_value * scale_factor / 2, f'{available_value}', 
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold')
            
            ax.text(i + 0.4, -max_total * 0.03, label,
                    ha='center', va='top', fontsize=11, rotation=45)

        ax.annotate('이용 가능', xy=(len(labels), max_total * 0.75), xytext=(len(labels) + 1, max_total * 0.75),
                    va='center', ha='left', fontsize=12, color='royalblue',
                    arrowprops=dict(arrowstyle='-', color='royalblue'))

        ax.annotate('이용 제한', xy=(len(labels), max_total * 0.25), xytext=(len(labels) + 1, max_total * 0.25),
                    va='center', ha='left', fontsize=12, color='red',
                    arrowprops=dict(arrowstyle='-', color='red'))

        ax.set_xlim(-0.5, len(labels)+2)
        ax.set_ylim(-max_total * 0.1, max_total * 1.1)
        ax.axis('off')

        plt.tight_layout()
        plt.show()


c = ChargningStationCount()
c.make_graph()