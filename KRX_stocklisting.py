import pandas as pd
import numpy as np
import FinanceDataReader as fdr

# 한국거래소(KRX)에 있는 모든 종목 불러오기
df_krx = fdr.StockListing('KRX')

# 코넥스 종목 제외
stock_list = df_krx.loc[df_krx['Market'].isin(['KOSPI', 'KOSDAQ'])]

# 보통주가 아닌 종목 제외
stock_list_copy = stock_list.loc[~stock_list['Name'].str.contains('전환')]
stock_list_copy = stock_list_copy.loc[~stock_list_copy['Name'].str.contains('스팩')]
stock_list_copy = stock_list_copy.loc[~stock_list_copy['Name'].str.endswith(('우', '우B', '우C', '우D'))]

# 종목 정보 내보내기
stock_list_copy.to_csv('./data/stock_list.txt',sep='\t', encoding='utf-8', index=False)
# stock_list 파일을 csv가 아닌 txt 파일로 만드는 이유
# : 엑셀 형식으로 데이터를 저장하면 0으로 시작하는 값은 자동으로 0이 생략되어 나타나기 때문.
#  이 경우 종목코드를 불러오는 데 오류가 생길 수 있음.
print('KRX 종목 정보 데이터프레임 생성 완료!!!')