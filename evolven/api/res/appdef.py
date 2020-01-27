from .api_base import ApiBaseObject


class AppDef(ApiBaseObject):
    
    def list(self, table="false", **kwargs):
        return self.api.request("/next/appDef?", {
            "action": "list",
            "table": table
        }, **kwargs)

    def get(self, guid, **kwargs):
        return self.api.request("/next/appDef?", {
            "action": "get",
            "guid": guid
            }, **kwargs)
