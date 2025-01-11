#!.venv/bin/python3
import tfl_api
from datetime import datetime
station_arrivals = tfl_api.Arrivals(id="490006767E")#display_name="forest hill rail station"
print(station_arrivals.display_name)
print(station_arrivals.id)
print(station_arrivals.modes)
print(station_arrivals.lines)
for arrival in station_arrivals.get_arrivals():
	print(f"{arrival['expected_arrival'].strftime('%H:%M')}\t{arrival['destination_name']} | {arrival['platform_name']} | {arrival['line_name']}")

