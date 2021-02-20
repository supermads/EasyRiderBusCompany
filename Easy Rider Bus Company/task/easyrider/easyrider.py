import json
import re
from collections import Counter


def find_errors(bus_info):
    error_dict = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0
    }
    stop_type_options = ["S", "O", "F", ""]
    stop_name_pattern = re.compile(r"[A-Z][a-z]+\s?\w+?\s?(Road|Avenue|Boulevard|Street)$")
    a_time_pattern = re.compile(r"[0-2][0-9]:[0-5][0-9]$")

    for dict in bus_info:
        bus_id = dict["bus_id"]
        stop_id = dict["stop_id"]
        stop_name = dict["stop_name"]
        next_stop = dict["next_stop"]
        stop_type = dict["stop_type"]
        a_time = dict["a_time"]

        if not bus_id or type(bus_id) != int:
            error_dict["bus_id"] += 1

        if not stop_id or type(stop_id) != int:
            error_dict["stop_id"] += 1

        if not stop_name or not re.match(stop_name_pattern, stop_name):
            error_dict["stop_name"] += 1

        if (not next_stop and next_stop != 0) or type(next_stop) != int:
            error_dict["next_stop"] += 1

        if stop_type not in stop_type_options:
            error_dict["stop_type"] += 1

        if not a_time or not re.match(a_time_pattern, a_time):
            error_dict["a_time"] += 1

    total_errors = sum([error_dict['stop_name'], error_dict['stop_type'], error_dict['a_time']])
    print(f"Format validation: {total_errors} errors")
    print(f"stop_name: {error_dict['stop_name']}")
    print(f"stop_type: {error_dict['stop_type']}")
    print(f"a_time: {error_dict['a_time']}")


def get_line_info(bus_info):
    line_info = {}
    for dict in bus_info:
        bus_id = dict["bus_id"]
        if bus_id in line_info.keys():
            line_info[bus_id] += 1
        else:
            line_info[bus_id] = 1
    print("Line names and number of stops:")
    for key, value in line_info.items():
        print(f"bus_id: {key}, stops: {value}")


def verify_stops(bus_info):
    stops = {}
    for dict in bus_info:
        bus_id = dict["bus_id"]
        stop_type = dict["stop_type"]
        if bus_id in stops.keys():
            stops[bus_id].append(stop_type)
        else:
            stops[bus_id] = [stop_type]
    for line, stop in stops.items():
        if stop.count("S") != 1 or stop.count("F") != 1:
            print(f"There is no start or end stop for the line: {line}.")
            return False
    return True


def count_stops(bus_info):
    start_stops = set()
    finish_stops = set()
    transfer_stops = []
    line_stops = {}

    for dict in bus_info:
        bus_id = dict["bus_id"]
        stop_name = dict["stop_name"]
        stop_type = dict["stop_type"]

        if stop_type == "S":
            start_stops.add(stop_name)
        elif stop_type == "F":
            finish_stops.add(stop_name)

    # Find transfer stops (stops shared by at least 2 bus lines)
        if bus_id in line_stops.keys():
            line_stops[bus_id].add(stop_name)
        else:
            line_stops[bus_id] = {stop_name}
    all_stops = []
    for stop in line_stops.values():
        all_stops += stop
    stop_freq_dict = Counter(all_stops)
    for stop, freq in stop_freq_dict.items():
        if freq > 1:
            transfer_stops.append(stop)

    print(f"Start stops: {len(start_stops)} {sorted(list(start_stops))}")
    print(f"Transfer stops: {len(transfer_stops)} {sorted(transfer_stops)}")
    print(f"Finish stops: {len(finish_stops)} {sorted(list(finish_stops))}")


def check_arrival_times(bus_info):
    curr_line = 0
    curr_time = ""
    error_lines = []
    print("Arrival time test:")
    for dict in bus_info:
        bus_id = dict["bus_id"]
        a_time = dict["a_time"]
        stop_name = dict["stop_name"]
        if bus_id == curr_line and bus_id not in error_lines:
            if a_time < curr_time:
                print(f"bus_id line {bus_id}: wrong time on station {stop_name}")
                error_lines.append(bus_id)
            curr_time = a_time
        else:
            curr_line = bus_id
            curr_time = a_time
    if len(error_lines) == 0:
        print("OK")


def check_on_demand_stops(bus_info):
    start_stops = set()
    finish_stops = set()
    transfer_stops = []
    on_demand_stops = set()
    line_stops = {}
    error_stops = []

    print("On demand stops test:")

    for dict in bus_info:
        bus_id = dict["bus_id"]
        stop_name = dict["stop_name"]
        stop_type = dict["stop_type"]

        if stop_type == "S":
            start_stops.add(stop_name)
        elif stop_type == "F":
            finish_stops.add(stop_name)
        elif stop_type == "O":
            on_demand_stops.add(stop_name)

    # Find transfer stops (stops shared by at least 2 bus lines)
        if bus_id in line_stops.keys():
            line_stops[bus_id].add(stop_name)
        else:
            line_stops[bus_id] = {stop_name}
    all_stops = []
    for stop in line_stops.values():
        all_stops += stop
    stop_freq_dict = Counter(all_stops)
    for stop, freq in stop_freq_dict.items():
        if freq > 1:
            transfer_stops.append(stop)

    for stop in on_demand_stops:
        if stop in start_stops or stop in finish_stops or stop in transfer_stops:
            error_stops.append(stop)

    if error_stops:
        print(f"Wrong stop type: {sorted(error_stops)}")
    else:
        print("OK")


def main():
    bus_info = json.loads(input())
    check_on_demand_stops(bus_info)


main()
