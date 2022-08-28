from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import requests
import time
import json

 
def get_news_list(driver):
    time.sleep(1)
    news_list = driver.find_element(By.XPATH, '//*[@id="latest-news"]/div[3]/div')
    news_html = news_list.get_attribute("innerHTML")

    soup = BeautifulSoup(news_html, "html.parser")
    news_div = soup.find_all('div', class_="media-right")

    return news_div

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://annapurnapost.com/"
response = requests.get(url)

driver.get(url)
driver.maximize_window()

# goto news hightlights page
news_highlights_button = driver.find_element(By.XPATH, '//*[@id="bs-example-navbar-collapse-1"]/div/div/ul/li[4]/a')
news_highlights_button.click()

news_div = get_news_list(driver)

news_titles = []
# click on more news if there are less than 30 articles
while len(news_titles) < 30:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1500);")
    time.sleep(1)

    extra_news_button = driver.find_element(By.CSS_SELECTOR, '#latest-news > div.container.additional-container > div > div.row.row--category-more-news > div.more.text-center > a')
    extra_news_button.click()

    news_div = get_news_list(driver)

    news_titles = []
    for div in news_div:
        news_title = div.h3.text
        if news_title not in news_titles:
            news_titles.append(news_title)

# create a dictionary to store the news
news_dict = {}
for i in range(len(news_titles)):
    news_dict[f"article_{i}"] = news_titles[i]

# store the news articles into a json file
with open("news_articles.json", "w", encoding="utf-8") as f:
    json.dump(news_dict, f, indent=3)

time.sleep(2)
driver.close()

