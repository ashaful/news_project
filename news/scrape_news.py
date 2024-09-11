import sys
import os
import django
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_project.settings')
django.setup()

from news.models import NewsArticle

# Define the URL of The Daily Star website
url = 'https://www.thedailystar.net/'

# Make a request to fetch the page content
response = requests.get(url)
if response.status_code == 200:
    print("Successfully fetched the webpage")
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")
    exit()

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all news article containers
articles = soup.find_all('div', class_='card')

# Initialize a list to store scraped data
scraped_data = []

# Loop through each article container and extract the necessary details
for article in articles:
    try:
        # Find the title and link
        title_tag = article.find('h3', class_='title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.find('a')['href']
            
            # Ensure the link is a full URL
            if not link.startswith('http'):
                link = 'https://www.thedailystar.net' + link

            # Extract the category from the article
            category_tag = article.find('p', class_='lc-3 intro')
            category = category_tag.get_text(strip=True) if category_tag else 'Uncategorized'

            # Set the newspaper name
            newspaper_name = "The Daily Star"

            # Set the date and time as current
            date = datetime.now().date()
            time = datetime.now().time()

            # Save the data to the database
            NewsArticle.objects.create(
                title=title,
                link=link,
                newspaper=newspaper_name,
                date=date,
                time=time,
                category=category
            )

            # Append the data to our list
            scraped_data.append({
                'title': title,
                'newspaper': newspaper_name,
                'date': date,
                'time': time,
                'category': category
            })

    except Exception as e:
        print(f"Error processing article: {e}")

# Write the scraped data to a CSV file
csv_file = "daily_star_news.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'newspaper', 'date', 'time', 'category'])
    writer.writeheader()
    writer.writerows(scraped_data)

print(f"Data written to {csv_file}")
