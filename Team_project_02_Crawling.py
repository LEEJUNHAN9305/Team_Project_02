from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages = [110, 110, 110, 78, 110, 66]

url = 'https://www.siksinhot.com/taste?upHpAreaId=9&hpAreaId=398&isBestOrd=N'

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)
df_titles = pd.DataFrame()



driver.get(url)
time.sleep(10)
for i in range(3, 29):
    driver.find_element_by_xpath('//*[@id="contents"]/div/div/div[1]/div[1]/div/div/a"]').click()
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="layer_area_box"]/div[2]/div[2]/div/div/div[2]/ul/li[{}]/a').format(i).click()
    time.sleep(0.2)
    titles = []
#     for j in range(1,pages[i]+1):
#         url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(i, j)
#         driver.get(url)
#         time.sleep(0.2)
#
#         for k in range(1, 5):
#             for l in range(1, 6):
#                 x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(k, l)
#                 try:
#                     title = driver.find_element_by_xpath(x_path).text
#                     title = re.compile('[^가-힣 ]').sub('', title)
#                     titles.append(title)
#                 except NoSuchElementException as e:
#                     time.sleep(0.5)
#                     try:
#                         title = driver.find_element_by_xpath(x_path).text
#                         title = re.compile('[^가-힣 ]').sub('', title)
#                         titles.append(title)
#                     except:
#                         try:
#                             x_path = '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt/a'.format(k, l)
#                             title = re.compile('[^가-힣 ]').sub('', title)
#                             titles.append(title)
#                         except:
#                             print('no such enlement')
#                 except StaleElementReferenceException as e:
#                     print(e)
#                     print(category[i], j, 'page', k * l)
#                 except:
#                     print('error')
#         if j % 30 == 0:
#             df_section_titles = pd.DataFrame(titles, columns=['titles'])
#             df_section_titles['category'] = category[i]
#             df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
#             df_section_titles.to_csv('./crawling_data/crawling_data_{}_{}_{}.csv'.format(category[i], j-29, j), index=False)
#             titles = []
#     df_section_titles = pd.DataFrame(titles, columns=['titles'])
#     df_section_titles['category'] = category[i]
#     df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
#     df_section_titles.to_csv('./crawling_data/crawling_data_{}_last.csv'.format(category[i]), index=False)
#     titles = []
# df_section_titles = pd.DataFrame(titles, columns=['titles'])
# df_section_titles['category'] = category[i]
# df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
# df_titles.to_csv('./crawling_data/naver_news_titles_{}.csv'.format(
#     datetime.datetime.now().strftime('%Y%m%d')), index=False)
# driver.close()