import webapp2
from models import *
import json
import utils

class MyHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

    #The dispatch is overwritten so we can respond to OPTIONS
    def dispatch(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.response.headers.add_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')
        if self.request.method.upper() == 'OPTIONS':
            self.response.status = 204
            self.response.write('')
        else:
            super(MyHandler, self).dispatch();


    def params_to_model(self, model, skip=None):
        if 'json' in self.request.headers['Content-Type']:
            params = json.loads(self.request.body)
        else:
            params = self.request.params
    
        ignore = ['created', 'updated', 'deleted', 'user_token']

        for k in params:
            if skip and k in skip:
                continue
            if k in ignore:
                continue
            value = params[k]
            if isinstance(value, basestring) and value.isdigit():
                value = int(value)
            setattr(model, k, value)

        return model

    def query_string_to_ndb_query(self, model, multidict):
        strings = []
        for item in multidict.items():
            if(item[0] == 'user_token'):
                continue
            strings.append(model+"."+item[0]+" == '"+item[1]+"'")
        return ", ".join(strings)


    def do_try(self, success, error=False):
        status_code = 200
        try:
            result = success()
            print status_code
            if result[1]:
                status_code = result[1]
            json_response = result[0]

        except Exception as inst:
            print inst
            if error:
                error()
            else:
                status_code = 500
                json_response = {
                    'error':'Request failed.'
                }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.status = status_code
        self.response.write(utils.GqlEncoder().encode(json_response))
            

class ExampleHandler(MyHandler):
    def get(self):
        def success():
            qs = self.query_string_to_ndb_query('Example', self.request.GET)
            if len(qs) > 0:
                result = Example.query(eval(qs), Example.deleted == None)
            else:
                result = Example.query(Example.deleted == None)

            example = [p.to_dict() for p in result.fetch()]
            json_response = {
                'items': example
            }
            return [json_response, 200]
        self.do_try(success)                     

    def post(self):
        def success():
            project = self.params_to_model(Example())
            project.status = 'p'
            project.put()
            json_response = {
                'id':project.key.id()
            }
            return [json_response, 201]
        self.do_try(success)

    def put(self, project_id):
        def success():
            find = Example.get_by_id(int(project_id))
            project = self.params_to_model(find)
            project.put()
            json_response = project.to_dict()
            return [json_response, 204]

        self.do_try(success)

application = webapp2.WSGIApplication([
    ('/example', ExampleHandler),
    ('/example/(\d+)', ExampleHandler)
], debug=True)
