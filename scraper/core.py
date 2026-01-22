import requests
from bs4 import BeautifulSoup
import json

class ArrowScraper:
    def __init__(self):
        self.base_url = "https://www.arrowconveyancing.co.uk/"
    
    def scrape(self):
        """Simple Flask-compatible scraper"""
        try:
            response = requests.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'success': True,
                'title': soup.title.text if soup.title else 'No title',
                'content': soup.get_text()[:500] + "..."
            }
        except Exception as e:
            return {
                'success': False, 
                'error': str(e)
            }