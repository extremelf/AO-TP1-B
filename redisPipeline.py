
class RedisPipeline(object):
    def __init__(self):
        print("ola")

    def process_item(self, item, spider):
        print(item)
        return item
