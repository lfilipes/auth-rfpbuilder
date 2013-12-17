from google.appengine.ext import db

class DeviceType(db.Model):
    name = db.StringProperty()

class FeatureCategory(db.Model):
    # Child of DeviceType
    name_eng = db.StringProperty()
    name_spa = db.StringProperty()
    name_por = db.StringProperty()

class Feature(db.Model):
    # Child of FeatureCategory
    name = db.StringProperty()
    desc_eng = db.StringProperty()
    desc_spa = db.StringProperty()
    desc_por = db.StringProperty()

class Device(db.Model):
    vendor = db.StringProperty()
    model = db.StringProperty()
    description = db.StringProperty()
    features = db.ListProperty(db.Key)

class AccessToken(db.Model):
    token = db.StringProperty()
    user = db.StringProperty()
    email = db.EmailProperty()
    lastlogin = db.DateTimeProperty(auto_now=True)

class Session(db.Model):
    start = db.DateTimeProperty(auto_now=True)


# borrador
#class DeviceFeatures(db.Model):
#    device = db.KeyProperty()
#    feature = db.KeyProperty()
#    owner = db.KeyProperty()
#    url
#    valid = db.BooleanProperty()
#    created = db.DateTimeProperty(auto_now=True)