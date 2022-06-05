from redisPipeline import RedisPipeline

SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}

CASSANDRA_KEYSPACE = 'coin_keyspace'
ITEM_PIPELINES = {
    'project.pipelines.CassandraPipeline': 100
}
REDIS_ITEMS_KEY: str
REDIS_ITEMS_SERIALIZER: str

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapyjs.SplashAwareDupeFilter'
