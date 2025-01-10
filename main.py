import tfl_api
from datetime import datetime
station_arrivals = tfl_api.Arrivals(display_name="blackfriars underground")
#print(station_arrivals.display_name)
#print(station_arrivals.id)
#print(station_arrivals.modes)
#print(station_arrivals.lines)
for arrival in station_arrivals.get_arrivals(lines=["district"]):
	print(f"{arrival['expected_arrival'].strftime('%H:%M')}\t{arrival['destination_name']} | {arrival['platform_name']} | {arrival['line_name']}")

