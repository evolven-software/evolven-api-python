from .api_base import ApiBaseObject


class Environment(ApiBaseObject):

    def search(self, term, env_id, **kwargs):
        return self._search_env(term, False, env_id)

    def search_logical_env(self, term, env_id=3, **kwargs):
        return self._search_env(term, False, env_id)

    def search_discovered_env(self, term, host_id=5, **kwargs):
        return self._search_env(term, False, host_id)

    def list(self, flat=True, **kwargs):
        res = self.api.request("/html/scripts/export-environments-tree.jsp?action=download", {
            "set-element-name": "true",
            "download": "false",
            "simple": "false",
            "stop-on-host": "false",
            "add-env-data": "true"
        })

        if not flat:
            return res

        res_list = []
        for root in res.Next.Root:
            if hasattr(root, "Host"):
                for host in root.Host:
                    self._flatten_env(host, res_list, "Environment")
            if hasattr(root, "Root"):
                for folder in root.Folder:
                    self._flatten_env(folder, res_list, "Folder")

        return res_list

    def get_children(self, env_id, **kwargs):
        return self.api.request("/next/Environments?action=children", {
            "envId": "%s" % env_id,
            "selectedTab": "Inventory",
            "ChangesContext": "Inventory"
        })

    def get_children_ids(self, env_id, **kwargs):
        return self.api.request("/next/Environments?action=descendants", {
            "EnvIdOnly": "true",
            "HasConfig": "true",
            "envId": "%s" % env_id,
            "selectedTab": "Inventory",
            "ChangesContext": "Analysis",
        })

    def _flatten_env(self, root, res_list, attr):
        if hasattr(root, attr):
            sub_env = getattr(root, attr)
            if type(sub_env) == list:
                for env in sub_env:
                    self._flatten_env(env, res_list, attr)
            else:
                self._flatten_env(sub_env, res_list, attr)
            delattr(root, attr)
        res_list.append(root)


    def _search_env(self, term, hosts_only=False, env_id=-1):
        params = {
            "Rows": -1,
            "Page": -1,
            "crit": term,
            "folder": "false",
            "idx": 0,
            "count": 0,
            "compareTo": 0,
            "filter": "false",
            "hosts":  hosts_only,
            "history": "false"}
        if int(env_id) > 0:
            params["env_id"] = env_id

        return self.api.request("/next/Environments?action=search", params, records_path="Next.Environment")

    def get_summary(self, env_id, **kwargs):
        return self.api.request("/next/Environments?action=summary", {
            "envId": "%s" % env_id
        }, **kwargs)
