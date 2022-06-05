from cassandra.cluster import Cluster
from scrapy.utils.misc import load_object
from twisted.internet.threads import deferToThread

import connection
import defaults


class CassandraPipeline(object):

    def __init__(self, cassandra_keyspace):
        self.session = None
        self.cassandra_keyspace = cassandra_keyspace

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            cassandra_keyspace=crawler.settings.get('CASSANDRA_KEYSPACE')
        )

    def open_spider(self, spider):
        cluster = Cluster()
        self.session = cluster.connect(self.cassandra_keyspace)

    def process_item(self, item, spider):
        # insert item
        try:
            print("lol i am here")
            self.session.execute(
                "INSERT INTO crypto_coin (name, marketCap,price_close,price_high,price_low,price_open,time_close,time_high, time_low, time_open,timestamp,volume) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                item['name'], item['marketCap'], item['price_close'], item['price_high'],
                item['price_low'], item['price_open'],
                item['time_close'], item['time_high'], item['time_low'], item['time_open'],
                item['timestamp'],
                item['volume'])
        except:
            print("yeah bro something wrong")
        return item


class RedisPipeline(object):

    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.serialize(item)
        self.server.rpush(key, data)
        return item
