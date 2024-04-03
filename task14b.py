from task14 import ScrapeHero
# from pika_client import PikaClient
from redis_queue import RedisQueue

queue = 'url_queue'
metadata = [{
    "url": "https://scrapeme.live/shop/",
    "scrape_function": "url_logic"
}]

def page_logic(soup, metadata):
    del metadata["scrape_function"]
    metadata["name"] = soup.find(class_='product_title entry-title').string
    metadata["description"] = soup.find(class_="woocommerce-product-details__short-description").p.string
    metadata["prize"] = soup.find(class_='price').span.text
    metadata["in stock"]  = soup.find(class_="stock in-stock").string.split()[0]
    return metadata
    
    
def url_logic(soup, metadata):
    urls = []
    next_url = soup.find(class_="next page-numbers")
    if next_url:
        next_url = next_url['href']
        next_url = {
            "url": next_url,
            "scrape_function": "url_logic"
        }
        urls.append(next_url)
    for li in soup.find_all(class_="woocommerce-LoopProduct-link woocommerce-loop-product__link"):
        url = li['href']
        urls.append({
            "url": url,
            "scrape_function": "page_logic"
        })
    return urls

scraper = ScrapeHero(
    host_name="10.0.0.46",
    port_no=6379,
    redis_queue= RedisQueue,
    metadata_list=metadata,
    queue=queue,
    scrape_functions = {
        "url_logic": url_logic,
        "page_logic": page_logic,
        },
    n_workers = 2,
    url_exceptions=[],
    data_store="pokemon_data"
    
)


data = scraper.start_scraping()
print(data)
