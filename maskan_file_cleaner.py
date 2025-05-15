import re
from typing import Dict, Any, List, Optional, Union

class RealEstateCleaner:
    """
    A comprehensive data cleaner for real estate listings that:
    - Standardizes and validates property data
    - Handles both rental and sale listings
    - Cleans and normalizes all fields
    - Provides robust error handling
    """
    
    def __init__(self):
        """Initialize regex patterns for data extraction from Persian text"""
        # Pattern to extract price values (e.g. "3,500,000 تومان")
        self.price_pattern = re.compile(r'(\d[\d,]*)\s*تومان')
        
        # Pattern to extract area values (supports both "120 متر" and standalone numbers)
        self.area_pattern = re.compile(r'(\d+)\s*متر|\b(\d+)\b')
        
        # Pattern to extract year values 
        self.year_pattern = re.compile(r'(\d+)')
        
        # Pattern to extract room counts (supports both "3 خواب" and standalone numbers)
        self.room_pattern = re.compile(r'(\d+)\s*خواب|\b(\d+)\b')

    def clean(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main cleaning method that processes raw scraped data into standardized format.
        
        Args:
            raw_data: Raw dictionary containing scraped property data
            
        Returns:
            Dict[str, Any]: Cleaned and standardized property data
            Returns empty dict if input is invalid
        """
        # Early return for empty/invalid input
        if not raw_data:
            return {}

        cleaned_data = raw_data.copy()
        
        # Clean each data field with appropriate method
        cleaned_data['address'] = self._clean_address(raw_data.get('address', ''))
        
        # Handle price fields differently based on rental/sale type
        self._clean_prices(cleaned_data, raw_data)
        
        # Clean numeric fields with specialized methods
        cleaned_data['area'] = self._extract_area_or_rooms(raw_data.get('area', ''))
        cleaned_data['number_of_rooms'] = self._extract_area_or_rooms(raw_data.get('number_of_rooms', ''))
        cleaned_data['year_of_manufacture'] = self._extract_number(
            raw_data.get('year_of_manufacture', ''), 
            self.year_pattern
        )
        
        # Clean list-type fields
        cleaned_data['facilities'] = self._clean_facilities(raw_data.get('facilities', []))
        cleaned_data['pictures'] = self._clean_images(raw_data.get('pictures', []))
        
        return cleaned_data

    def _clean_prices(self, cleaned_data: Dict[str, Any], raw_data: Dict[str, Any]) -> None:
        """
        Cleans and standardizes price-related fields based on listing type (rental/sale).
        
        Handles:
        - Different price formats (strings, numbers)
        - Empty/missing values
        - Conversion to integers
        - Proper null handling for irrelevant fields
        """
        is_rental = raw_data.get('is_rental', False)
        
        if is_rental:
            # For rental properties, clean mortgage and rent fields
            cleaned_data['mortgage'] = self._extract_number(raw_data.get('mortgage', ''))
            cleaned_data['rent'] = self._extract_number(raw_data.get('rent', ''))
            cleaned_data['total_price'] = None
            cleaned_data['price_per_meter'] = None
        else:
            # For sale properties, clean total price and price per meter
            cleaned_data['total_price'] = self._extract_number(raw_data.get('total_price', ''))
            cleaned_data['price_per_meter'] = self._extract_number(raw_data.get('price_per_meter', ''))
            cleaned_data['mortgage'] = None
            cleaned_data['rent'] = None

    def _extract_area_or_rooms(self, value: Union[str, int]) -> Optional[int]:
        """
        Extracts numeric value for area or room count from various text formats.
        
        Args:
            value: Input value which could be string or number
            
        Returns:
            Extracted integer or None if value is invalid
        """
        # Handle already numeric values
        if isinstance(value, int):
            return value
            
        # Handle empty/None values
        if not value:
            return None
            
        try:
            # First try direct conversion to integer
            return int(value)
        except ValueError:
            # If direct conversion fails, use appropriate regex pattern
            pattern = self.area_pattern if 'متر' in str(value) else self.room_pattern
            match = pattern.search(str(value))
            
            if match:
                # Extract first non-None group from regex match
                number_str = next(g for g in match.groups() if g is not None)
                return int(number_str.replace(',', ''))
                
        return None

    def _clean_address(self, address: str) -> str:
        """
        Cleans and standardizes address string by:
        - Removing extra whitespace
        - Normalizing punctuation
        - Removing duplicate words while preserving order
        """
        if not address:
            return ""
            
        # Normalize whitespace and remove special chars
        address = ' '.join(address.strip().split())
        
        # Remove duplicate words while maintaining order
        parts = address.split()
        seen = set()
        unique_parts = [x for x in parts if not (x in seen or seen.add(x))]
        
        return ' '.join(unique_parts)

    def _extract_number(self, text: str, pattern: Optional[re.Pattern] = None) -> Optional[int]:
        """
        Extracts numeric value from text using specified regex pattern.
        
        Args:
            text: Input text containing number
            pattern: Regex pattern to use (defaults to price pattern)
            
        Returns:
            Extracted integer or None if no match found
        """
        if not text:
            return None
            
        try:
            # Use price pattern if none specified
            pattern = pattern or self.price_pattern
                
            match = pattern.search(str(text))
            if match:
                # Get first non-None group from regex match
                number_str = next(g for g in match.groups() if g is not None)
                return int(number_str.replace(',', ''))
                
        except (ValueError, AttributeError, TypeError, StopIteration):
            pass
            
        return None

    def _clean_facilities(self, facilities: List[str]) -> List[str]:
        """
        Cleans list of facilities by:
        - Removing empty/None items
        - Trimming whitespace
        - Removing duplicates while preserving order
        """
        if not facilities:
            return []
            
        cleaned = []
        seen = set()
        
        for item in facilities:
            if isinstance(item, str):
                item = item.strip()
                if item and item not in seen:
                    cleaned.append(item)
                    seen.add(item)
                    
        return cleaned

    def _clean_images(self, images: List[str]) -> List[str]:
        """
        Cleans list of image URLs by:
        - Removing empty/None items
        - Trimming whitespace
        - Removing duplicates while preserving order
        - TODO: Add URL validation/normalization
        """
        if not images:
            return []
            
        cleaned = []
        seen = set()
        
        for url in images:
            if isinstance(url, str):
                url = url.strip()
                if url and url not in seen:
                    cleaned.append(url)
                    seen.add(url)
                    
        return cleaned