import uuid as uuid
from cassandra.cluster import Cluster
from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread

import connection
import defaults

default_serialize = ScrapyJSONEncoder().encode


class CassandraPipeline(object):

    def __init__(self, cassandra_keyspace):
        self.cassandra_keyspace = "coin_keyspace"

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
            self.session.execute(
                "INSERT INTO crypto_coin (id, name, marketCap,price_close,price_high,price_low,price_open,time_close,time_high, time_low, time_open,timestamp,volume) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    uuid.uuid4(),
                    item['name'], item['marketCap'], item['price_close'], item['price_high'],
                    item['price_low'], item['price_open'],
                    item['time_close'], item['time_high'], item['time_low'], item['time_open'],
                    item['timestamp'],
                    item['volume']))
        except Exception:
            print("yeah bro something wrong")
        return item


class RedisPipeline(object):

    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = serialize_func

    print("lol i am here 1")

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

    print("lol i am here2")

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    print("lol i am here3")

    def _process_item(self, item, spider):
        print("lol i am here4")
        key = self.item_key(item, spider)
        print("lol i am here5")
        data = self.serialize(item)
        print("lol i am here6")
        self.server.rpush(key, data)
        print("redis time")
        return item

    def item_key(self, item, spider):

        return self.key % {'spider': spider.name}
