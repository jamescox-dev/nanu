import os
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, ListItem, ListView, Static


class RootPathOption(ListItem):
    def __init__(self, root_path: Path, label: str) -> None:
        super().__init__(Static(f'{label}'))
        self.root_path = root_path


class OpenFileScreen(ModalScreen[Path]):
    BINDINGS = [
        ('escape', 'app.pop_screen', 'Cancel')
    ]

    CSS_PATH = 'tcss/open_file_screen.tcss'

    selected_file: reactive[Path | None] = reactive(None)

    def __init__(self) -> None:
        super().__init__()
        self.root_path_options = [
            RootPathOption(Path.cwd(), '\[ .  ] Current Directory'),
            RootPathOption(Path.home(), '\[ ~  ] Home Directory'),
        ]
        if os.name == 'nt':
            try:
                self.root_path_options += [RootPathOption(drive) for drive in os.listdrives()]
            except OSError:
                pass
        elif os.name == 'posix':
            self.root_path_options.append(RootPathOption(Path('/'), '\[ /  ] Root Directory'))


    def compose(self) -> ComposeResult:
        root_path_list = ListView(*self.root_path_options)
        dir_tree = DirectoryTree('./')
        container = Container(root_path_list, dir_tree, Horizontal(Button('Cancel', id='cancel'), Button('Open', id='open', disabled=True)))
        container.border_title = 'Open File'
        yield container


    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.query_one(DirectoryTree).path = event.item.root_path
        self.selected_file = None


    def watch_selected_file(self, selected_file: Path | None) -> None:
        self.query_one('#open').disabled = selected_file is None


    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        self.selected_file = None


    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        self.selected_file = event.path


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'open':
            self.dismiss(self.selected_file)
        else:
            self.dismiss()