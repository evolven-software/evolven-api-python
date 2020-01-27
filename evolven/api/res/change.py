from .api_base import ApiBaseObject
import pandas

class Change(ApiBaseObject):

    calculated_fields = [
        "CI", "Category", "Compliant", "diff-action", "diff-object-name", "Dynamic", "is-ignore", 
        "Loneliness", "SystemTag", "actionString", "applicationLayer", "artifact", 
        "closed", "comment", "file-type", "freq", "impact-area", "it-action", 
        "logical-layer", 
        "relative-change", "server-component", "suspect", "time-anomaly", "type-violation", "is-toggle",
        "value-anomaly", "value-type", 
        "application-definition"
        ]

    _default_fields = ['AnnotatedDescription', 'Authorized', 'AuthorizedCause', 'CISubType', 'CIType', 'ChangeType', 'Class', 'Consistency', 'ConsistencyKey', 'ConsistencyPercent', 'CurrentValue', 'EnvClass', 'Environment', 'EnvironmentName', 'EnvironmentType', 'FullPath', 'History', 'Host', 'HostClass', 'HostType', 'ID', 'Icon', 'IsChange', 'Item', 'LastItem', 'LastPath', 'Name', 'NoiseCategory', 'Operation', 'Os', 'OsIcon', 'Parameter', 'Path', 'PreviousValue', 'RiskDescription', 'RiskLevel', 'RiskNodeId', 'RiskScenario', 'RiskSimpleLevel', 'Riskscore', 'Significances', 'StartTime', 'State', 'Time', 'Type', 'envId', 'hostId']
    
    def list(self, env_id, start=0, end="now", filter='', fields=None, details=True, count=100000, group_by=None, setup_analysis=False, **kwargs):
        """
        Get all changes for particular environment
        """
        if setup_analysis:
            self.set_up_analysis(env_id, start, end)

        if fields == None:
            fields = self.calculated_fields

        res = self.api.request("/html/scripts/changes-tree-summary.jsp", {
            "envId": env_id,
            "start": start,
            "end": end,
            "details": details,
            "count": count,
            "groupBy": group_by,
            "crit": filter,
            "field": ",".join(fields) if fields is not None else ""
            }, records_path="Next.Changes.Change", **kwargs)

        return self._normalize_fields(res, fields)


    def set_comment(self, change_ids, env_id, comment, **kwargs):
        """
        Add comments
        """
        if type(change_ids) is list:
            change_ids = ",".join(map(str, change_ids))

        
        # Only now you can Mark as suspect
        return self.api.request('/next/changes',{
            'action': 'comment',
            'ids': change_ids,
            'Comment': comment,
            'selectedTab': 'Analysis',
            'ChangesContext': 'Analysis',
            'returnStatus':False
            }, **kwargs)


    def set_suspect_tag(self, change_id, env_id, remove=None, start=0, end='now', **kwargs):
        """
        Add suspect tag to the specific change
        """
        action = 'tag' if remove == None else 'untag'

        self.set_up_analysis(env_id = env_id, start=start, end=end, **kwargs)
        
        # Only now you can Mark as suspect
        return self.api.request('/next/changes',{
            'action': action,
            'ids': change_id,
            'selectedTab': 'Analysis',
            'ChangesContext': 'Analysis',
            }, **kwargs)

    def set_authorization(self, change_id, env_id, state, start=0, end='now', **kwargs):
        """
        Set change as authorized
        """

        self.set_up_analysis(env_id = env_id, start=start, end=end, **kwargs)

        return self.api.request('/next/changes', {
            'action': 'setAuthorized',
            'ids':change_id,
            'cause': 'Authorization+changed+via+evolvenBot',
            'selectedTab': 'Analysis',
            'ChangesContext': 'Analysis',
            'state': state # 1: authorized, -1: unathorized, 0: no data
            }, **kwargs)


    def set_up_analysis(self, env_id, start=0, end='now', **kwargs):
        """
        Set up analysis properties.
        """
        # First, set analysis
        self.api.request('/next/analysisDashboard',{
            'action': 'getAnalysis',
            'envId': env_id,
            'start': start,
            'end': end,
            'reload': True,
            'monitoring': True,
            'filter': 0,
            }, **kwargs)

        # Set cluster
        self.api.request('/next/changes', {
            'action': 'setCluster',
            'ids': 0,
            'cluster': True,
            'envId': env_id,
            'start': start,
            'end': end,
            }, **kwargs)
        
        # Get all changes
        self.api.request('/next/changes', {
            'action': 'getChanges',
            'type': 'cluster',
            'ids': 0,
            'Monitoring': True,
            'envId': env_id,
            'start': start,
            'end': end,
            }, **kwargs)


    def fields(self):
        return self.api.request('/next/options', {"type":"diff-field"}, records_path="Next.Option")


    def _normalize_fields(self, res, extra_fields):

        if res is not None and type(res) == pandas.core.frame.DataFrame and len(res) > 0:

            if "AnnotatedDescription" in res:
                res["AnnotatedDescription"] = [
                    " ".join([el["Text"] for el in record]) 
                    for record in res["AnnotatedDescription"]]

            if "Operation" in res:
                operation_type = {
                    "130": "PROPERTY UPDATE", 
                    "131": "PROPERTY ADD",
                    "132": "PROPERTY REMOVE",
                    "133": "NODE ADD",
                    "134": "NODE REMOVE"
                }
                res["Operation"] = [operation_type[record] if record in operation_type else "?" 
                                        for record in res["Operation"]]

            # Extra fields
            cng_list = []
            for record in res.Fields:
                cng = {}
                for field in record.Field:        
                    cng[field.Name] = field.Value
                for field in extra_fields:
                    if field not in cng:
                        cng[field] = "null"
                cng_list.append(cng)

            cng_df = pandas.DataFrame.from_dict(cng_list)

            res = pandas.concat([res, cng_df], axis=1)
            res = res.drop(['Fields'], axis=1)

            # Make sure all the default fields are present
            for field in self._default_fields:
                if field not in res:
                    res[field] = [''] * len(res)

            # sort columns to make sure they appeary in the same order
            res = res.reindex_axis(sorted(res.columns), axis=1)

        return res

    def get_timeline(self, env_id, start=0, end='now', **kwargs):
        
        self.set_up_analysis(env_id=env_id, start=start, end=end)

        return self.api.request('/next/analysisDashboard', {
            'action': 'getTimeline',
            'type': 'cluster',
            'ids' : 0,
            'envId': env_id,
            'start': start,
            'end': end
            })


