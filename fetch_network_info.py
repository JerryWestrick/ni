# Define the new module

import json
import subprocess
import socket


# This query is taken from the original netinfo.py file.
# It fetches details about processes and their associated network details.
query = ''' 
SELECT 
    p.pid,
    p.name AS program_name,
    p.uid,
    p.gid,
    u.username,
    os.local_address,
    os.local_port,
    s.name AS local_service,
    os.remote_address,
    os.remote_port,
    sr.name AS remote_service,
    os.state,
    CASE os.protocol
        WHEN 1 THEN 'icmp'
        WHEN 6 THEN 'tcp'
        WHEN 17 THEN 'udp'
        ELSE 'unknown'
    END AS protocol
FROM processes p
JOIN process_open_sockets os ON p.pid = os.pid
LEFT JOIN users u ON p.uid = u.uid
LEFT JOIN etc_services s ON os.local_port = s.port AND (CASE os.protocol WHEN 6 THEN 'tcp' WHEN 17 THEN 'udp' ELSE 'unknown' END) = s.protocol
LEFT JOIN etc_services sr ON os.remote_port = sr.port AND (CASE os.protocol WHEN 6 THEN 'tcp' WHEN 17 THEN 'udp' ELSE 'unknown' END) = sr.protocol
WHERE os.state = 'ESTABLISHED' OR os.state = 'LISTEN'
'''


def get_hostname_from_ip(ip):
    if '127.0.0.1' in ip:
        return ""

    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, OSError):
        return ""


program_items = ["gid", "program_name", "uid", "username"]
connection_items = ["local_address", "local_port", "local_service", "protocol",
                    "remote_address", "remote_port", "remote_service", "state"]


def gather_programs(connection_list):
    last_program_name = ""
    program = None
    programs = {}


    for con in connection_list:
        if last_program_name != con["program_name"]:
            # We got a program Break!
            # Save last program
            if program is not None:
                programs[program['program_name']] = program
            # start new program
            program = {'connections': []}
            for k in program_items:
                program[k] = con[k]
            last_program_name = program['program_name']

        # Here we save this connection
        c = {}
        for k in connection_items:
            c[k] = con[k]
        # resolve hostnames

        c['local_host'] = get_hostname_from_ip(c['local_address'])
        c['remote_host'] = get_hostname_from_ip(c['remote_address'])

        program['connections'].append(c)

    return programs


def fetch_network_info():
    """
    Fetches the current network information using osquery.
    """
    cmd = ['osqueryi', '--json', query]
    connection_string = subprocess.check_output(cmd)
    connection_list = json.loads(connection_string)
    # The result is a list of connections sorted by program name
    # You now need to make program  containing a list of connections out of that...
    programs = gather_programs(connection_list)

    return programs


if __name__ == '__main__':
    info = fetch_network_info()
    # for pgm in info.items():
    #     pretty = json.dumps(pgm, indent=4)
    #     print(pretty)
    pretty = json.dumps(info, indent=4)
    print(pretty)
