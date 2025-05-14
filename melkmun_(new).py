import requests
import json

class Melkemun:
    def __init__(self, city_id=2, date_from="2024-05-14", date_to="2025-05-10", limit=20):
        self.base_url = "https://api.melkemun.com/v1/estates/"
        self.city_id = city_id
        self.date_from = date_from
        self.date_to = date_to
        self.limit = limit
        self.seen_ids = set()
        self.headers = {
            "Referer": "https://melkemun.com/",
            "Sec-CH-UA": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        }
    def build_url(self):
        return (
            f"{self.base_url}?ordering=-published_at"
            f"&limit={self.limit}"
            f"&published_at__gte={self.date_from}T00:00:00.000Z"
            f"&published_at__lte={self.date_to}T23:59:59.000Z"
            f"&loc_city_id={self.city_id}"
        )
        
    def fetch_data(self):
        url = self.build_url()
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print("خطا در دریافت داده:", response.status_code)
            return []

    def process_results(self, results):
        cnt = 1
        for item in results:
            estate_id = item.get("id")
            if estate_id not in self.seen_ids:
                print(cnt, ":", estate_id)
                self.seen_ids.add(estate_id)
                cnt += 1

    def run(self):
        results = self.fetch_data()
        self.process_results(results)

if __name__ == "__main__":
    scraper = Melkemun()
    scraper.run()