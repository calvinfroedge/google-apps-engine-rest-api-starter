import unittest
import webtest
import webapp2
from google.appengine.ext import ndb
from models import *
from main import *
from google.appengine.ext import testbed

class ProjectHandlerTest(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication([('/projects', ProjectHandler)])
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
    
    def tearDown(self):
        self.testbed.deactivate()

    def test_postProject(self):
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        params = {'name': 'calvin', 'description': 'test'}
        response = self.testapp.post('/projects', params)
        self.assertEqual(response.status_int, 201)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    for method in dir(MyHandlerTest):
       if method.startswith("test"):
          suite.addTest(MyHandlerTest(method))
    unittest.TextTestRunner().run(suite)
