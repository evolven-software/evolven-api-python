from .api_base import ApiBaseObject


class Configuration(ApiBaseObject):

	ELEMENT_TYPE = {
		"34301": "Environment",
		"34302": "Tree",
		"34303": "Node",
		"34304": "Attribute",
		"34305": "Table",
		"34306": "Table Row",
		}
	
	def search(self, term, env_id, search_children=True, search_tables=True, **kwargs):
		"""
		Finds all the CIs under specific environment and its' children.
		"""
		# get all childs
		childs = []

		if search_children:
			data = self.api.Environment.get_children_ids(env_id).Next.envId
			childs = data if type(data) == list else []
			childs.append("%s"%env_id)

		return self.api.request("/next/configurationTree", {
			"action": "search",
			"Rows":"-1",
			"Page":"1",
			"Search":"%s"%term,
			"envId":"%s"%env_id,
			"Att":"true",
			"Table":"%s"%search_tables,
			"offset":"0",
			"selectedTab":"Inventory",
			"ChangesContext":"Dashboard",
			"term": term,
			"env_id": ",".join(childs),
			"search_tables": search_tables,
			}, records_path="Next.Node", **kwargs)


	def list(self, env_id, **kwargs):
		return self.api.request("/next/configurationTree", {
			"action": "setEnv",
			"envId": env_id
		}, records_path="Next.Node", **kwargs)



	def get_children(self, node_id, env_id=None, **kwargs):
		self.__init_config_tree(env_id)
		return self.api.request("/next/configurationTree", {
			"action": "children",
			"nodeId":"%s"%node_id,
			"Rows":"-1",
			"Page":"1"
			}, records_path="Next.Node", **kwargs)


	def get_node_by_path(self, env_id, node_path, parent_node=None):

		if not type(node_path) is list:
			node_path = node_path.split("/")
		
		nodes = None
		if parent_node is not None:
			nodes = self.get_children(node_id=parent_node.ID)
		else:
			nodes = self.list(env_id=env_id)
			
		for idx, node in nodes.iterrows():
			if node.Name == node_path[0]:
				if len(node_path) == 1:
					return node
				return self.get_node_by_path(env_id, node_path[1:], node)
		
		return None


	# def get(self, node_id, env_id=None, **kwargs):
	# 	self.__init_config_tree(env_id)
	# 	return self.api.request("/next/configurationTree", {
	# 		"action": "details",
	# 		"id": "%s"%node_id
	# 		}, **kwargs)

	# def get_table(self, node_id, env_id=None, **kwargs):
	# 	self.__init_config_tree(env_id)
	# 	return self.api.request("/next/configurationTree", {
	# 		"action": "table",
	# 		"nodeId": "%s"%node_id,
	# 		"selectedTab": "Inventory",
	# 		"ChangesContext": "Dashboard",
	# 		}, **kwargs)


	def __init_config_tree(self, env_id):
		if env_id is not None:
			self.list(env_id)
