from google.appengine.ext import webapp
from google.appengine.api import mail
from dbmodel import *
from session import *
from caching import *
import datetime

class AddDeviceType(webapp.RequestHandler):
    def post(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        dev_type_name = self.request.get('name')
        dev_type_key = self.request.get('key')
        msg = "Failure"
        if dev_type_name:
            if dev_type_key:
                dev_type = getBuffObj(db.Key(dev_type_key))
                dev_type.name = dev_type_name
                msg = 'Device Type Updated'
                memcache.delete(dev_type_key)
            else:
                dev_type = DeviceType(name=dev_type_name)
                msg = 'Device Type Added'
            dev_type.put()
        self.response.out.write(msg)

class AddFeatureCategory(webapp.RequestHandler):
    def post(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        fc_name_eng = self.request.get('name_eng')
        fc_name_spa = self.request.get('name_spa')
        fc_name_por = self.request.get('name_por')
        dv_type = self.request.get('dv_type')
        fc_key = self.request.get('key')
        msg = "Failure"
        if fc_name_eng and dv_type:
            if fc_key:
                category = getBuffObj(db.Key(fc_key))
                category.name_eng = fc_name_eng
                msg = "Feature Category Updated"
                memcache.delete(fc_key)
            else:
                device_type = getBuffObj(db.Key(dv_type))
                category = FeatureCategory(parent=device_type, name_eng=fc_name_eng)
                msg = "Feature Category Added"
            if fc_name_spa:
                category.name_spa = fc_name_spa
            if fc_name_por:
                category.name_por = fc_name_por
            category.put()
        self.response.out.write(msg)

class AddFeature(webapp.RequestHandler):
    def post(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        feat_name = self.request.get('name')
        cat_key = self.request.get('category')
        feat_key = self.request.get('key')
        feat_desc_eng = self.request.get('desc_eng')
        feat_desc_spa = self.request.get('desc_spa')
        feat_desc_por = self.request.get('desc_por')
        msg = "Failure"
        if feat_name and cat_key:
            if feat_key:
                feat = getBuffObj(db.Key(feat_key))
                feat.name = feat_name
                msg = "Feature Updated"
                # Flush Memcache
                memcache.delete(feat_key)
            else:
                cat = getBuffObj(db.Key(cat_key))
                feat = Feature(parent=cat, name=feat_name)
                msg = "Feature Added"
            if feat_desc_eng:
                feat.desc_eng = feat_desc_eng
            if feat_desc_spa:
                feat.desc_spa = feat_desc_spa
            if feat_desc_por:
                feat.desc_por = feat_desc_por
            feat.put()
            # Flush Memcaches
            memcache.delete('featbyfc=' + cat_key)
            memcache.delete('featbydt=' + str(db.Key(cat_key).parent()))
        self.response.out.write(msg)

class AddDevice(webapp.RequestHandler):
    def post(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        dev_vendor = self.request.get('vendor')
        dev_model = self.request.get('model')
        dev_desc = self.request.get('description')
        dev_key = self.request.get('key')
        dev_type_key = self.request.get('device_type')
        msg = "Failure"
        if dev_vendor and dev_model and dev_type_key:
            if dev_key:
                dev = getBuffObj(db.Key(dev_key))
                dev.vendor = dev_vendor
                dev.model = dev_model
                msg = "Device Updated"
                memcache.delete(dev_key)
            else:
                dev_type = getBuffObj(db.Key(dev_type_key))
                dev = Device(parent=dev_type, vendor=dev_vendor, model=dev_model, features=[])
                msg = "Device Added"
            if dev_desc:
                dev.description = dev_desc
            dev.put()
        self.response.out.write(msg)

class AddDeviceFeature(webapp.RequestHandler):
    def post(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        dev_key = self.request.get('device')
        feat_key = self.request.get('feature')
        support = self.request.get('support')
        msg = "Error!"
        if dev_key and feat_key:
            dev = getBuffObj(db.Key(dev_key))
            if support == 'true':
                dev.features.append(db.Key(feat_key))
                dev.put()
                msg = "Feature Added!"
            else:
                dev.features.remove(db.Key(feat_key))
                dev.put()
                msg = "Feature Removed!"
            memcache.delete(dev_key)
            memcache.delete('dfbydev=' + dev_key)
        self.response.out.write(msg)

class AddToken(webapp.RequestHandler):
    def post(self):
        tk_token = self.request.get('token')
        tk_user = self.request.get('user')
        tk_email = self.request.get('email')
        if tk_token and tk_user and tk_email:
            token = AccessToken(token=tk_token, user=tk_user, email=tk_email)
            token.put()
            self.response.out.write('Token Added')
            return
        self.response.out.write('Failure')

class EmailToken(webapp.RequestHandler):
    def post(self):
        tk_token = self.request.get('token')
        if tk_token:
            tk = db.get(db.Key(tk_token))
            mail.send_mail(sender="Daniel Garcia <danidoo@gmail.com>",
                           to=tk.user + " <" + tk.email + ">",
                           subject="Your rfpbuilder token",
                           body="Dear " + tk.user + """,

Here is your RFP Builder token: """ + tk.token + """ 

Thanks,
RFP Builder Team
http://rfpbuilder.appspot.com""")

            self.response.out.write('E-mail sent')
            return
        self.response.out.write('Failure')

app = webapp.WSGIApplication(
                                     [('/add/device_type', AddDeviceType),
                                      ('/add/feature_category', AddFeatureCategory),
                                      ('/add/feature', AddFeature),
                                      ('/add/device', AddDevice),
                                      ('/add/device_feature', AddDeviceFeature),
                                      ('/add/token', AddToken),
                                      ('/add/email_token', EmailToken)],
                                     debug=True)
