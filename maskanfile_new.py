from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

driver = webdriver.Chrome(service=Service())
driver.get("https://maskan-file.ir/Site/Default.aspx")
time.sleep(4)

def extract_ids(soup):
    links = soup.find_all("a", class_="more-detail")
    cnt = 1
    for link in links:
        id_attr = link.get("id", "")
        match = re.search(r'moreDetail_(\d+)', id_attr)
        if match:
            ad_id = match.group(1)
            print(cnt,":", ad_id)
            cnt += 1
            
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
extract_ids(soup)

driver.quit()