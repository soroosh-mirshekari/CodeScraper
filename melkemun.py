import requests

class Estate:
    """
    Represents a single real estate listing, with formatting logic
    for extracting required fields from raw API data.
    """
    
    STATUS_MAP = {
        0: "فروش",
        1: "رهن و اجاره",
        2: "رهن کامل",
        3: "پیش فروش",
        5: "مشارکت",
        6: "اجاره موقت"
    }

    TYPE_MAP = {
        0: "آپارتمان",
        1: "ویلایی",
        2: "زمین",
        3: "ویلا",
        4: "تجاری",
        5: "سوییت",
        6: "اداری",
        7: "باغ"
    }

    def __init__(self, raw_data):
        """
        Initialize an Estate object from raw dictionary data returned by the API.
        """
        self.raw_data = raw_data
        self.status_id = raw_data.get("status_id")
        self.type_id = raw_data.get("type_id")
        self.is_rental = self.status_id in [1, 2, 6]

    def get_title(self):
        """
        Compose a title based on transaction type and building type.
        """
        status_text = self.STATUS_MAP.get(self.status_id, "نامشخص")
        type_text = self.TYPE_MAP.get(self.type_id, "نامشخص")
        return f"{status_text} {type_text}"

    def to_dict(self):
        """
        Convert the estate data into the target dictionary structure.
        """
        return {
            "file_code": str(self.raw_data.get("id", "")),
            "title": self.get_title(),
            "address": self.raw_data.get("loc_address", ""),
            "total_price": "" if self.is_rental else str(self.raw_data.get("price", "")),
            "price_per_meter": "" if self.is_rental else str(self.raw_data.get("price_per_meter", "")),
            "mortgage": str(self.raw_data.get("deposit", "")) if self.is_rental else "",
            "rent": str(self.raw_data.get("price", "")) if self.is_rental else "",
            "area": str(self.raw_data.get("lot", "")),
            "number_of_rooms": str(self.raw_data.get("rooms", "")),
            "year_of_manufacture": str(self.raw_data.get("built_year", "")),
            "facilities": [
                key.replace("ame_", "")
                for key, value in self.raw_data.items()
                if key.startswith("ame_") and value is True
            ],
            "pictures": [],  # Website has no picture
            "is_rental": self.is_rental
        }


class EstateFetcher:
    """
    Handles fetching real estate listings from melkemun.com public API.
    """

    BASE_URL = "https://api.melkemun.com/v1/estates/"
    HEADERS = {
        "Origin": "https://melkemun.com",
        "Referer": "https://melkemun.com/",
        "User-Agent": "Mozilla/5.0",
    }

    def __init__(self, city_id=2, date_from="2024-05-19T00:00:00.000Z",
                 date_to="2025-05-15T23:59:59.000Z"):
        """
        Initialize the fetcher with optional filters for city and date range.
        """
        self.city_id = city_id
        self.date_from = date_from
        self.date_to = date_to

    def fetch(self, limit=20, offset=0):
        """
        Fetch a list of estate records from the API with pagination.
        """
        params = {
            "ordering": "-published_at",
            "limit": limit,
            "offset": offset,
            "loc_city_id": self.city_id,
            "published_at__gte": self.date_from,
            "published_at__lte": self.date_to,
        }
        response = requests.get(self.BASE_URL, headers=self.HEADERS, params=params)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            raise Exception(f"Error fetching data: {response.status_code}")


class EstateManager:
    """
    Main interface for working with estate data in an OOP style.
    """

    def __init__(self):
        self.fetcher = EstateFetcher()

    def get_estate_by_index(self, n):
        """
        Get the nth estate as a dictionary in the desired format.
        """
        # Fetch enough records to include index n
        estates_raw = self.fetcher.fetch(limit=n + 1)

        if n >= len(estates_raw):
            raise IndexError(f"File number {n} not found (available: {len(estates_raw)})")

        estate = Estate(estates_raw[n])
        return estate.to_dict()


# Script entry point
if __name__ == "__main__":
    try:
        n = int(input("Enter listing index (0 to anything): "))
        manager = EstateManager()
        estate_data = manager.get_estate_by_index(n)
        print(estate_data)
    except Exception as e:
        print(f"Error: {e}")
