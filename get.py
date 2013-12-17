from google.appengine.ext import webapp
from google.appengine.api import memcache
from dbmodel import *
from session import *
from caching import *
import json
import datetime
import logging

class GetDeviceType(webapp.RequestHandler):
    def get(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        device_types = []
        dev_type_key = self.request.get('key')
        dev_types = DeviceType.all()
        if dev_type_key:
            dev_types.filter("__key__ =", db.Key(dev_type_key))
        for dev_type in dev_types:
            device_type = {}
            device_type['key'] = str(dev_type.key())
            device_type['name'] = dev_type.name
            device_types.append(device_type)
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.JSONEncoder().encode(device_types))

class GetFeatureCategory(webapp.RequestHandler):
    def get(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        feature_categories = []
        dev_type_key = self.request.get('device_type')
        fc_key = self.request.get('key')
        fcs = FeatureCategory.all()
        if dev_type_key:
            fcs.ancestor(db.Key(dev_type_key))
        if fc_key:
            fcs.filter("__key__ = ", db.Key(fc_key))
        for fc in fcs:
            feature_category = {}
            dev_type = getBuffObj(fc.key().parent())
            feature_category['key'] = str(fc.key())
            feature_category['name_eng'] = fc.name_eng
            feature_category['name_spa'] = fc.name_spa
            feature_category['name_por'] = fc.name_por
            feature_category['device_type_name'] = dev_type.name
            feature_category['device_type_key'] = str(dev_type.key())
            feature_categories.append(feature_category)
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.JSONEncoder().encode(feature_categories))

class GetFeature(webapp.RequestHandler):
    def get(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        feat_key = self.request.get('key')
        dev_type_key = self.request.get('device_type')
        feat_category = self.request.get('feature_category')
        features = []
        if feat_key:
            feats = Feature.all()                
            feats.filter("__key__ = ", db.Key(feat_key))
        else:
            if feat_category:
                b = memcache.get('featbyfc=' + feat_category)
                if b:
                    feats = b
                    logging.info('Cache Hit for featbyfc=' + feat_category)
                else:
                    feats = Feature.all()
                    feats.ancestor(db.Key(feat_category))
                    feats = list(feats)
                    memcache.add('featbyfc=' + feat_category, feats, 600)
            else:
                if dev_type_key:
                    b = memcache.get('featbydt=' + dev_type_key)
                    if b:
                        feats = b
                        logging.info('Cache Hit for featbydt=' + dev_type_key)
                    else:
                        feats = Feature.all()
                        feats.ancestor(db.Key(dev_type_key))
                        feats = list(feats)
                        memcache.add('featbydt=' + dev_type_key, feats, 600)
        for feat in feats:
            feature = {}
            feature['key'] = str(feat.key())
            feature['name'] = feat.name
            cat = getBuffObj(feat.key().parent())
            feature['category_name'] = cat.name_eng
            feature['category_key'] = str(cat.key())
            dev_type = getBuffObj(cat.key().parent())
            feature['device_type_key'] = str(dev_type.key())
            feature['desc_eng'] = feat.desc_eng
            feature['desc_spa'] = feat.desc_spa
            feature['desc_por'] = feat.desc_por
            features.append(feature)
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.JSONEncoder().encode(features))

class GetDevice(webapp.RequestHandler):
    def get(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        devices = []
        dev_type_key = self.request.get('device_type')
        dev_key = self.request.get('key')
        devs = Device.all()
        if dev_type_key:
            # Filter devices by Device Type
            devs.ancestor(db.Key(dev_type_key))
        if dev_key:
            devs.filter("__key__ = ", db.Key(dev_key))
        for dev in devs:
            device = {}
            device['key'] = str(dev.key())
            device['vendor'] = dev.vendor
            device['model'] = dev.model
            device['description'] = dev.description
            dev_type = getBuffObj(dev.key().parent())
            device['device_type_name'] = dev_type.name
            device['device_type_key'] = str(dev_type.key())
            devices.append(device)
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.JSONEncoder().encode(devices))

    
class GetDeviceFeatures(webapp.RequestHandler):
    def get(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        device = self.request.get('device')
        feat_category = self.request.get('feature_category')
        if not device:
            self.response.out.write('Error')
            return
        if not feat_category:
            out = memcache.get('dfbydev=' + device)
            if out:
                logging.info('Cache Hit for dfbydev=' + device)
                self.response.out.write(out)
                return
        response = {}
        dev = getBuffObj(db.Key(device))
        response['device_vendor'] = dev.vendor
        response['device_model'] = dev.model
        response['device_key'] = str(dev.key())
        if feat_category:
            b = memcache.get('featbyfc=' + feat_category)
            if b:
                feats = b
                logging.info('Cache Hit for featbyfc=' + feat_category)
            else:
                feats = Feature.all()
                feats.ancestor(db.Key(feat_category))
                feats = list(feats)
                memcache.add('featbyfc=' + feat_category, feats, 600)
        else:
            dt = dev.key().parent() # Device Type
            b = memcache.get('featbydt=' + str(dt))
            if b:
                feats = b
                logging.info('Cache Hit for featbydt=' + str(dt))
            else:
                feats = Feature.all()
                feats.ancestor(dt) # Filter features per device type
                feats = list(feats)
                memcache.add('featbydt=' + str(dt), feats, 600)
        features = {}
        dev_features = []
        for dev_feat in dev.features:
            dev_features.append(dev_feat)
        for feat in feats:
            feature = {}
            feature['feat_name'] = feat.name
            feat_key = feat.key()
            if feat_key in dev_features:
                feature['supported'] = True
            else:
                feature['supported'] = False
            features[str(feat_key)] = feature
        response['features'] = features
        out = json.JSONEncoder().encode(response)
        memcache.add('dfbydev=' + device, out, 600)
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(out)

class GetToken(webapp.RequestHandler):
    def get(self):
        tokens = []
        tks = AccessToken.all()
        for tk in tks:
            token = {}
            token['key'] = str(tk.key())
            token['token'] = tk.token
            token['user'] = tk.user
            token['email'] = tk.email
            token['lastlogin'] = str(tk.lastlogin)
            tokens.append(token)
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.JSONEncoder().encode(tokens))

class GetSession(webapp.RequestHandler):
    def get(self):
        sessions = []
        ses = Session.all()
        for s in ses:
            session = {}
            session['start'] = str(s.start)
            token = db.get(s.key().parent())
            session['user'] = token.user
            sessions.append(session)
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.JSONEncoder().encode(sessions))

app = webapp.WSGIApplication(
                                     [('/get/device_type', GetDeviceType),
                                      ('/get/feature_category', GetFeatureCategory),
                                      ('/get/feature', GetFeature),
                                      ('/get/device', GetDevice),
                                      ('/get/device_features', GetDeviceFeatures),
                                      ('/get/token', GetToken),
                                      ('/get/session', GetSession)],
                                     debug=True)
