from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Footer, TextArea

from nanu.open_file_screen import OpenFileScreen


class NanuApp(App):
    BINDINGS = [
        ('ctrl+o', 'open_file', 'Open a file.'),
    ]

    CSS_PATH = 'tcss/nanu_app.tcss'


    def compose(self) -> ComposeResult:
        yield TextArea.code_editor()
        yield Footer()


    def _open_file(self, filepath: Path) -> None:
        self.notify(f'Opened: {filepath}')


    def action_open_file(self) -> None:
        def file_selected(filepath: Path | None) -> None:
            if filepath:
                self._open_file(filepath)

        self.push_screen(OpenFileScreen(), file_selected)
