from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

class Maskan_File:
    def __init__(self, url):
        self.url = url
        self.seen_links = set()

    def start_driver(self):
        self.driver = webdriver.Chrome(service=Service())
        self.driver.get(self.url)
        time.sleep(4)
    
    def extract_links(self, soup):
        links = soup.find_all("div", class_="btn-showdetail")
        link_list = []

        for div in links:
            onclick = div.get("onclick", "")
            if onclick:
                match = re.search(r"window\.open\('([^']+)'\)", onclick)
                if match:
                    full_link = match.group(1)
                    if full_link not in self.seen_links:
                        link_list.append(full_link)
                        self.seen_links.add(full_link)
                    
        return link_list
        
    def click_next(self):
        try:
            next_button = self.driver.find_element(By.LINK_TEXT, "مشاهده موارد بیشتر")
            next_button.click()
            return True
        except:
            return False
        
    def run(self):
        trylisten = True
        all_links = []
        try:
            self.start_driver()
            while True:
                time.sleep(1)
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                links = self.extract_links(soup)
                all_links.extend(links)
                if not self.click_next():
                    break
        finally:
            self.driver.quit()
        
        return all_links
            
if __name__ == "__main__":
    scraper = Maskan_File("https://maskan-file.ir/Site/Default.aspx")
    links = scraper.run()
    print(links)