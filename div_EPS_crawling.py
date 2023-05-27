import time
import numpy as np
import pandas as pd
import OpenDartReader
import FinanceDataReader as fdr

my_api = '' # 소연 api key
# my_api = '' # 내 api key

dart = OpenDartReader(my_api)

def find_div_and_EPS(stock, year):
    output = dict()
    try:
        _report = dart.report(stock, "배당", year, '11011')
    except:
        _report = None
        
    if (_report is None) or (len(_report) == 0):
        output['주당배당금'] = np.nan, np.nan, np.nan 
        output['주당순이익'] = np.nan, np.nan, np.nan
        return output
    
    else:
        # 주당 배당금 정리
        div_temp = _report.loc[_report["se"] == "주당 현금배당금(원)"].iloc[0]
        div_row = div_temp[['thstrm', 'frmtrm', 'lwfr']].values
        
        cur_div = int(div_row[0].replace('-','0').replace(',',''))
        pre_div = int(div_row[1].replace('-','0').replace(',',''))
        spre_div = int(div_row[2].replace('-','0').replace(',',''))

        output['주당배당금'] = spre_div, pre_div, cur_div

        # 주당순이익 정리
        EPS_temp = _report.loc[_report["se"].str.contains("주당순이익")].iloc[0]
        EPS_row = EPS_temp[['thstrm', 'frmtrm', 'lwfr']].values

        cur_EPS = int(EPS_row[0].replace('-', '0').replace(',',''))
        pre_EPS = int(EPS_row[1].replace('-', '0').replace(',',''))
        spre_EPS = int(EPS_row[2].replace('-', '0').replace(',',''))
        output['주당순이익']= spre_EPS, pre_EPS, cur_EPS

        return output
    

stock_list = pd.read_csv('./data/stock_list.txt', sep='\t')
stock_name_list = stock_list['Name'].values

div_data = []
EPS_data = []

for idx, name in enumerate(stock_name_list):
    print(idx + 1, '/', len(stock_name_list))

    div_record = [name]
    EPS_record = [name]
    
    for year in [2016, 2019, 2022]:
        try:
            output = find_div_and_EPS(name, year)
        except:
            pass
        
        spre_divs, pre_divs, cur_divs = output['주당배당금']
        spre_EPS, pre_EPS, cur_EPS = output['주당순이익']

        div_record += [spre_divs, pre_divs, cur_divs]
        EPS_record += [spre_EPS, pre_EPS, cur_EPS]

        
    div_data.append(div_record)
    EPS_data.append(EPS_record)
        

columns = ['stock_name', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']

df_div = pd.DataFrame(div_data, columns=columns)
df_EPS = pd.DataFrame(EPS_data, columns=columns)

df_div.sort_values(by='stock_name', ascending=True, ignore_index=True, inplace=True)
df_EPS.sort_values(by='stock_name', ascending=True, ignore_index=True, inplace=True)

df_div.to_csv("./data/dividends.csv", encoding='utf-8', index=False)
df_EPS.to_csv("./data/EPS.csv", encoding='utf-8', index=False)