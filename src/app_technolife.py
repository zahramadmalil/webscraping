from bs4 import BeautifulSoup
import requests
import sqlite3

DB_NAME = 'LaptopData.db'
conn = sqlite3.connect(DB_NAME)
print('DB CREATED')

query = '''CREATE TABLE IF NOT EXISTS laptop_techno
(id INTEGER primary key AUTOINCREMENT,
description TEXT,
price REAL,
image_url TEXT,
link TEXT)
'''
cursor = conn.cursor()
cursor.execute(query)
conn.commit()
print('TABLE CREATED')

url = 'https://www.technolife.com/category/laptop-equipment/laptop'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
#print(soup)

cards = soup.select('section.relative.w-full.rounded-\\[10px\\].bg-white')
#print(len(cards))

for card in cards:

    description = card.select_one('h2').get_text().strip()
    
    if description == None:
        continue
    # print(description)
    # print('-'*30)

    price = card.select_one('p.text-\\[22px\\].font-semiBold.leading-5').get_text().strip()
    if price ==  None:
        continue
    # print(price)
    # print('-'*30)

    img_url = 'https://www.technolife.com' + card.select_one('img').get('src')
    # print(img_url)
    # print('-'*30)

    link = 'https://www.technolife.com' + card.select_one('a').get('href')
    # print(link)
    # print('-'*30)

    query = '''
            INSERT INTO laptop_techno(description, price, image_url, link)
            VALUES(?, ?, ?, ?)'''
    
    cursor = conn.cursor()
    cursor.execute(query, (description, price, img_url, link))
    conn.commit()

conn.close()
print('DATA SCRAPED')