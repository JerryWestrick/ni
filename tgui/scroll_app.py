from textual.app import App
from textual.widgets import Placeholder


class ScrollApp(App):
    async def on_mount(self) -> None:
        # Create a placeholder for content, this could be any content widget
        placeholders = [Placeholder(f"Pane {i + 1}") for i in range(10)]

        # Dock the placeholders vertically
        for placeholder in placeholders:
            await self.view.dock(placeholder, edge="top")


ScrollApp.run(log="textual.log")
