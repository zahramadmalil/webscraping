from bs4 import BeautifulSoup
import requests
import sqlite3
import re

DB_NAME = 'MobileData.db'
conn = sqlite3.connect(DB_NAME)
print('DB CREATED')

# چون هر بار اجرا ممکنه رکورد تکراری اضافه بشه، جدول رو از اول می‌سازیم
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS mobile_techno')
query = '''CREATE TABLE IF NOT EXISTS mobile_techno
(id INTEGER primary key AUTOINCREMENT,
 description TEXT,
 brand TEXT,
 storage TEXT,
 ram TEXT,
 color TEXT,
 rating TEXT,
 image_url TEXT,
 link TEXT)
'''
cursor.execute(query)
conn.commit()
print('TABLE CREATED')

# ---------- مرحله ۱: گرفتن لیست محصولات از صفحه موبایل ----------
url = 'https://www.technolife.com/category/mobile/mobile-phone'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

cards = soup.select('section.relative.w-full.rounded-\\[10px\\].bg-white')
print(f'cards: {len(cards)}')

# ---------- مرحله ۲: رفتن به هر محصول ----------
for card in cards:

    # لینک محصول رو بگیر
    link_tag = card.select_one('a')
    if link_tag is None:
        continue
    link = 'https://www.technolife.com' + link_tag.get('href')

    # تصویر
    img_tag = card.select_one('img')
    if img_tag is None:
        continue
    img_url = 'https://www.technolife.com' + img_tag.get('src')

    # ---------- ورود به صفحه محصول ----------
    print(f'\n>>> {link}')
    product_response = requests.get(link, headers=headers)
    product_response.encoding = 'utf-8'
    product_soup = BeautifulSoup(product_response.text, 'html.parser')

    # --- توضیح کوتاه (اسم محصول) ---
    h1 = product_soup.find('h1')
    description = h1.get_text().strip() if h1 else None
    if not description:
        continue

    # --- متن کل صفحه برای پیدا کردن مشخصات ---
    page_text = product_soup.get_text(' ', strip=True)

    # --- برند = اولین کلمه اسم محصول ---
    brand = description.split()[0]

    # --- حافظه داخلی ---
    storage_match = re.search(
        r'حافظه\s*(?:داخلی)?\s*[:\-]?\s*([\d]+\s*(?:GB|گیگابایت|TB|ترابایت))',
        page_text, re.IGNORECASE
    )
    storage = storage_match.group(1) if storage_match else 'نامشخص'

    # --- RAM ---
    ram_match = re.search(
        r'(?:RAM|رم)\s*[:\-]?\s*([\d]+\s*(?:GB|گیگابایت))',
        page_text, re.IGNORECASE
    )
    ram = ram_match.group(1) if ram_match else 'نامشخص'

    # --- رنگ ---
    color_match = re.search(r'رنگ\s*[:\-]?\s*([^\n,،]+)', page_text)
    color = color_match.group(1).strip() if color_match else 'نامشخص'

    # --- امتیاز کاربران ---
    rating_match = re.search(
        r'(?:امتیاز|rating)\s*[:\-]?\s*([\d.]+)',
        page_text, re.IGNORECASE
    )
    rating = rating_match.group(1) if rating_match else 'بدون امتیاز'

    print(f'    توضیح: {description[:60]}')
    print(f'    برند: {brand}')
    print(f'    حافظه: {storage}')
    print(f'    RAM: {ram}')
    print(f'    رنگ: {color}')
    print(f'    امتیاز: {rating}')

    # ---------- ذخیره در دیتابیس ----------
    insert_query = '''
        INSERT INTO mobile_techno
        (description, brand, storage, ram, color, rating, image_url, link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(insert_query, (
        description, brand, storage, ram, color, rating, img_url, link
    ))
    conn.commit()

conn.close()
print('\n✅ DATA SCRAPED')