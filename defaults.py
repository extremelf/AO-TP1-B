import redis
PIPELINE_KEY = '%(spider)s:items'

REDIS_CLS = redis.StrictRedis
REDIS_ENCODING = 'utf-8'

REDIS_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
    'encoding': REDIS_ENCODING,
}