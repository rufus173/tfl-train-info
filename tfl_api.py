import requests
import json

api_url = "https://api.tfl.gov.uk"

class StopPoint:
	def __init__(self,mode=None,id=None,display_name=None):
		if display_name != None:
			self.id = self.get_id_from_display_name(display_name,mode=mode)[0]
		elif  id != None:
			self.id = id
		else:
			raise Exception("provide at least 1 of: id, display_name")
		self.display_name = self.get_display_name_from_id(self.id)
		self.modes = self.get_modes(self.id)
	def get_id_from_display_name(self,display_name,mode=None):
		display_name = display_name.replace(" ","%20")
		if mode != None:
			mode = mode.replace(" ","%20")
			mode_string = f"?modes={mode}"
		else:
			mode_string = ""
		response = requests.get(f"{api_url}/StopPoint/Search/{display_name}{mode_string}")
		response.raise_for_status()
		response = response.json()
		if response["total"] == 0:
			raise Exception("No matches found")
		return response["matches"][0]["id"], response["matches"][0]["name"]
	def get_display_name_from_id(self,id):
		response = requests.get(f"{api_url}/StopPoint/{id}")
		response.raise_for_status()
		response = response.json()
		return response["commonName"]
	def get_modes(self,id):
		response = requests.get(f"{api_url}/StopPoint/{id}")
		response.raise_for_status()
		response = response.json()
		modes = []
		for mode in response["lineModeGroups"]:
			modes.append(mode["modeName"])
		return modes
class Departures(StopPoint):
	def __init__(self,display_name=None,id=None,modes=None):
		super().__init__(display_name,id)
	def get_departures(self,modes=self.modes):
		pass
			
	
