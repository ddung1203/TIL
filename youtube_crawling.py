import pandas as pd
import time
from bs4 import BeautifulSoup as bs
import requests
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 크롤링 전 세팅
chrome_driver_path = r'D:\Downloads\chromedriver.exe'

# 크롤링 URL
# 향후 찾고 싶은 영상 URL만 변경
keyword = input('검색할 단어를 입력하세요: ')
url_path = 'https://www.youtube.com/results?search_query={}&sp=EgIYAw%253D%253D'.format(keyword)

# 댓글
comment_lst=[]
# 좋아요 개수
like_count_lst = []

# Vidoe list
tmp=[]

a = 'watch?'
b = '&'

# 크롤링 할 비디오
with Chrome(executable_path = chrome_driver_path) as driver:
	wait = WebDriverWait(driver, 20)
	driver.get(url_path)
	time.sleep(3)

	titles = driver.find_elements_by_css_selector(".yt-simple-endpoint")
	for i in titles:
		href = i.get_attribute('href')
		tmp.append(href)
	tmp = list(filter(None, tmp))
	tmp = list(set(tmp))

	url_list = [s for s in tmp if a in s]
	url_list = [s for s in url_list if b not in s]
	print(url_list)


def start(url_path):
	def infinite_loop():
		last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
		
		while True:
			driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
			time.sleep(1.0)
			new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
			if new_page_height == last_page_height:
				time.sleep(1.0)
				if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
					break
			else:
				last_page_height = new_page_height
	with Chrome(executable_path = chrome_driver_path) as driver:
	  
		wait = WebDriverWait(driver, 20)
		driver.get(url_path)
		time.sleep(3)
		
		# 무한 크롤링
		infinite_loop()

	  # 댓글 가져오기    
		try:
			for comment in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content-text')))):
				if comment.text != '':
					comment_temp = comment.text.replace('\n', ' ')
					comment_lst.append(comment_temp)
				else:
					comment_lst.append('없음')
		except:
	      # 크롤링 값이 없을 경우에
			comment_lst.append('없음')

	  # 좋아요 개수 가져오기
		try:
			for like_count in tqdm(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#vote-count-middle')))):
				if like_count.text != '':
					like_count_lst.append(like_count.text)
				else:
					like_count_lst.append('0')
		except:
	      # 좋아요 개수가 없을 경우에
			like_count_lst.append('없음')


for i in url_list:
	start(i)

#start('https://www.youtube.com/watch?v=Vy_5_WNMLck')

print('done')

# 저장 위치
save_path = r'D:\Downloads\`'

df = pd.DataFrame({
									 '댓글' : comment_lst,
                   '좋아요 개수' : like_count_lst,
                   })

# 인덱스 1부터 실행
df.index = df.index+1

# to_csv 저장
df.to_csv(save_path + '유튜브 댓글 크롤링.csv' , encoding='utf-8-sig')

print('save done')