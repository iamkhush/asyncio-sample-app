from datetime import datetime, timedelta


def memoize(f):
    store = {}

    def wrapper(*args):
        now = datetime.now()
        cached_until = now + timedelta(seconds=60)
        if store:
            if store['cached_until'] < now:
                store.update({'cached_until': cached_until, 'result': f(*args)})
        else:
            store.update({'cached_until': cached_until, 'result': f(*args)})
        return store['result']

    return wrapper