from .api_base import ApiBaseObject
import pandas as pd


class Host(ApiBaseObject):

    def __init__(self, api, discovered_root):
        self.api = api
        self.discovered_root = discovered_root
    
    def search(self, term, **kwargs):
        """
        Finds all the matches in hosts of discovered environments. Default installation holds discovered environments under root env_id=5.
        """
        return self.api.Environment._search_env(term, True, env_id=self.discovered_root)
    

    def get_by_name(self, name, **kwargs):
        """
        Returns the first host that matched given name
        """
        return self.search("^%s"%name)


    def get_by_id(self, term, **kwargs):
        """
        TODO: Returns host details by id.
        """
        return self.search("hostid=%s"%term)


    def list_discovered_env(self, detailed=True, stop_on_host=True, **kwargs):

        res = self.api.request("/html/scripts/export-environments-tree.jsp?action=download", {
            "set-element-name": "true",
            "download": "false",
            "simple": "false",
            "stop-on-host": stop_on_host,
            "add-env-data": detailed,
            "envId": self.discovered_root
            }, records_path="Next.Root.Host", **kwargs)

        return res

    def list(self, **kwargs):
        return self.api.request("/next/hosts?action=get", {}, records_path="Next.Host", **kwargs)

