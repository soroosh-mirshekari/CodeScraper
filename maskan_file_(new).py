from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

driver = webdriver.Chrome(service=Service())
driver.get("https://maskan-file.ir/Site/Default.aspx")
time.sleep(4)

def extract_id(soup):
    links = soup.find_all("a", class_="more-detail")
    seen_id = set()
    cnt = 1
    for link in links:
        id = link.get("id", "")
        match = re.search(r'moreDetail_(\d+)', id)
        if match and match.group(1) not in seen_id:
            id_number = match.group(1)
            print(cnt,":", id_number)
            seen_id.add(id_number)
            cnt += 1
            
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
extract_id(soup)
driver.quit()