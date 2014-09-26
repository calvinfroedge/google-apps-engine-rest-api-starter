from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel
import datetime

class ModelUtils(object):
    def to_dict(self):
        result = super(ModelUtils,self).to_dict()
        result['id'] = self.key.id() #get the key as a string
        del result['class_']
        return result

class Meta(polymodel.PolyModel):
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.DateTimeProperty()


class Example(ModelUtils,Meta,ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    user_id = ndb.StringProperty()
    status = ndb.StringProperty()
