import re
from typing import Dict, List, Optional
from datetime import datetime

class MelkemunEstateCleaner:
    """
    A class for cleaning and standardizing real estate data from melkemun.com
    This class transforms raw data received from the scraper into a standard format.
    """
    
    # Mapping of transaction types
    STATUS_MAPPING = {
        0: "فروش",
        1: "رهن و اجاره",
        2: "رهن کامل",
        3: "پیش فروش",
        5: "مشارکت",
        6: "اجاره موقت"
    }
    
    # Mapping of property types
    TYPE_MAPPING = {
        0: "آپارتمان",
        1: "ویلایی",
        2: "زمین",
        3: "ویلا",
        4: "تجاری",
        5: "سوییت",
        6: "اداری",
        7: "باغ"
    }
    
    # Mapping of facilities to Persian
    FACILITY_MAPPING = {
        "elevator": "آسانسور",
        "parking": "پارکینگ",
        "bathroom": "سرویس بهداشتی",
        "security_guard": "نگهبان",
        "warehouse": "انباری",
        "jacuzzi": "جکوزی",
        "conference_hall": "سالن کنفرانس"
    }

    def __init__(self, raw_data: Dict):
        """
        Initialization with raw data
        
        :param raw_data: Dictionary containing raw data from the API
        """
        self.raw_data = raw_data or {}
        self.status_id = self.raw_data.get("status_id")
        self.type_id = self.raw_data.get("type_id")
        self.is_rental = self.status_id in {1, 2, 6}

    def clean(self) -> Dict:
        """
        Perform all cleaning and standardization of the data
        
        :return: A dictionary containing the cleaned and standardized data
        """
        try:
            cleaned_data = {
                "source": "melkemun",  # Corrected site name
                "file_code": self._clean_id(),
                "title": self._generate_title(),
                "address": self._clean_address(),
                "total_price": self._clean_price("price"),
                "price_per_meter": self._clean_price("price_per_meter"),
                "mortgage": self._clean_mortgage(),
                "rent": self._clean_rent(),
                "area": self._clean_area(),
                "number_of_rooms": self._clean_rooms(),
                "year_of_manufacture": self._clean_year(),
                "facilities": self._extract_facilities(),
                "pictures": self._extract_pictures(),
                "is_rental": self.is_rental,
                "transaction_type": self.STATUS_MAPPING.get(self.status_id, "نامشخص"),
                "property_type": self.TYPE_MAPPING.get(self.type_id, "نامشخص"),
                "location": self._extract_location(),
                "seller_info": self._extract_seller_info(),
                "description": self._clean_description(),
                "published_at": self._clean_publish_date(),
                "metadata": self._extract_metadata()
            }
            
            # Remove empty fields
            return {k: v for k, v in cleaned_data.items() if v not in [None, "", [], {}]}
            
        except Exception as e:
            print(f"Error cleaning data: {str(e)}")
            return {}

    # ========== Helper Methods ==========
    
    def _clean_id(self) -> str:
        """Clean and standardize property ID"""
        return str(self.raw_data.get("id", "")).strip()

    def _generate_title(self) -> str:
        """Generate a standardized title for the property"""
        status = self.STATUS_MAPPING.get(self.status_id, "معامله")
        prop_type = self.TYPE_MAPPING.get(self.type_id, "ملک")
        area = self.raw_data.get("lot")
        rooms = self.raw_data.get("rooms")
        
        title_parts = [status, prop_type]
        
        if area:
            title_parts.append(f"{area} متر")
        if rooms:
            title_parts.append(f"{rooms} خوابه")
            
        return " ".join(title_parts)

    def _clean_address(self) -> str:
        """Clean and standardize address"""
        address = self.raw_data.get("loc_address", "")
        city = self.raw_data.get("loc_city_name", "")
        neighborhood = self.raw_data.get("loc_neighborhood_name", "")
        
        # Remove unnecessary characters
        address = re.sub(r'\s+', ' ', address).strip()
        
        address_parts = []
        if neighborhood:
            address_parts.append(neighborhood)
        if address:
            address_parts.append(address)
        if city and city not in address:
            address_parts.append(city)
            
        return "، ".join(address_parts) if address_parts else "نامشخص"

    def _clean_price(self, field_name: str) -> str:
        """Clean price and price per meter"""
        if self.is_rental:
            return ""
            
        price = self.raw_data.get(field_name)
        if price is None:
            return ""
            
        try:
            return "{:,}".format(int(price))
        except (ValueError, TypeError):
            return ""

    def _clean_mortgage(self) -> str:
        """Clean deposit amount"""
        if not self.is_rental:
            return ""
            
        deposit = self.raw_data.get("deposit")
        if deposit is None:
            return ""
            
        try:
            return "{:,}".format(int(deposit))
        except (ValueError, TypeError):
            return ""

    def _clean_rent(self) -> str:
        """Clean rent amount"""
        if not self.is_rental:
            return ""
            
        rent = self.raw_data.get("price")
        if rent is None:
            return ""
            
        try:
            return "{:,}".format(int(rent))
        except (ValueError, TypeError):
            return ""

    def _clean_area(self) -> str:
        """Clean area (size)"""
        area = self.raw_data.get("lot")
        if area is None:
            return ""
            
        try:
            return str(int(area))
        except (ValueError, TypeError):
            return ""

    def _clean_rooms(self) -> str:
        """Clean number of rooms"""
        rooms = self.raw_data.get("rooms")
        if rooms is None:
            return ""
            
        try:
            return str(int(rooms))
        except (ValueError, TypeError):
            return ""

    def _clean_year(self) -> str:
        """Clean year of manufacture"""
        year = self.raw_data.get("built_year")
        if year is None:
            return ""
            
        try:
            return str(int(year))
        except (ValueError, TypeError):
            return ""

    def _extract_facilities(self) -> List[str]:
        """Extract and standardize facilities"""
        facilities = []
        
        # Main facilities with "ame_" prefix
        for key, value in self.raw_data.items():
            if key.startswith("ame_") and value:
                facility_name = key[4:]  # Remove "ame_" prefix
                persian_name = self.FACILITY_MAPPING.get(facility_name, facility_name)
                facilities.append(persian_name)
        
        # Additional facilities
        if self.raw_data.get("has_kitchen", False):
            facilities.append("آشپزخانه")
        if self.raw_data.get("has_furniture", False):
            facilities.append("مبله")
            
        return sorted(list(set(facilities)))  # Remove duplicates and sort

    def _extract_pictures(self) -> List[str]:
        """Extract pictures (not available in this API)"""
        return []

    def _extract_location(self) -> Dict:
        """Extract geographic location information"""
        lat = self.raw_data.get("loc_latitude")
        lon = self.raw_data.get("loc_longitude")
        
        return {
            "latitude": str(lat) if lat is not None else "",
            "longitude": str(lon) if lon is not None else "",
            "map_link": f"https://maps.google.com/?q={lat},{lon}" if lat and lon else ""
        }

    def _extract_seller_info(self) -> Dict:
        """Extract seller information"""
        return {
            "name": self.raw_data.get("seller_name", "").strip(),
            "type": "شخصی" if self.raw_data.get("is_individual") else "نمایشگاه",
            "phone": self._clean_phone(self.raw_data.get("seller_phone", ""))
        }

    def _clean_phone(self, phone: str) -> str:
        """Clean phone number"""
        phone = re.sub(r'[^\d+]', '', phone)
        return phone if phone else ""

    def _clean_description(self) -> str:
        """Clean description"""
        desc = self.raw_data.get("description", "")
        if not desc:
            return ""
            
        # Remove extra spaces and new lines
        desc = re.sub(r'\s+', ' ', desc).strip()
        return desc

    def _clean_publish_date(self) -> str:
        """Clean publish date"""
        publish_date = self.raw_data.get("published_at", "")
        if not publish_date:
            return ""
            
        try:
            # Convert to a readable format
            dt = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.strftime("%Y/%m/%d %H:%M")
        except ValueError:
            return publish_date

    def _extract_metadata(self) -> Dict:
        """Extract additional metadata"""
        return {
            "floor": self.raw_data.get("floor"),
            "total_floors": self.raw_data.get("total_floors"),
            "building_age": self.raw_data.get("building_age"),
            "status_id": self.status_id,
            "type_id": self.type_id
        }


def batch_clean_estates(raw_data_list: List[Dict]) -> List[Dict]:
    """
    Clean a batch of real estate data
    
    :param raw_data_list: List of dictionaries containing raw data
    :return: List of dictionaries containing cleaned data
    """
    return [MelkemunEstateCleaner(item).clean() for item in raw_data_list]
