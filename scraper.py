import scrapy
import sys
import json
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.http.headers import Headers
from scrapy.http.request import Request
from twisted.internet import reactor, defer

from CryptoList import CryptoList

RENDER_HTML_URL = 'http://localhost:8050/render.html'


class CryptoListSpider(scrapy.Spider):
    name = 'CryptoListSpider'
    start_urls = ['https://coinmarketcap.com/all/views/all']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'LOG_ENABLED': False,
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'CONCURRENT_ITEMS': 4
    }

    def __init__(self, *args, **kwargs):
        super(CryptoListSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            body = json.dumps({"url": url, 'wait': 0.5}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield scrapy.Request(RENDER_HTML_URL, self.parse, method="POST", body=body, headers=headers)

    def parse(self, response, **kwargs):
        for coin in response.css("tr.cmc-table-row"):
            cryptos.add_crypto(name=coin.css("a.cmc-table__column-name--name::text").get() if coin.css(
                "a.cmc-table__column-name--name::text").get() else coin.css("a.cmc-link::text").get())


class CryptoInfoSpider(scrapy.Spider):
    name = 'CryptoInfoSpider'
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
        'LOG_ENABLED': False,
        'COOKIES_ENABLED': False,
        'USER_AGENT': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'CONCURRENT_ITEMS': 4
    }

    def __init__(self, *args, **kwargs):
        super(CryptoInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls = list(
            map(lambda crypto: f'https://coinmarketcap.com/currencies/{crypto["name"].lower()}/historical-data/',
                cryptos.get_list()))

    def start_requests(self):
        for url in self.start_urls:
            body = json.dumps({"url": url, 'wait': 0.5}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield scrapy.Request(RENDER_HTML_URL, self.parse, method="POST", body=body, headers=headers)

    def parse(self, response, **kwargs):
        coin_id = response.css("div.nameHeader > img").xpath('@src').get().split("/")[-1].split(".")[0]
        request = Request(
            url=f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id={coin_id}&convertId=2781&timeStart=1647820800&timeEnd=1653091200',
            callback=self.parse_coins,
            cb_kwargs=dict(main_url=response.url))
        yield request

    def parse_coins(self, response, main_url):
        json_data = json.loads(response.body)
        print(json_data['data']['quotes'][1]['timeOpen'])



if __name__ == "__main__":
    if "twisted.internet.reactor" in sys.modules:
        del sys.modules["twisted.internet.reactor"]
    cryptos = CryptoList()
    process = CrawlerRunner()


    @defer.inlineCallbacks
    def crawler():
        yield process.crawl(CryptoListSpider)
        yield process.crawl(CryptoInfoSpider)
        reactor.stop()


    crawler()
    reactor.run()
