import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse

import json
import time
import random

from .res.change import Change
from .res.configuration import Configuration
from .res.environment import Environment
from .res.host import Host
from .res.eql import EQL
from .res.login import Login
from .res.appdef import AppDef
from .res.api_result import ApiResultObject
from .res.blended import Blended
from .res.policy import Policy
from .res.search import Search



class EvolvenAPI():
    
    def __init__(self, host, port=443, username=None, password=None, 
                db_lib = "enlight_lib", db_main = "enlight_main", db_host=None,
                discovered_root_id=5, logical_root_id=3, debug=False, fake=False, 
                return_type="object", session_key=None, max_retries=5):

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db_lib = db_lib
        self.db_main = db_main
        self.db_host = db_host
        self.debug = debug
        self.fake = fake
        self.return_type = return_type
        self.discovered_root = discovered_root_id
        self.logical_root = logical_root_id
        self.max_retries = max_retries
        self.session_key_self_assigned = True


        self.Configuration  = Configuration(self)
        self.Change         = Change(self)
        self.Environment    = Environment(self)
        self.Host           = Host(self, discovered_root_id)
        self.EQL            = EQL(self)
        self.Login          = Login(self)
        self.AppDef         = AppDef(self)
        self.Blended        = Blended(self)
        self.Policy         = Policy(self)
        self.Search         = Search(self)

        if session_key is None:
            s_key = self.Login.login()
            if s_key is not None:
                self.session_key = s_key
                self.session_key_self_assigned = False
            else:
                raise Exception("Cannot login")
        else:
            self.session_key = sessionKey
            self.session_key_self_assigned = False



    def reset_session_key(self):
        self.session_key = str(int(time.time()))+str(random.getrandbits(5))
        self.session_key_self_assigned = True

    def set_session_key(self):
        self.session_key = str(int(time.time()))+str(random.getrandbits(5))
        self.session_key_self_assigned = False


    def _get_api_url(self, action):

        if not "?" in action:
            action = action+"?"
           

        url = "%(host)s:%(port)s/enlight.server%(action)s&json=true&pretty=true"%{
            "host": self.host,
            "port": self.port,
            "action": action,
        }

        return url
        

    def request(self, action, parameters, records_path=None, return_type=None, return_values=True, **kwargs):
        
        url = self._get_api_url(action)
        
        # querystring = {
        #     "db_lib": self.db_lib,
        #     "db_main": self.db_main,
        #     "db_host": self.db_host
        # }

        querystring = {}
        if not self.session_key_self_assigned:
            querystring.update({
                "EvolvenSessionKey": self.session_key
                })
        else:
            querystring.update({
                "user": self.username,
                "pass": self.password,
                }) 

        querystring.update(parameters)
        querystring.update(kwargs)

        url += "&" + urllib.parse.urlencode(querystring)


        if self.debug:
            print(url)

        if not self.fake:
            res = None
            n_retries = 0

            while res is None and n_retries < self.max_retries:
                try:
                    req = urllib.request.urlopen(url, timeout=120)
                    res = req.read().decode('ascii', 'ignore')
                except urllib.error.URLError:
                    n_retries +=1
                    print('URL request failed (%s/%s). Trying again.'%(n_retries, self.max_retries))
                    time.sleep(2)
                    pass

            if return_values:
                return self._parse_response(res, url, records_path, return_type)
        
        return "{}"



    def _dict2obj(self, d):
        return json.loads(json.dumps(d), object_hook=ApiResultObject)
    
    def _parse_response(self, response, url=None, records_path=None, return_type=None):

        if return_type is None:
            return_type = self.return_type
        
        data = json.loads(response)
                
        if url is not None and type(data) is not list:
            data["url"] = url

        # return as string
        if return_type == "string":
           return json.dumps(data)

        # return as json
        elif return_type == "json":
            return data

        # return as DataFrame
        elif return_type == "DataFrame":
            if records_path is not None:
                res = self._dict2obj(data)
                return res.toDataFrame(records_path)

        # return as obj by default
        return self._dict2obj(data)


    def search_to_count(self, result):
        return int(result["Next"]["Count"])

