from maps.maps_processor import GameMap
from engine.game_objects import PaintingConst

from tkinter import (
    Canvas,
    Tk as tk_Tk,
    mainloop as tk_mainloop,
    NSEW as TK_NSEW)


class EventListener:
    """Interface for circular imports problem resolving.

    It is impossible to have GameEngine import here and GUI import in 'engine.py' at the
    same time so GameEngine have this interface.
    """
    def key_released(self, key_code: int):
        """GUI thread enters this method to subtract pressed key from 'keysPressed' set"""
        pass

    def key_pressed(self, key_code: int):
        """GUI thread enters this method to add pressed key to 'keysPressed' set"""
        pass

    def window_closed(self):
        """GUI thread enters this method to switch value of '_game_closed' variable"""
        pass


class GameGUI(Canvas):
    _widgets_root = tk_Tk()

    def __init__(self):
        """Method for correct Canvas initialization with not None master"""
        Canvas.__init__(self, self._widgets_root)

    def _setup_appearance(self, input_map: GameMap):
        """Sets up appearance of game Canvas"""
        self._widgets_root.title('Squares battle')

        self.grid(column=0, row=0, sticky=TK_NSEW)

        self['width'] = input_map.game_field_size.x
        self['height'] = input_map.game_field_size.y
        self._widgets_root.resizable(False, False)

        self['bg'] = 'white'

    _engine_as_event_listener: EventListener

    def _setup_mouse_and_keyboard_bindings(self):
        """Player's firing and moving bindings"""
        # TODO: Mouse bindings
        self._widgets_root.bind(
            '<1>',
            lambda event: print(123))
        # self._engine_as_event_listener.key_pressed(event.keycode))
        self.bind(
            '<KeyRelease>',
            lambda event: self._engine_as_event_listener.key_released(event.keycode))

    def _setup_closing_binding(self):
        """Event on window closing"""
        # TODO
        pass

    def init(self, input_map: GameMap, input_engine_as_event_listener: EventListener):
        self._gameObjectsPainter = self.GameObjectsPainter(input_map, self)
        self._engine_as_event_listener = input_engine_as_event_listener
        # TODO: For events firing add ttk_Frame that will be between root and Canvas
        self._setup_appearance(input_map)

    @staticmethod
    def run_gui_loop():
        tk_mainloop()

    def render(self):
        """Called by GameEngine when game field render is needed

        GameEngine DO NOT wait until method '_paint_all_game_objects' execution ends
        """
        self.after(0, self._paint_all_game_objects())

    class GameObjectsPainter:
        """Contains all painting methods"""
        _rendering_map: GameMap
        _gui: Canvas

        def __init__(self, input_map: GameMap, input_gui: Canvas):
            self._rendering_map = input_map
            self._gui = input_gui

        def paint_player(self):
            self._gui.create_rectangle(
                self._rendering_map.player.current_position.x,
                self._rendering_map.player.current_position.y,
                PaintingConst.PLAYER_SIDE_LENGTH,
                PaintingConst.PLAYER_SIDE_LENGTH,
                fill='blue')

    _gameObjectsPainter: GameObjectsPainter

    def _paint_all_game_objects(self):
        self.delete('all')

        self._gameObjectsPainter.paint_player()
