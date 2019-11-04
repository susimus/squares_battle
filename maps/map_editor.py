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


# TODO: Implement [MapEditor]
class MapEditor(tk_Frame):
    _current_game_map: GameMap

    _game_gui: GameGUI

    # Check what button is sunken to find out creation state. Always one and
    # only one creation button should be in pressed state
    _basic_platform_button: tk_Button
    _speed_up_buff_button: tk_Button
    _jump_height_up_buff_button: tk_Button

    _save_filename_entry: tk_Entry
    _save_button: tk_Button

    _load_filename_entry: tk_Entry
    _load_button: tk_Button

    # TODO: Implement [init]
    def init(self):
        self.grid(row=0, column=0)

        self._current_game_map = GameMap(
            Vector2D(*DEFAULT_RESOLUTION), [], [])

        self._init_slave_widgets()

    def _init_slave_widgets(self):
        self._game_gui = GameGUI(
            input_widgets_root=self.master, master=self)
        self._game_gui.init(self._current_game_map, EventListener())
        self._game_gui.grid(row=0, column=0, rowspan=7)

        self._init_creation_buttons()

        self._init_saving_widgets()

        self._init_loading_widgets()

    def _init_creation_buttons(self):
        self._basic_platform_button = tk_Button(
            master=self, text='BasicPlatform')
        self._basic_platform_button.grid(row=0, column=1)
        self._basic_platform_button.configure(
            relief='sunken',
            command=self._basic_platform_button_command)

        self._speed_up_buff_button = tk_Button(
            master=self, text='SpeedUpBuff')
        self._speed_up_buff_button.grid(row=1, column=1)
        self._speed_up_buff_button.configure(
            command=self._speed_up_buff_button_command)

        self._jump_height_up_buff_button = tk_Button(
            master=self, text='JumpHeightUpBuff')
        self._jump_height_up_buff_button.grid(row=2, column=1)
        self._jump_height_up_buff_button.configure(
            command=self._jump_height_up_buff_button_command)

    def _basic_platform_button_command(self):
        if self._basic_platform_button['relief'] != 'sunken':
            self._basic_platform_button.configure(relief='sunken')

            if self._speed_up_buff_button['relief'] == 'sunken':
                self._speed_up_buff_button.configure(relief='raised')

            if self._jump_height_up_buff_button['relief'] == 'sunken':
                self._jump_height_up_buff_button.configure(relief='raised')

    def _speed_up_buff_button_command(self):
        if self._speed_up_buff_button['relief'] != 'sunken':
            self._speed_up_buff_button.configure(relief='sunken')

            if self._basic_platform_button['relief'] == 'sunken':
                self._basic_platform_button.configure(relief='raised')

            if self._jump_height_up_buff_button['relief'] == 'sunken':
                self._jump_height_up_buff_button.configure(relief='raised')

    def _jump_height_up_buff_button_command(self):
        if self._jump_height_up_buff_button['relief'] != 'sunken':
            self._jump_height_up_buff_button.configure(relief='sunken')

            if self._speed_up_buff_button['relief'] == 'sunken':
                self._speed_up_buff_button.configure(relief='raised')

            if self._basic_platform_button['relief'] == 'sunken':
                self._basic_platform_button.configure(relief='raised')

    def _init_saving_widgets(self):
        self._save_filename_entry = tk_Entry(master=self)
        self._save_filename_entry.grid(row=3, column=1)

        self._save_button = tk_Button(master=self, text='Save')
        self._save_button.grid(row=4, column=1)
        self._save_button.configure(command=self._save_button_command)

    def _save_button_command(self):
        if self._save_filename_entry.get() != '':
            with open(self._save_filename_entry.get(), 'wb') as file_handle:
                pickle_dump(self._current_game_map, file_handle)

                self._current_game_map.remove_all_game_objects()

                self._game_gui.render()

    def _init_loading_widgets(self):
        self._load_filename_entry = tk_Entry(master=self)
        self._load_filename_entry.grid(row=5, column=1)

        self._load_button = tk_Button(master=self, text='Load')
        self._load_button.grid(row=6, column=1)
        self._load_button.configure(command=self._load_button_command)

    def _load_button_command(self):
        if self._load_filename_entry.get() != '':
            with open(self._load_filename_entry.get(), 'rb') as file_handle:
                self._current_game_map.set(pickle_load(file_handle))

                self._game_gui.render()


class MapEditorException(ApplicationException):
    pass


if __name__ == '__main__':
    map_editor: MapEditor = MapEditor(master=tk_Tk())

    map_editor.init()

    tk_mainloop()
