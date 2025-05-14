import requests
import time

class Estate:
    def __init__(self, data):
        self.data = data

    def display(self, index=None):
        if index is not None:
            print(index)
        print("ID:", self.data.get("id"))
        print("Address:", self.data.get("loc_address", "N/A"))
        print("Price:", self.data.get("price", "N/A"))
        # اضافه شده: اجاره اگر آگهی از نوع اجاره‌ای باشه
        rent = self.data.get("deposit") if self.data.get("type_id") == 4 else "N/A"
        print("Rent (Deposit):", rent)
        print("Area (lot):", self.data.get("lot", "N/A"))
        print("Rooms:", self.data.get("rooms", "N/A"))
        print("Built Year:", self.data.get("built_year", "N/A"))
        print("Published At:", self.data.get("published_at", "N/A"))
        print("Seller:", self.data.get("seller_name", "N/A"))
        print("Description:", self.data.get("description", "N/A"))
        print("Latitude:", self.data.get("loc_latitude", "N/A"))
        print("Longitude:", self.data.get("loc_longitude", "N/A"))
        print("Elevator:", self.data.get("ame_elevator", "N/A"))
        print("Parking:", self.data.get("ame_parking", "N/A"))
        print("Bathroom:", self.data.get("ame_bathroom", "N/A"))
        print("Security Guard:", self.data.get("ame_security_guard", "N/A"))
        print("Status ID:", self.data.get("status_id", "N/A"))
        print("-" * 50)

class EstateFetcher:
    BASE_URL = "https://api.melkemun.com/v1/estates/"
    HEADERS = {
        "Origin": "https://melkemun.com",
        "Referer": "https://melkemun.com/",
        "User-Agent": "Mozilla/5.0",
    }
    def __init__(self, total=20, limit=20, city_id=2,
        date_from="2024-05-19T00:00:00.000Z",
        date_to="2025-05-15T23:59:59.000Z"):
        self.total = total
        self.limit = limit
        self.city_id = city_id
        self.date_from = date_from
        self.date_to = date_to

    def fetch_all_estates(self):
        all_estates = []
        for offset in range(0, self.total, self.limit):
            estates = self._fetch(offset)
            print(f"Got {len(estates)} items from offset {offset}")
            all_estates.extend(Estate(item) for item in estates)
            time.sleep(1)
        return all_estates

    def _fetch(self, offset):
        params = {
            "ordering": "-published_at",
            "limit": self.limit,
            "offset": offset,
            "loc_city_id": self.city_id,
            "published_at__gte": self.date_from,
            "published_at__lte": self.date_to,
        }
        response = requests.get(self.BASE_URL, headers=self.HEADERS, params=params)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"Failed to fetch offset {offset}, status: {response.status_code}")
            return []

if __name__ == "__main__":
    fetcher = EstateFetcher(total = 20)
    estates = fetcher.fetch_all_estates()
    for idx, estate in enumerate(estates, start = 1):
        estate.display(index=idx)
