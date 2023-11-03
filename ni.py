import json

from compare_network_behavior import check_network_behavior




def format_output(results):
    # Define the box boundaries
    top_border = "┌" + "─" * 182 + "┐"
    bottom_border = "└" + "─" * 182 + "┘"

    formatted_lines = [top_border]

    for name, result in results.items():
        formatted_lines.append(f"│ Program: {result['Program']:<150}  │")
        # formatted_lines.append(descrip_line = f"│ Descrip: {result['Descrip']:<170} {result['Status']:<15} │")
        # formatted_lines.append(listen_line = f"│ Listen : {result['Listen']:<170} {result['Status']:<15} │")
        for con in result['Connections']:
            formatted_lines.append(f"│ Connect: {con['Connect']:<170} {con['Status']:<15} │")

        formatted_lines.append(bottom_border)

    return "\n".join(formatted_lines)


if __name__ == '__main__':

    # Compare the connections to the definitions
    comparison_results = check_network_behavior()

    # Format the results and print them out
    print(format_output(comparison_results))
