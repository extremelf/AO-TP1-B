import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.http.headers import Headers
import scrapy_splash
import json
from CryptoList import CryptoList

RENDER_HTML_URL = 'http://localhost:8050/render.html'


class CryptoSpider(scrapy.Spider):
    name = 'CryptoSpider'
    start_urls = ['https://coinmarketcap.com/all/views/all']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'LOG_ENABLED': False,
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'CONCURRENT_ITEMS': 4
    }

    def __init__(self, *args, **kwargs):
        super(CryptoSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            body = json.dumps({"url": url, 'wait': 0.5}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield scrapy.Request(RENDER_HTML_URL, self.parse, method="POST", body=body, headers=headers)

    def parse(self, response, **kwargs):
        for coin in response.css("tr.cmc-table-row"):
            cryptos.add_crypto(name=coin.css("a.cmc-table__column-name--name::text").get() if coin.css("a.cmc-table__column-name--name::text").get() else coin.css("a.cmc-link::text").get())


if __name__ == "__main__":
    cryptos = CryptoList()
    process = CrawlerProcess(get_project_settings())
    process.crawl(CryptoSpider)
    process.start()
    print(cryptos.get_list())
