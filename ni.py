import json

from textual.app import ComposeResult, App
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Static, ListView, ListItem, Log

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


class NetworkInformationViewer(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "list_view.tcss"

    network_behavior = {}
    network_info = {}
    comparison_results = {}
    panel_info = []
    panel_txt = []
    last_highlighted = 0
    list_items = []

    def load_network_behavior(self):
        with open("network_behavior.json", "r") as file:
            self.network_behavior = json.load(file)

    def fetch_network_info(self):
        self.network_info = fetch_network_info()

    def compare(self):
        # Compare the connections to the definitions
        self.comparison_results = check_network_behavior(network_behavior=self.network_behavior,
                                                         network_info=self.network_info)

    def format_programs(self) -> None:
        for _, result in self.comparison_results.items():
            self.list_items.append(ListItem(Static(self.format_program(result))))
        return

    def format_program(self, result):
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

        self.panel_info.append(result)
        t = "\n".join(formatted_lines)
        self.panel_txt.append(t)
        return Panel(t,
                     style="cornflower_blue on grey0",
                     title=result['program_name'],
                     title_align="left")

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit NetworkInformationViewer"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield ListView(*self.list_items)
        # yield Log()

    def on_list_view_highlighted(self, message):
        # log = self.query_one(Log)
        idx = message.list_view.index
        if self.last_highlighted != idx:
            # log.write_line(
            #     f"UnHighlighted item no:{self.last_highlighted} or Program:{self.panel_info[self.last_highlighted]['program_name']} ")
            new_panel = Panel(self.panel_txt[self.last_highlighted],
                              style="cornflower_blue on grey0",
                              title=self.panel_info[self.last_highlighted]['program_name'],
                              title_align="left")
            self.list_items[self.last_highlighted].displayed_children[0].update(new_panel)

        self.last_highlighted = idx
        # log.write_line(f"Highlighted item no:{idx} or Program:{self.panel_info[idx]['program_name']} ")

        new_panel = Panel(self.panel_txt[idx],
                          style="yellow on grey0",
                          title=self.panel_info[idx]['program_name'],
                          title_align="left")
        self.list_items[idx].displayed_children[0].update(new_panel)

    def on_list_view_selected(self, message):
        # log = self.query_one(Log)
        idx = message.list_view.index
        # log.write_line(f"Selected item no:{idx} or Program:{self.panel_info[idx]['program_name']} ")

    def action_quit(self) -> None:
        """An action to quit the program."""
        self.exit()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == '__main__':
    app = NetworkInformationViewer()
    app.load_network_behavior()
    app.fetch_network_info()
    app.compare()
    app.format_programs()
    app.run()
