from .api_base import ApiBaseObject
import pandas as pd


class Search(ApiBaseObject):

    def __init__(self, api):
        self.api = api
    
    def search(self, query, env_id=None, **kwargs):

        if env_id is None:
            env_id = self.api.discovered_root

        res = self.api.request("/html/scripts/api/assets.jsp", {
            "globalCrit": query,
            "envId": env_id,
            "all": True,
            "action": "table",
            }, records_path="Next.Table.Rows.Row", **kwargs)

        return res

