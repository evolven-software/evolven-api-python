from .api_base import ApiBaseObject

class Blended(ApiBaseObject):

	def list(self, env_id, start=0, end='now', **kwargs):
		return self.api.request("/next/blended", {
			'action': 'get',
			'envId': env_id,
			'start': start,
			'end': end
			}, records_path="Next.Record", **kwargs)

	def get(self, blended_id, **kwargs):
		return self.api.request("/next/blended", {
			'action': 'get',
			'id': blended_id,
			}, records_path="Next.Record", **kwargs)


	def create(self, event_source, event_id, event_name, event_message, event_start, event_end, event_hosts, event_deeplink, **kwargs):
		return self.api.request("/next/blended", {
			'action': 'create',
			'delete': True,
			'Source': event_source,
			'eventId': event_id,
			'event': event_name,
			'Message': event_message,
			'Start': event_start,
			'End': event_end,
			'host': event_hosts,
			'DeepLink': event_deeplink,
			}, records_path="Next", **kwargs)


	def investigate(self, event_id, **kwargs):
		return self.api.request("/html/scripts/changes-tree-summary.jsp", {
			# 'GroupBy': 'analysis-filter',
			'blended-environment': event_id
			}, records_path="Next", **kwargs)
