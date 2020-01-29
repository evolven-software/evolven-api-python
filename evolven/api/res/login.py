from .api_base import ApiBaseObject

class Login(ApiBaseObject):

	def login(self, user=None, password=None, **kwargs):
		res = self.api.request("/next/api?action=login", {
            'user': user if user else self.api.username,
            'pass': password if password else self.api.password
           })
		try:
			return res.Next.ID
		except:
			return None