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
        self.html = self.driver.page_source
        self.soup = BeautifulSoup(self.html, "html.parser")

    def extract_links(self):
        links = self.soup.find_all("div", class_="btn-showdetail")
        link_list = []
        
        for div in links:
            onclick = div.get("onclick", "")
            if onclick:
                match = re.search(r"window\.open\('([^']+)'\)", onclick)
                if match:
                    full_link = match.group(1)
                    if full_link and full_link not in self.seen_links:
                        link_list.append(full_link)
                        self.seen_links.add(full_link)
        
        return link_list
    
    def quit_driver(self):
        if self.driver:
            self.driver.quit()   
    
    def run(self):
        try:
            self.start_driver()
            return self.extract_links()
        finally:
            self.quit_driver()

if __name__ == "__main__":
    detector = Maskan_File("https://maskan-file.ir/Site/Default.aspx")
    links = detector.run()
    print(links)