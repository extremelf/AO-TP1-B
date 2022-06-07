import redis


def connection_pool():
    r = redis.Redis(
        host='localhost',
        port=6379,
        password='lepass420')

    return r
