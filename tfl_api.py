import requests
from datetime import datetime
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
		self.lines = self.get_lines(self.id)
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
	def get_lines(self,id):
		response = requests.get(f"{api_url}/StopPoint/{id}")
		response.raise_for_status()
		response = response.json()
		lines = []
		for line in response["lines"]:
			lines.append(line["id"])
		return lines
class Arrivals(StopPoint):
	def __init__(self,display_name=None,id=None,modes=None):
		super().__init__(display_name=display_name,id=id)
	def get_arrivals(self,modes=None,lines=None):
		if modes == None:
			modes = self.modes
		if lines == None:
			lines = self.lines
		arrivals = []
		response = requests.get(f"{api_url}/StopPoint/{self.id}/Arrivals")
		response.raise_for_status()
		for arrival in response.json():
			#print(json.dumps(arrival,indent=4))
			if arrival["lineId"] not in lines:
				continue
			if "destinationName" not in arrival:
				continue
			arrival_info = {
				"line_id": arrival["lineId"],
				"line_name": arrival["lineName"],
				"time_to_station": arrival["timeToStation"],
				"expected_arrival": datetime.fromisoformat(arrival["expectedArrival"][:-1]),
				"platform_name": arrival["platformName"],
				"destination_name": arrival["destinationName"],
			}
			arrivals.append(arrival_info)
		return arrivals
	def __iter__(self):
		self.cached_arrivals = self.get_arrivals()
		self.itter_index = -1
		return self
	def __next__(self):
		if self.itter_index > len(self.cached_arrivals):
			return StopItteration()
		self.itter_index += 1
		return self.cached_arrivals[itter_index]
			
	
