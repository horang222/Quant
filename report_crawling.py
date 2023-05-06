
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager # webdriver_manager 처음 실행할 때는 다운받느라 조금 시간이 걸릴 수 있음

# 브라우저 꺼짐 방지
options = Options()
options.add_experimental_option('detach', True)

# 불필요한 에러 메시지 없애기
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

cnt = 0

domains = []
titles = []
author = []
firms = []
dates = []
for page_no in range(1, 357):
    cnt += 1
    url = f'https://www.paxnet.co.kr/stock/report/report?menuCode=3333&currentPageNo={page_no}&reportId=140703&searchKey=category&searchValue='
    driver.get(url)
    time.sleep(3)
    print(f'{cnt}페이지 로드 완료, {cnt}페이지 크롤링 시작')

    if page_no != 356:

        for n in range(2, 32):
            temp = driver.find_element(By.CSS_SELECTOR, f'#contents > div.cont-area > div.board-type > ul > li:nth-child({n})')
            temp_list = temp.text.split('\n')
            domains.append(temp_list[0])
            titles.append(temp_list[1])

            # record += [temp_list[0], temp_list[1]]
            temp_infos = temp_list[2].split(' ')
            author.append(temp_infos[0])
            firms.append(temp_infos[1])
            date = pd.to_datetime(temp_infos[-1])
            dates.append(date)
            
    else:
        for n in range(2, 29):
            temp = driver.find_element(By.CSS_SELECTOR, f'#contents > div.cont-area > div.board-type > ul > li:nth-child({n})')
            temp_list = temp.text.split('\n')
            domains.append(temp_list[0])
            titles.append(temp_list[1])

            # record += [temp_list[0], temp_list[1]]
            temp_infos = temp_list[2].split(' ')
            author.append(temp_infos[0])
            firms.append(temp_infos[1])
            date = temp_infos[-1]
            date = pd.to_datetime(date)
            dates.append(date)

driver.quit()

# cols = ['업종', '제목', '애널리스트', '증권사', '작성일']
df = pd.DataFrame()
df['업종'] = domains
df['제목'] = titles
df['작성자'] = author
df['증권사'] = firms
df['작성일'] = dates
# df = pd.DataFrame(data, index=False)

print('데이터프레임 생성 완료!!!')

df.to_csv("./data/report.csv", encoding='utf-8', index=False)

print('데이터프레임 저장 완료!!!')