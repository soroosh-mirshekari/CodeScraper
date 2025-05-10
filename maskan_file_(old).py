from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

driver = webdriver.Chrome(service=Service())
driver.get("https://maskan-file.ir/Site/Default.aspx")
seen_id = set()
time.sleep(4)

def extract_id(soup):
    links = soup.find_all("a", class_="more-detail")
    cnt = 1
    for link in links:
        id = link.get("id", "")
        match = re.search(r'moreDetail_(\d+)', id)
        if match and match.group(1) not in seen_id:
            id_number = match.group(1)
            print(cnt,":", id_number)
            seen_id.add(id_number)
            cnt += 1
            
while True:
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    extract_id(soup)
    try:
        next_button = driver.find_element(By.LINK_TEXT, "مشاهده موارد بیشتر")
        next_button.click()
    except:
        break
driver.quit()