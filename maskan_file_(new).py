from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

class Maskan_File:
    def __init__(self, url):
        self.url = url
        
    def start_driver(self):
        self.driver = webdriver.Chrome(service=Service())
        self.driver.get(self.url)
        time.sleep(4)
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, "html.parser")

    def extract_ids(self):
        links = self.soup.find_all("a", class_="more-detail")
        seen_ids = set()
        cnt = 1
        
        for link in links:
            element_id = link.get("id", "")
            match = re.search(r'moreDetail_(\d+)', element_id)
            if match and match.group(1) not in seen_ids:
                id_number = match.group(1)
                print(cnt,":", id_number)
                seen_ids.add(id_number)
                cnt += 1
    
    def quit_driver(self):
        if self.driver:
            self.driver.quit()   
    
    def run(self):
        try:
            self.start_driver()
            self.extract_ids()
        finally:
            self.quit_driver()

if __name__ == "__main__":
    scraper = Maskan_File("https://maskan-file.ir/Site/Default.aspx")
    scraper.run()