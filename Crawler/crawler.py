import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Set to prevent infinite recursion
MAX_PAGES_TO_CRAWL = 10


class SimpleWebCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()  # Set to store visited URLs
        self.to_visit = [base_url]  # Queue for URLs to visit

    def crawl(self):
        while self.to_visit and len(self.visited) < MAX_PAGES_TO_CRAWL:
            url = self.to_visit.pop(0)
            if url not in self.visited:
                self.visit_page(url)

    def visit_page(self, url):
        print(f"Visiting: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.visited.add(url)
                self.extract_links(response.text, url)
            else:
                print(f"Failed to retrieve {url} (Status code: {response.status_code})")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            # Resolve relative links
            full_url = urljoin(base_url, href)
            # Ensure the link is within the same domain
            if self.is_valid_link(full_url):
                self.to_visit.append(full_url)

    def is_valid_link(self, url):
        # Ensure it's the same domain and not already visited
        return (urlparse(url).netloc == urlparse(self.base_url).netloc and
                url not in self.visited)


if __name__ == "__main__":
    start_url = "https://divar.ir"
    crawler = SimpleWebCrawler(start_url)
    crawler.crawl()
