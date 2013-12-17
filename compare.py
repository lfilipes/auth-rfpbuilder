from google.appengine.ext import webapp
from dbmodel import *
from session import *
from caching import *
import json
import datetime
import logging

def CompareDevices(include, exclude=None):
    first = True
    features_in = []
    for dev_id in include:
        dev = getBuffObj(db.Key(dev_id))
        if first:
            features_in = dev.features
            first = False
        else:
            dv_features = dev.features
            toremove = []
            for feat in features_in:
                if feat not in dv_features:
                    toremove.append(feat)
            # Loop to remove features from list
            for e in toremove:
                features_in.remove(e)
    features_ex = []
    if exclude:
        for dev_id in exclude:
            dev = getBuffObj(db.Key(dev_id))
            dv_features = dev.features
            for feat in features_in:
                if feat not in features_ex:
                    if feat not in dv_features:
                        features_ex.append(feat)
    result = {}
    result['include'] = features_in
    result['exclude'] = features_ex
    return result

class Compare(webapp.RequestHandler):
    def get(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        dev_include = self.request.get_all('include')
        dev_exclude = self.request.get_all('exclude')
        if not dev_include or len(dev_include)<2:
            self.response.out.write('At least 2 switches needed for comparison!')
            return
        features = CompareDevices(dev_include, dev_exclude)
        response = {}
        response_in = []
        for feat in features['include']:
            response_in.append(getBuffObj(feat).name)
        response['include'] = response_in
        response_ex = []
        for feat in features['exclude']:
            response_ex.append(getBuffObj(feat).name)
        response['exclude'] = response_ex
        self.response.out.write(json.JSONEncoder().encode(response))

class FinalRFPText(webapp.RequestHandler):
    def get(self):
        # First check session authorized
        if not checkSession(self):
            self.abort(403)
        else:
            self.response.set_cookie('session_key', self.request.cookies.get('session_key'), datetime.timedelta(hours=2), path='/')

        dev_include = self.request.get_all('include')
        lang = self.request.get('lang')
        if not dev_include or len(dev_include)<2:
            self.response.out.write('At least 2 switches needed to build an RFP!')
            return
        rfp_items = CompareDevices(dev_include)['include']
        features = Feature.get(rfp_items)
        cat_keys = []
        for f in features:
            cat = f.key().parent()
            if cat not in cat_keys:
                cat_keys.append(cat)
        categories = FeatureCategory.get(cat_keys)
        response = """<html><head><title>RFP Model</title>
        <link rel="stylesheet" href="/style/style.css" type="text/css" media="print, projection, screen" />
        </head><body>"""
        for cat in categories:
            if lang == 'por' and cat.name_por and cat.name_por != ' ':
                response += "<h2>" + cat.name_por + "</h2>"
            elif lang == 'spa' and cat.name_spa and cat.name_spa != ' ':
                response += "<h2>" + cat.name_spa + "</h2>"
            else:
                response += "<h2>" + cat.name_eng + "</h2>"
            for f in features:
                if f.key().parent() == cat.key():
                    if lang == 'por' and f.desc_por and f.desc_por != ' ':
                        response += "<p>" + f.desc_por + "</p>"
                    elif lang == 'spa' and f.desc_spa and f.desc_spa != ' ':
                        response += "<p>" + f.desc_spa + "</p>"
                    elif f.desc_eng and f.desc_eng != ' ':
                        response += "<p>" + f.desc_eng + "</p>"
                    else:
                        response += "<p>" + f.name + "</p>"
        response += "</body></html>"
        self.response.out.write(response)

app = webapp.WSGIApplication(
                                     [('/compare', Compare),
                                      ('/rfp', FinalRFPText)],
                                     debug=True)
