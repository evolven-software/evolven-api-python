from .api_base import ApiBaseObject
import pandas

class Policy(ApiBaseObject):

    def list(self, **kwargs):
        """
        Get all policies
        """
        return self.api.request("/next/policy", {
            "action":"get",
            "returnStatus":"false",
            }, records_path="Next.Rule", **kwargs)


    def get(self, id, env_id=None, **kwargs):
        """
        Get policy details. If env_id is set, it returns policy results only for 
        specific environment (it could be logical env)
        """

        return self.api.request("/next/policy", {
            "action":"getResult",
            "json":"true",
            "RuleId":id,
            "envId":env_id,
            }, records_path="Next.Environment", **kwargs)




