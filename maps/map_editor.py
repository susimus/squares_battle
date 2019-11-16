from tkinter import (
    Tk as tk_Tk,
    Frame as tk_Frame,
    Button as tk_Button,
    Entry as tk_Entry,
    mainloop as tk_mainloop)
from sys import path as sys_path
from os.path import (
    join as os_path_join,
    dirname as os_path_dirname,
    abspath as os_path_abspath,
    pardir as os_pardir)
from pickle import dump as pickle_dump, load as pickle_load
from typing import Dict, Callable

try:
    from maps import GameMap, DEFAULT_RESOLUTION
except ModuleNotFoundError:
    sys_path.append(os_path_join(
        os_path_dirname(os_path_abspath(__file__)), os_pardir))

    from maps import GameMap, DEFAULT_RESOLUTION
finally:
    from engine import ApplicationException
    from engine.game_objects import *
    from engine.engine import EventListener
    from user_interface.game_ui import GameGUI


class MapEditor(tk_Frame):
    _game_map: GameMap
    _game_gui: GameGUI

    # Check what button is sunken to find out creation state. Always one and
    # only one creation button should be in pressed state
    #
    # Button name MUST be legit game object class. 'globals()[button_name]'
    # is used in mouse bindings methods
    _creation_button: Dict[str, tk_Button]
    _creation_game_objects: List[str]

    _save_filename_entry: tk_Entry
    _save_button: tk_Button

    _load_filename_entry: tk_Entry
    _load_button: tk_Button

    # [BasicPlatform] instance that is currently creating via sunken mouse
    # left button (button 1) in motion. In any other mouse state this var is
    # [None]
    _creating_basic_platform: Optional[BasicPlatform]

    def init(self):
        self._game_map = GameMap(
            Vector2D(*DEFAULT_RESOLUTION), [], [])
        self._creating_basic_platform = None

        self.grid(row=0, column=0)

        self._init_slave_widgets()

        self._init_mouse_bindings()

    def _init_slave_widgets(self):
        self._game_gui = GameGUI(
            input_widgets_root=self.master, master=self)
        self._game_gui.init(self._game_map, [EventListener()])
        self._game_gui.grid(row=0, column=0, rowspan=8)

        self._init_creation_buttons()

        self._init_saving_widgets()

        self._init_loading_widgets()

    def _init_creation_buttons(self):
        self._creation_button = dict()
        self._creation_game_objects = [
            'Player', 'BasicPlatform', 'SpeedUpBuff', 'JumpHeightUpBuff']

        for i in range(len(self._creation_game_objects)):
            self._creation_button[self._creation_game_objects[i]] = tk_Button(
                master=self, text=self._creation_game_objects[i])
            self._creation_button[self._creation_game_objects[i]].grid(
                row=i, column=1)
            self._creation_button[self._creation_game_objects[i]].configure(
                command=self._get_creation_button_command(
                    self._creation_game_objects[i]))

        self._creation_button['Player'].configure(relief='sunken')

    def _get_creation_button_command(self, sinking_button_name: str) -> (
            Callable[[], None]):
        def result_func():
            for button_name in self._creation_button:
                self._creation_button[button_name].configure(
                    relief='raised')

            self._creation_button[sinking_button_name].configure(
                relief='sunken')

        return result_func

    def _init_saving_widgets(self):
        self._save_filename_entry = tk_Entry(master=self)
        self._save_filename_entry.grid(row=4, column=1)

        self._save_button = tk_Button(master=self, text='Save')
        self._save_button.grid(row=5, column=1)
        self._save_button.configure(command=self._save_button_command)

    def _save_button_command(self):
        if self._save_filename_entry.get() != '':
            with open(self._save_filename_entry.get(), 'wb') as file_handle:
                pickle_dump(self._game_map, file_handle)

                self._game_map.remove_all_game_objects()

                self._game_gui.render()

    def _init_loading_widgets(self):
        self._load_filename_entry = tk_Entry(master=self)
        self._load_filename_entry.grid(row=6, column=1)

        self._load_button = tk_Button(master=self, text='Load')
        self._load_button.grid(row=7, column=1)
        self._load_button.configure(command=self._load_button_command)

    def _load_button_command(self):
        if self._load_filename_entry.get() != '':
            with open(self._load_filename_entry.get(), 'rb') as file_handle:
                self._game_map.set(pickle_load(file_handle))

                self._game_gui.render()

    def _init_mouse_bindings(self):
        self.master.bind('<Button-1>', self._create_game_object)
        self.master.bind('<B1-Motion>', self._change_basic_platform_size)
        self.master.bind(
            '<ButtonRelease-1>', self._finish_basic_platform_creation)

    def _create_game_object(self, event):
        """Adds new game object to current game map

        Invokes on left mouse button click
        """
        for button_name in self._creation_button:
            if (self._creation_button[button_name]['relief'] == 'sunken'
                    and event.widget.__class__.__name__ == 'GameGUI'):
                if button_name == 'Player':
                    if len(self._game_map.movable_objects) == 0:
                        self._game_map.movable_objects.append(
                            Player(Vector2D(event.x, event.y)))
                    else:
                        # If one [Player] instance already exists on map then
                        # it is forbidden to create another [Player]
                        # instance on the same map (game will crush
                        # otherwise). So here firstly created [Player]
                        # instance is moved to new location
                        self._game_map.movable_objects[0].location = (
                            Vector2D(event.x, event.y))

                elif button_name == 'BasicPlatform':
                    self._creating_basic_platform = (
                        BasicPlatform(0, 0, Vector2D(event.x, event.y)))

                    self._game_map.immovable_objects.append(
                        self._creating_basic_platform)

                else:
                    self._game_map.immovable_objects.append(
                        globals()[button_name](Vector2D(event.x, event.y)))

                self._game_gui.render()

    def _change_basic_platform_size(self, event):
        """Imitates basic platform stretching on its creation

        Invokes when left mouse button is held down and moved
        """
        if self._creating_basic_platform is not None:
            self._creating_basic_platform.width = (
                event.x
                - self._creating_basic_platform.location.x)

            self._creating_basic_platform.height = (
                event.y
                - self._creating_basic_platform.location.y)

            self._game_gui.render()

    def _finish_basic_platform_creation(self, _):
        if self._creating_basic_platform is not None:
            if self._creating_basic_platform.width < 0:
                self._creating_basic_platform.location.x += (
                    self._creating_basic_platform.width)

                self._creating_basic_platform.width *= -1

            if self._creating_basic_platform.height < 0:
                self._creating_basic_platform.location.y += (
                    self._creating_basic_platform.height)

                self._creating_basic_platform.height *= -1

            self._creating_basic_platform = None

    # Improvement: [_move_game_object] method
    def _move_game_object(self, event):
        """Draw chosen game object on cursor position

        Invokes every 10 millis
        """
        pass


class MapEditorException(ApplicationException):
    pass


if __name__ == '__main__':
    map_editor: MapEditor = MapEditor(master=tk_Tk())

    map_editor.init()

    tk_mainloop()
