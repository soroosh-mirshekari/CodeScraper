from bs4 import BeautifulSoup
from selenium import webdriver
import time  
from maskan_file_cleaner import RealEstateCleaner

class RealEstateScraper:
    def __init__(self, property_url):
        self.property_url = property_url
        self.data = {
            "file_code": "",
            "title": "",
            "address": "",
            "total_price": "",
            "price_per_meter": "",
            "mortgage": "",  
            "rent": "",
            "area": "",
            "number_of_rooms": "",
            "year_of_manufacture": "",
            "facilities": [],
            "pictures": [],
            "is_rental": False
        }

    def scrape(self):
        try:
            url = self.property_url
            # Getting page source without opening chrome visually
            options = webdriver.ChromeOptions()
            options.add_argument('--headless') 
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
        
            driver = webdriver.Chrome(options=options)
            driver.get(url)

            # One step ahead of internet operators
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()  

            # Extract file code from URL
            import re
            match = re.search(r'Homes/(\d+)/', url)
            self.data["file_code"] = match.group(1) 

            property_type_div = soup.select_one('div.col-md-4.col-sm-4.col-lg-3.col-xs-12.col-12')
            if property_type_div and "رهن و اجاره" in property_type_div.get_text(strip=True):
                self.data["is_rental"] = True
            
            self.data["title"] = self._extract_text(soup, 'h4.adds')
            self._extract_address(soup)
            self._extract_pricing_info(soup)
            self._extract_property_details(soup)
            self.data["pictures"] = self._scrape_images(soup)

            return self.data

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def _extract_address(self, soup):
        address_div = soup.select_one('div.adds:-soup-contains("منطقه")')
        if address_div:
            part1 = self._extract_text(address_div, 'p.text-customm2.matns')
            part2 = self._extract_text(address_div, 'h4.adds')
            self.data["address"] = f"{part1} {part2}".strip()

    def _extract_pricing_info(self, soup):
        if self.data["is_rental"]:
            mortgage_element = soup.select_one('div.col-md-2.col-sm-2.col-lg-5.card-body.ForPrint h3')
            self.data["mortgage"] = mortgage_element.get_text(strip=True) if mortgage_element else ""
            
            rent_element = soup.select_one('div.col-md-2.col-sm-2.col-lg-5.card-body.ForPrint h5 span')
            self.data["rent"] = rent_element.get_text(strip=True) if rent_element else ""
        else:
            total_price_element = soup.select_one('div.card-body h4')
            self.data["total_price"] = total_price_element.get_text(strip=True) if total_price_element else ""
            
            price_per_meter_element = soup.select_one('div.col-md-6.col-sm-6.col-lg-6.col-xs-12 > span.spanMatns')
            self.data["price_per_meter"] = price_per_meter_element.get_text(strip=True) if price_per_meter_element else ""

    def _extract_property_details(self, soup):
        area_element = soup.select_one('div.Metrazh.matns2 span.matns2')
        self.data["area"] = area_element.get_text(strip=True) if area_element else ""
        
        rooms_div = soup.select_one('div.col-md-4.col-sm-4.col-lg-4.col-xs-12:-soup-contains("تعداد خواب")')
        self.data["number_of_rooms"] = self._extract_text(rooms_div, 'span.spanMatns').strip() if rooms_div else ""
        
        year_div = soup.select_one('div.col-md-4.col-sm-4.col-lg-4.col-xs-12:-soup-contains("سن بنا")')
        self.data["year_of_manufacture"] = self._extract_text(year_div, 'span.spanMatns').strip() if year_div else ""
        
        facilities_div = soup.select_one('div.Facilities')
        if facilities_div:
            self.data["facilities"] = [item.get_text(strip=True) for item in facilities_div.select('li.lis')]
        else:
            self.data["facilities"] = []

    # Helper method to safely extract text using a CSS selector
    def _extract_text(self, parent, selector):
        if parent is None:
            return ""
        element = parent.select_one(selector)
        return element.get_text(strip=True) if element else ""

    def _scrape_images(self, soup):
        try:
            all_images = set()
            main_images = soup.select('div.mySlides img[src]')
            
            for img in main_images:
                src = img.get('src', '')
                if 'index.png' not in src and src:
                    # Normalize relative URLs
                    if src.startswith('../../../../../'):
                        src = "https://maskan-file.ir" + src.replace('../../../../../', '/')
                    elif not src.startswith(('http://', 'https://')):
                        src = "https://maskan-file.ir" + src if src.startswith('/') else f"https://maskan-file.ir/{src}"
                    all_images.add(src)
            
            return list(all_images)
        
        except Exception as e:
            print(f"Error extracting images: {e}")
            return []

if __name__ == "__main__":
    scraper = RealEstateScraper(input("Enter property URL: "))
    property_data = scraper.scrape()
    print(property_data if property_data else "Failed to retrieve property data")
    cleaner = RealEstateCleaner()
    cleaned_data = cleaner.clean(property_data)
    print(cleaned_data)
