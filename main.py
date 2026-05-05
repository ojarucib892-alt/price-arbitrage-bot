import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

# Database setup
def initialize_db():
    conn = sqlite3.connect('apartments.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS apartments
                 (id INTEGER PRIMARY KEY, title TEXT, price REAL, date_scraped TEXT)''')
    conn.commit()
    return conn

# Scrape data from Avito
def scrape_avito():
    url = 'https://www.avito.ru/elista'  # Example URL for Avito in Elista
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    apartments = []
    
    for item in soup.find_all('div', class_='item-class'):  # Update class accordingly
        title = item.find('h3').text
        price = float(item.find('span', class_='price-class').text.replace('₽', '').replace(' ', ''))
        apartments.append((title, price))
    
    return apartments

# Save and analyze data
def save_apartments(conn, apartments):
    c = conn.cursor()
    for title, price in apartments:
        c.execute('INSERT INTO apartments (title, price, date_scraped) VALUES (?, ?, ?)',
                  (title, price, datetime.utcnow().isoformat()))
    conn.commit()

def analyze_prices(conn):
    c = conn.cursor()
    # Example query to find the cheapest apartment
    c.execute('SELECT title, price FROM apartments ORDER BY price LIMIT 1')
    cheapest = c.fetchone()
    print(f'Cheapest apartment: {cheapest[0]} at price {cheapest[1]}')

if __name__ == '__main__':
    conn = initialize_db()
    apartments = scrape_avito()
    save_apartments(conn, apartments)
    analyze_prices(conn)
    conn.close()