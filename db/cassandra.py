from cassandra.cluster import Cluster


class CassandraPipeline(object):

    def __init__(self, cassandra_keyspace):
        self.cassandra_keyspace = 'coin_keyspace'

    def open_spider(self, spider):
        cluster = Cluster()
        self.session = cluster.connect(self.cassandra_keyspace)

    def process_item(self, item, spider):
        # insert item
        self.session.execute("INSERT INTO crypto_coin (item) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                             item['name'], item['marketCap'], item['price_close'], item['price_high'],
                             item['price_low'], item['price_open'],
                             item['time_close'], item['time_high'], item['time_low'], item['time_open'],
                             item['timestamp'],
                             item['volume'])
        return item
