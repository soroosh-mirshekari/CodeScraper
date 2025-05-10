import requests
import time

base_url = "https://api.melkemun.com/v1/estates/"
headers = {
    "Referer": "https://melkemun.com/",
    "Sec-CH-UA": "\"Chromium\";v=\"136\", \"Google Chrome\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}

seen_id = set()
limit = 20
total_pages = 200
cnt = 1

for page in range(total_pages):
    offset = page * limit
    url = f"{base_url}?ordering=-published_at&limit={limit}&offset={offset}&published_at__gte=2024-05-14T00:00:00.000Z&published_at__lte=2025-05-10T23:59:59.000Z&loc_city_id=2"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data.get("results", []):
            id = item.get("id")
            if id and id not in seen_id:
                print(cnt, ":", id)
                seen_id.add(id)
                cnt += 1
    else:
        print("خطا در دریافت صفحه", page + 1)
    
    time.sleep(1)