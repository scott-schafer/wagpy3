from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

def scrape_data(request):
    url = "127.0.0.1"  # Replace with the URL you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Extract all paragraph tags
    paragraphs = soup.find_all('p')
    scraped_text = [p.get_text() for p in paragraphs]

    context = {'scraped_text': scraped_text}
    return render(request, 'blog/blog_detail.html', context)


