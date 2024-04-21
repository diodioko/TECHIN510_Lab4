# books_scraper.py
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from db import Database

load_dotenv()
BASE_URL = 'http://books.toscrape.com/catalogue/page-{page}.html'

def get_rating(rating_str):
    ratings = {
        'Zero': 0,
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return ratings.get(rating_str, 0)

with Database(os.getenv('DATABASE_URL')) as pg:
    pg.create_table()
    # pg.truncate_table()  # Uncomment if you need to reset the table

    page = 1
    while True:
        url = BASE_URL.format(page=page)
        print(f"Scraping {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        book_list = soup.select('article.product_pod')

        if not book_list:
            break

        for book in book_list:
            details = {}
            details['name'] = book.select_one('h3 > a').get('title')
            price = book.select_one('p.price_color').text[1:]
            details['price'] = float(price)
            details['rating'] = get_rating(book.select_one('p.star-rating').get('class')[1])
            link = 'http://books.toscrape.com/catalogue/' + book.select_one('h3 > a').get('href')
            
            # Fetching book details page
            detail_response = requests.get(link)
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')
            description_tag = detail_soup.select_one('.product_page > p')
            details['description'] = description_tag.text if description_tag else 'No description available'

            pg.insert_book(details)
        page += 1
