import json

from check_network_behavior import check_network_behavior
from fetch_network_info import fetch_network_info

from rich import print
from rich.console import Group
from rich.panel import Panel

color_text = 'green'
color_connection = 'green'


def format_connection(con: dict) -> str:
    return (f"{con['state'][:6]} :[{color_connection}] {con['protocol']} "
            f"{con['local_address']}({con['local_host']}):{con['local_port']}({con['local_service']})"
            f" --> "
            f"{con['remote_address']}({con['remote_host']}):{con['remote_port']}({con['remote_service']})"
            f"[/{color_connection}]"
            )


def format_output(results):
    pannels = []
    for name, result in results.items():
        formatted_lines = [f"Program: [{color_text}]{result['program_name']}[/{color_text}]",
                           f"Descrip: [{color_text}]{result['description']}[/{color_text}]",
                           f"Link   : [{color_text}]{result['link']}[/{color_text}]",
                           f"User   : [{color_text}]{result['username']}({result['uid']}:{result['gid']})[/{color_text}]"]
        for con in result['connections']:
            formatted_lines.append(format_connection(con))
        formatted_lines.append("[bold underline]Checks:[/bold underline]")
        for chk in result['checks']:
            my_color = color_text if chk['result'] == "PASS" else "red1"
            formatted_lines.append(f"[bold {my_color}]-{chk['result']}- : {chk['description']}[/bold {my_color}]")

        pannels.append(Panel("\n".join(formatted_lines),
                             style="cornflower_blue on grey0",
                             title=result['program_name'],
                             title_align="left"))
    return pannels


if __name__ == '__main__':
    # Get Network Behavior
    with open("network_behavior.json", "r") as file:
        network_behavior = json.load(file)

    # Get
    network_info = fetch_network_info()

    # Compare the connections to the definitions
    comparison_results = check_network_behavior(network_behavior=network_behavior, network_info=network_info)

    # Format the results and print them out
    for p in format_output(comparison_results):
        print(p)
