from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime



url = 'https://www.siksinhot.com/taste?upHpAreaId=9&hpAreaId=398&isBestOrd=N'

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options)
df_titles = pd.DataFrame()


star_scores = []
reviews = []

driver.get(url)
time.sleep(10)
flag2 = True
cnt = 2
for l in [3, 6, 9]:     # 도시 Xpath 순서 번호
    driver.find_element_by_xpath('//*[@id="contents"]/div/div/div[1]/div[1]/div/div/a').click()
    time.sleep(0.2)
    driver.find_element_by_xpath(f'//*[@id="layer_area_box"]/div[2]/div[2]/div/div/div[1]/ul/li[{l}]/a/span').click()
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="layer_area_box"]/div[2]/div[2]/div/div/div[2]/ul/li[2]/a').click()
    time.sleep(0.2)
    while flag2:  #   3, 32
        cnt += 1
        flag = True
        xpath_cnt = 0
        error_cnt = 0
        error2_cnt = 0

        while flag:
            xpath_cnt += 1
            try:                                     # //*[@id="tabMove3"]/div/ul/li[1]/div/div/div[2]/p //*[@id="tabMove3"]/div/ul/li[1]/div/div/div[2]/p
                review = driver.find_element_by_xpath(f'//*[@id="tabMove3"]/div/ul/li[{xpath_cnt}]/div/div/div[2]/p').text
                review = re.compile('[^가-힣 ]').sub('', review)
                reviews.append(review)            # 리뷰 저장

                star_score = driver.find_element_by_xpath(f'//*[@id="tabMove3"]/div/ul/li[{xpath_cnt}]/div/div/div[2]/div/span/strong').text
                star_score = star_score.split('.')
                star_scores.append(star_score[0])    # 별점 저장
                error_cnt += 1

            except:
                try:
                    driver.find_element_by_xpath('//*[@id="tabMove3"]/div/a/span').click() # Xpath 가 더 존재하지 않으면 클릭
                                                # //*[@id="tabMove2"]/div/a/span         //*[@id="tabMove3"]/div/a/span
                    print('error', error_cnt)
                    time.sleep(0.2)
                    error2_cnt += 1
                    if error_cnt < 5:
                        if error2_cnt > 2:
                            break
                        else:
                            pass
                    error_cnt = 0
                except:
                    try:
                        driver.find_element_by_xpath('//*[@id="tabMove2"]/div/a/span').click()
                    except:
                        driver.find_element_by_xpath('//*[@id="contents"]/div/div/div[1]/div[1]/div/div/a').click()
                        time.sleep(0.2)
                        driver.find_element_by_xpath(
                            f'//*[@id="layer_area_box"]/div[2]/div[2]/div/div/div[2]/ul/li[{cnt}]/a').click()
                        time.sleep(0.2)
        df_section_titles = pd.DataFrame(star_scores, columns=['star_score'])
        df_section_titles['reviews'] = reviews
        df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
        df_section_titles.to_csv(f'./Crawling_data/crawling_data_{l}_{cnt}.csv', index=False)
        star_scores = []
        reviews = []
        try:
            driver.find_element_by_xpath('//*[@id="contents"]/div/div/div[1]/div[1]/div/div/a').click()
            time.sleep(0.2)
            driver.find_element_by_xpath(f'//*[@id="layer_area_box"]/div[2]/div[2]/div/div/div[2]/ul/li[{cnt}]/a').click()
            time.sleep(0.2)
        except:
            driver.get(url)
            driver.find_element_by_xpath('//*[@id="contents"]/div/div/div[1]/div[1]/div/div/a').click()
            time.sleep(0.2)
            driver.find_element_by_xpath(
                f'//*[@id="layer_area_box"]/div[2]/div[2]/div/div/div[2]/ul/li[{cnt}]/a').click()
            time.sleep(0.2)

df_section_titles = pd.DataFrame(star_scores, columns=['star_scores'])
df_section_titles['reviews'] = reviews
df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
df_titles.to_csv('./Crawling_data/siksin_crawling{}.csv'.format(
datetime.datetime.now().strftime('%Y%m%d')), index=False)

driver.close()