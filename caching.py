from google.appengine.api import memcache
from dbmodel import *

def getBuffObj(key):
    strkey = str(key)
    obj = memcache.get(strkey)
    if obj is None:
        obj = db.get(key)
        memcache.add(strkey, obj, 600)
    return obj
