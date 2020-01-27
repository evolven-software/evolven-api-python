from .api_base import ApiBaseObject

class EQL(ApiBaseObject):
    
    def execute(self, query, **kwargs):
        """
        Parses query and returns a deeplink to product.
        """
        if self.api.debug:
        	print(query)
        return self.api.request("/next/changes?action=getEvolvenQueryLanguage", {
            "content": query.replace(" ", "+")
            })

