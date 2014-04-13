import os,bmemcached
mc = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
        os.environ.get('MEMCACHEDCLOUD_USERNAME'),
        os.environ.get('MEMCACHEDCLOUD_PASSWORD'))
print repr(mc.get('stale_scores')).replace("],","],\n")
