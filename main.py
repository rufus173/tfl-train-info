import tfl_api
stop_point = tfl_api.Departures(id="910GCATFORD")#display_name="Catford")
print(stop_point.display_name)
print(stop_point.id)
print(stop_point.modes)

