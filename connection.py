import sys

import six

from scrapy.utils.misc import load_object

import defaults

# Shortcut maps 'setting name' -> 'parmater name'.
SETTINGS_PARAMS_MAP = {
    'REDIS_USERNAME': 'redis 6.0',
    'REDIS_PASSWORD': 'lepass420',
    'REDIS_DB': 0,
    'REDIS_URL': 'redis://redis6.0:lepass420@localhost:6379',
    'REDIS_HOST': 'localhost',
    'REDIS_PORT': 6379,
    'REDIS_ENCODING': 'encoding',
}

if sys.version_info > (3,):
    SETTINGS_PARAMS_MAP['REDIS_DECODE_RESPONSES'] = 'decode_responses'


def get_redis_from_settings(settings):
    params = defaults.REDIS_PARAMS.copy()
    params.update(settings.getdict('REDIS_PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])

    return get_redis(**params)


# Backwards compatible alias.
from_settings = get_redis_from_settings


def get_redis(**kwargs):
    redis_cls = kwargs.pop('redis_cls', defaults.REDIS_CLS)
    url = kwargs.pop('url', None)
    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)
