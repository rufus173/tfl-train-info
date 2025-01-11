import requests
class CachedRequests():
	__cached_requests = {
		"get": [],
	}
	def cached_get_request(self,url):
		for request in self.__cached_requests["get"]:
			if request[0] == url:
				return request[1]
		response = requests.get(url)
		response.raise_for_status()
		if response.ok == False:
			raise Exception(f"{response.status} - {response.reason}")
		self.__cached_requests["get"].append((url,response))
		return response
