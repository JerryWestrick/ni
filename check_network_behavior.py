import json



def extract_host_port(data):
    """Extracts host and port from a data string of format [host]:port."""
    if "]:" in data:  # Both host and port are provided
        host, port = data.split("]:")
        host = host[1:]  # Removing the starting [
    else:  # Only host is provided
        host = data[1:-1]  # Removing the starting [ and ending ]
        port = None
    return host, port


def check_network_behavior(network_behavior, network_info):
    results = {}

    # Helper function to handle LISTEN_ON check.
    def check_listen_on(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        ports = [conn['local_port'] for conn in program_info['connections'] if conn['state'] == 'LISTEN']
        if c_value in ports:
            result = "PASS"
        else:
            result = "FAIL"
        return [{"check": check_type, "result": result, "description": f'{c_type}:{c_value}'}]

    # Helper function to handle NO_LISTEN check.
    def check_no_listen(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        ports = [conn['local_port'] for conn in program_info['connections'] if conn['state'] == 'LISTEN']
        if not ports:
            result = "PASS"
        else:
            result = "FAIL"
        return [{"check": c_type, "result": result, "description": f'{c_type}:{c_value}'}]

    # Helper function to handle VALIDATE_CONN check.
    def check_validate_conn(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        results = []
        parts = c_value.split(";")
        local_data, remote_data = None, None
        for part in parts:
            if part.startswith('local'):
                local_data = part.split("=")[1]
            elif part.startswith('remote'):
                remote_data = part.split("=")[1]
        local_addresses, local_port = extract_host_port(local_data) if local_data else (None, None)
        remote_addresses, remote_port = extract_host_port(remote_data) if remote_data else (None, None)

        connections = [conn for conn in program_info['connections'] if
                       (not local_addresses or conn['local_address'] in local_addresses.split(",")) and
                       (not local_port or conn['local_port'] == local_port) and
                       (not remote_addresses or conn['remote_address'] in remote_addresses.split(",")) and
                       (not remote_port or conn['remote_port'] == remote_port)]
        if connections:
            results.append({"check": c_type, "result": "PASS", "description": f"{c_type}:{c_value}"})
        else:
            results.append({"check": c_type, "result": "FAIL", "description": f"{c_type}:{c_value}"})

        return results

    # Helper function to handle NON_SYS_USER check.
    def check_non_sys_user(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        result = "PASS" if int(program_info['uid']) > 999 else "FAIL"
        return [{"check": c_type, "result": result, "description": f'{c_type}:{c_value}'}]

    # Helper function to handle SYS_USER check.
    def check_sys_user(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        result = "PASS" if int(program_info['uid']) < 1000 else "FAIL"
        return [{"check": c_type, "result": result, "description": f'{c_type}:{c_value}'}]

    # Helper function to handle VALIDATE_USERNAME check.
    def check_validate_username(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        result = "PASS" if program_info['username'] == c_value else "FAIL"
        return [{"check": c_type, "result": result, "description": f'{c_type}:{c_value}'}]

    # Helper function to handle VALIDATE_UID check.
    def check_validate_uid(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        result = "PASS" if program_info['uid'] == c_value else "FAIL"
        return [{"check": c_type, "result": result, "description": f'{c_type}:{c_value}'}]

    # Helper function to handle Unknown check.
    def check_unknown(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        return [{"check": c_type, "result": "FAIL", "description": f'{c_type}:{c_value}'}]

    def check_define(program_info: dict[str, dict], c_type: str, c_value: str) -> list[dict]:
        return [{"check": c_type, "result": "FAIL", "description": f'No {c_type} for {program_info["program_name"]}'}]

    helper_dict: dict[str, any] = {
        'LISTEN_ON': check_listen_on,
        'NO_LISTEN': check_no_listen,
        'VALIDATE_CONN': check_validate_conn,
        'NON_SYS_USER': check_non_sys_user,
        'SYS_USER': check_sys_user,
        'VALIDATE_USERNAME': check_validate_username,
        'VALIDATE_UID': check_validate_uid,
        'DEFINE': check_define,
        'UNKNOWN': check_unknown
    }

    # Iterate over each program in network_info.
    for pgm_name, pgm_results in network_info.items():
        behavior = network_behavior.get(pgm_name, {"checks": ["DEFINE"], "description": "", "link": ""})
        pgm_results['description'] = behavior['description']
        pgm_results['link'] = behavior['link']
        checks = behavior['checks']
        pgm_checks = []

        for check in checks:
            # Split check into type and value.
            check_type, check_value = check.split(":", 1) if ":" in check else (check, "")

            # Using the helper_dict call the corresponding check_routine
            helper_rtn = helper_dict.get(check_type, "UNKNOWN")
            msgs = helper_rtn(pgm_results, check_type, check_value)
            pgm_checks.extend(msgs)

        pgm_results['checks'] = pgm_checks
        results[pgm_name] = pgm_results

    return results


if __name__ == '__main__':
    # Read the network_behavior file
    with open("network_behavior.json", "r") as file:
        network_behavior = json.load(file)

    # Read the network_info file
    with open("test_network_info.json", "r") as file:
        network_info = json.load(file)

    # Execute the check_network_behavior routine
    results = check_network_behavior(network_behavior, network_info)
    pretty = json.dumps(results, indent=4)
    print(pretty)
