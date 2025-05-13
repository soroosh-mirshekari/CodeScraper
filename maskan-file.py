import requests
from bs4 import BeautifulSoup

class RealEstateScraper:
    def __init__(self, property_code):
        self.property_code = property_code
        self.base_url = "https://maskan-file.ir//Site/Homes.aspx?codeFile="
        self.data = {
            "file_code": property_code,
            "title": "",
            "address": "",
            "total_price": "",
            "price_per_meter": "",
            "mortgage": "",  
            "rent": "",
            "area": "",
            "number_of_rooms": "",
            "year_of_manufacture": "",
            "facilities": "",
            "pictures": [],
            "is_rental": False
        }

    def scrape(self):
        try:
            url = self.base_url + str(self.property_code)
            response = requests.get(url)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, 'html.parser')

            property_type_div = soup.select_one('div.col-md-4.col-sm-4.col-lg-3.col-xs-12.col-12')
            if property_type_div and "رهن و اجاره" in property_type_div.get_text(strip=True):
                self.data["is_rental"] = True
            
            self.data["title"] = self._extract_text(soup, 'h4.adds')
            self._extract_address(soup)
            self._extract_pricing_info(soup)
            self._extract_property_details(soup)
#            self.data["pictures"] = self._scrape_images(soup)

            return self.data

        except requests.exceptions.RequestException as e:
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
            self.data["mortgage"] = self._extract_text(soup, 'div.col-md-2.col-sm-2.col-lg-5.card-body.ForPrint h3')
            self.data["rent"] = self._extract_text(soup, 'div.col-md-2.col-sm-2.col-lg-5.card-body.ForPrint h5 span')
        else:
            self.data["total_price"] = self._extract_text(soup, 'div.card-body h4')
            self.data["price_per_meter"] = self._extract_text(soup, 'div.col-md-6.col-sm-6.col-lg-6.col-xs-12 > span.spanMatns')

    def _extract_property_details(self, soup):
        self.data["area"] = self._extract_text(soup, 'div.Metrazh.matns2 span.matns2')
        
        rooms_div = soup.select_one('div.col-md-4.col-sm-4.col-lg-4.col-xs-12:-soup-contains("تعداد خواب")')
        self.data["number_of_rooms"] = self._extract_text(rooms_div, 'span.spanMatns').strip() if rooms_div else ""
        
        year_div = soup.select_one('div.col-md-4.col-sm-4.col-lg-4.col-xs-12:-soup-contains("سن بنا")')
        self.data["year_of_manufacture"] = self._extract_text(year_div, 'span.spanMatns').strip() if year_div else ""
        
        facilities_div = soup.select_one('div.Facilities')
        self.data["facilities"] = [item.get_text(strip=True) for item in facilities_div.select('li.lis')] if facilities_div else []

    def _extract_text(self, parent, selector):
        element = parent.select_one(selector)
        return element.get_text(strip=True) if element else ""

#    def _scrape_images(self, soup):
        try:
            all_images = set()
            
            main_images = soup.select('div.mySlides img.imgslides[src]')
            thumb_images = soup.select('img.demo[src]')
            
            for img in main_images + thumb_images:
                src = img['src']
                if 'index.png' not in src:
                    if src.startswith('../../../../../'):
                        src = "https://maskan-file.ir" + src.replace('../../../../../', '/')
                    all_images.add(src)
            
            return list(all_images)
        
        except Exception as e:
            print(f"Error extracting images: {e}")
            return []

if __name__ == "__main__":
    scraper = RealEstateScraper(input())
    property_data = scraper.scrape()
    print(property_data if property_data else "Failed to retrieve property data")