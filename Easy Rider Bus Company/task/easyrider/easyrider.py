import json


def main():
    error_dict = {
        "bus_id": 0,
        "stop_id": 0,
        "stop_name": 0,
        "next_stop": 0,
        "stop_type": 0,
        "a_time": 0
    }

    bus_info = json.loads(input())

    for dict in bus_info:
        bus_id = dict["bus_id"]
        stop_id = dict["stop_id"]
        stop_name = dict["stop_name"]
        next_stop = dict["next_stop"]
        stop_type = dict["stop_type"]
        stop_type_options = ["S", "O", "F"]
        a_time = dict["a_time"]

        if not bus_id or type(bus_id) != int:
            error_dict["bus_id"] += 1

        if not stop_id or type(stop_id) != int:
            error_dict["stop_id"] += 1

        if not stop_name or type(stop_name) != str:
            error_dict["stop_name"] += 1

        if (not next_stop and next_stop != 0) or type(next_stop) != int:
            error_dict["next_stop"] += 1

        if stop_type not in stop_type_options and stop_type != "":
            error_dict["stop_type"] += 1

        if not a_time or type(a_time) != str:
            error_dict["a_time"] += 1

    total_errors = sum(list(error_dict.values()))
    print(f"Type and required field validation: {total_errors} errors")
    for key, value in error_dict.items():
        print(f"{key}: {value}")


main()
