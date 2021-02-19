import json
import re


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


def main():
    bus_info = json.loads(input())
    get_line_info(bus_info)


main()
