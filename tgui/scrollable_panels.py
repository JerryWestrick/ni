from rich.panel import Panel
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Static, Button, Label, DataTable, Placeholder

programs = {
    "zoom.real":
        '''Program: zoom.real                                                                                         
Descrip:                                                                                                   
Link   :                                                                                                   
User   : jerry(1000:1000)                                                                                  
ESTABL : tcp 192.168.1.88(desktop):34542() --> 170.114.52.3():443(https)                                   
ESTABL : tcp 192.168.1.88(desktop):41706() --> 170.114.2.51(170-114-251.zoom.us):443(https)                
ESTABL : tcp 192.168.1.88(desktop):34540() --> 170.114.52.3():443(https)                                   
ESTABL : tcp 192.168.1.88(desktop):47184() --> 170.114.14.74(170-114-14-74.zoom.us):443(https)             
Checks:                                                                                                    
-FAIL- : No DEFINE for zoom.real''',
    "jetbrains-toolb":
        '''Program: jetbrains-toolb                                                                                   
Descrip:                                                                                                   
Link   :                                                                                                   
User   : jerry(1000:1000)                                                                                  
LISTEN : tcp ::ffff:127.0.0.1():52829() --> ::():0()                                                       
ESTABL : tcp ::ffff:127.0.0.1():40722() --> ::ffff:127.0.0.1():63342()                                     
Checks:                                                                                                    
-FAIL- : No DEFINE for jetbrains-toolb''',
    "whatsdesk":
        '''Program: whatsdesk                                                                                         
Descrip:                                                                                                   
Link   :                                                                                                   
User   : jerry(1000:1000)                                                                                  
ESTABL : tcp 192.168.1.88(desktop):36304() --> 157.240.14.52(whatsapp-cdn-shv-02-mia3.fbcdn.net):443(https)
Checks:                                                                                                    
-FAIL- : No DEFINE for whatsdesk''',
    "chrome":
        '''Program: chrome                                                                                            
Descrip: Google Chrome web browser                                                                         
Link   : https://www.google.com/chrome/                                                                    
User   : jerry(1000:1000)                                                                                  
ESTABL : tcp 192.168.1.88(desktop):51708() --> 74.125.26.188(uc-in-f188.1e100.net):5228(gcm-5228)          
Checks:                                                                                                    
-PASS- : NO_LISTEN:                                                                                        
-PASS- : NON_SYS_USER:''',
    "thunderbird":
        '''Program: thunderbird                                                                                       
Descrip:                                                                                                   
Link   :                                                                                                   
User   : jerry(1000:1000)                                                                                  
ESTABL : tcp 192.168.1.88(desktop):49692() --> 74.208.5.6(imap.perfora.net):993(imaps)                     
ESTABL : tcp 192.168.1.88(desktop):46494() --> 23.81.68.39():993(imaps)                                    
Checks:                                                                                                    
-FAIL- : No DEFINE for thunderbird'''
}


class NetworkInformationViewer(App):
    """A Textual app to manage stopwatches."""

    # CSS_PATH = "stopwatch.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit NetworkInformationViewer"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        panels = []
        for program, value in programs.items():
            panels.append(Static(Panel(value,
                                style="cornflower_blue on grey0",
                                title=program,
                                title_align="left")))
        yield ScrollableContainer(*panels)

    def action_quit(self) -> None:
        """An action to quit the program."""
        self.exit()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = NetworkInformationViewer()
    app.run()
