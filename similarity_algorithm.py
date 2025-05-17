from difflib import SequenceMatcher

class PropertySimilarity:
    def __init__(self):
        self.weight_config = {
            'title': 0.15,
            'address': 0.2,
            'area': 0.15,
            'number_of_rooms': 0.1,
            'year_of_manufacture': 0.05,
            'facilities': 0.15,
            'price': 0.2
        }

    def similarity_score(self, p1: dict, p2: dict) -> float:
        score = 0.0
        if p1['is_rental'] != p2['is_rental']:
            return score
        else:
            # 1. Title similarity
            score += self.weight_config['title'] * SequenceMatcher(None, p1['title'], p2['title']).ratio()
            # 2. Address similarity
            score += self.weight_config['address'] * SequenceMatcher(None, p1['address'], p2['address']).ratio()
            # 3. Area similarity (normalized difference)
            area_diff = abs(int(p1['area']) - int(p2['area']))
            max_area = max(int(p1['area']), int(p2['area']))
            score += self.weight_config['area'] * max(1 - (area_diff)**2 / max_area , 0)
            # 4. Room count similarity (exact match)
            score += self.weight_config['number_of_rooms'] if p1['number_of_rooms'] == p2['number_of_rooms'] else 0
            # 5. Year of manufacture (normalized difference)
            if p1['year_of_manufacture'] and p2['year_of_manufacture']:
                year_diff = abs(int(p1['year_of_manufacture']) - int(p2['year_of_manufacture']))
                score += self.weight_config['year_of_manufacture'] * max(1 - (year_diff)**2 / 50 , 0)
            # 6. Facilities (Jaccard similarity)
            facilities_union = set(p1['facilities']).union(set(p2['facilities']))
            facilities_intersection = set(p1['facilities']).intersection(set(p2['facilities']))
            facilities_similarity = len(facilities_intersection) / len(facilities_union) if facilities_union else 0
            score += self.weight_config['facilities'] * facilities_similarity
            # 7. Price similarity (normalized difference)
            if p1['is_rental'] == False:
                price_diff = abs(float(p1['total_price']) - float(p2['total_price']))
                max_price = max(float(p1['total_price']), float(p2['total_price']))
                score += self.weight_config['price'] * (1 - price_diff / max_price)
            else:
                mortgage_diff = abs(float(p1['mortgage']) - float(p2['mortgage']))
                max_motgage = max(float(p1['mortgage']), float(p2['mortgage']))
                rent_diff = abs(float(p1['rent']) - float(p2['rent']))
                max_rent = max(float(p1['rent']), float(p2['rent']))
                score += self.weight_config['price'] * (1 - rent_diff / (2*max_rent) - mortgage_diff / (2*max_motgage))
            return round(score*100, 2)
    
    def compare_properties(self , properties) -> list[dict]:
        results = []
        for i in range(len(properties)):
            for j in range(i+1, len(properties)):
                p1, p2 = properties[i] , properties[j]
                similarity = self.similarity_score(p1,p2)
                if similarity >= 70:
                    results.append({
                        'property_1': p1['id'],
                        'property_2': p2['id'],
                        'similarity': similarity
                    })
        results.sort(key=lambda x: x['similarity'],reverse=True)
        return results

if __name__ == '__main__':
    p1 = {'file_code': '', 'title': 'جلال 62 اولین تقاطع سمت چپ', 'address': 'منطقه 11 محله آزاد شهر خیابان جلال آل احمد ( ایرج میرزا ) 62 اولین تقاطع سمت چپ', 'total_price': 8880000000, 'price_per_meter': 48000000, 'mortgage': None, 'rent': None, 'area': 185, 'number_of_rooms': 3, 'year_of_manufacture': 1, 'facilities': ['پارکینگ', 'آسانسور', 'انباری', 'تراس', 'معاوضه'], 'pictures': [], 'is_rental': False}

    p2 = {'file_code': '', 'title': 'ساجدی 3 فخر ۱۲', 'address': 'منطقه 2 محله فرامرز عباسی خیابان ساجدی 3 فخر ۱۲', 'total_price': 5390000000, 'price_per_meter': 35000000, 'mortgage': None, 'rent': None, 'area': 154, 'number_of_rooms': 3, 'year_of_manufacture': 18, 'facilities': ['نیاز به کارشناسی قیمت', 'بازسازی شده', 'پارکینگ', 'انباری', 'سرویس فرنگی', 'تراس', 'کمد دیواری', 'گاز روکار', 'خط تلفن', 'معاوضه'], 'pictures': ['https://maskan-file.ir/img/FilesImages/2724168_5.jpg?v=5/17/2025', 'https://maskan-file.ir/img/FilesImages/2724168_7.jpg?v=5/17/2025', 'https://maskan-file.ir/img/FilesImages/2724168_8.jpg?v=5/17/2025', 'https://maskan-file.ir/img/FilesImages/2724168_4.jpg?v=5/17/2025', 'https://maskan-file.ir/img/FilesImages/2724168_2.jpg?v=5/17/2025', 'https://maskan-file.ir/img/FilesImages/2724168_1.jpg?v=5/17/2025', 'https://maskan-file.ir/img/FilesImages/2724168_6.jpg?v=5/17/2025', 'https://maskan-file.ir/img/FilesImages/2724168_3.jpg?v=5/17/2025'], 'is_rental': False} 

    similarity_checker = PropertySimilarity()
    score = similarity_checker.similarity_score(p1, p2)
    print(f"Similarity Score: {score}")