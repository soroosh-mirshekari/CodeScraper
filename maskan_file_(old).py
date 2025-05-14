from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

class Maskan_File:
    def __init__(self, url):
        self.url = url
        self.seen_ids = set()

    def start_driver(self):
        self.driver = webdriver.Chrome(service=Service())
        self.driver.get(self.url)
        time.sleep(4)
    
    def extract_ids(self, soup):
        links = soup.find_all("a", class_="more-detail")
        cnt = len(self.seen_ids) + 1

        for link in links:
            element_id = link.get("id", "")
            match = re.search(r'moreDetail_(\d+)', element_id)
            if match:
                id_number = match.group(1)
                if id_number not in self.seen_ids:
                    print(cnt ,":", id_number)
                    self.seen_ids.add(id_number)
                    cnt += 1
                    
    def click_next(self):
        try:
            next_button = self.driver.find_element(By.LINK_TEXT, "مشاهده موارد بیشتر")
            next_button.click()
            return True
        except:
            return False
        
    def run(self):
        try:
            self.start_driver()
            while True:
                time.sleep(1)
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                self.extract_ids(soup)
                if not self.click_next():
                    break
        finally:
            self.driver.quit()
            
if __name__ == "__main__":
    scraper = Maskan_File("https://maskan-file.ir/Site/Default.aspx")
    scraper.run() 