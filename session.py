from dbmodel import *
from google.appengine.api import memcache

def checkSession(req):
    session_key = req.request.cookies.get('session_key')
    if session_key:
        s = memcache.get(session_key)
        if s:
            return True
        else:
            session = db.get(db.Key(session_key))
            if session:
                memcache.add(session_key, session, 1200)
                return True
    return False
