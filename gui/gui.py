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
        pass

    def key_pressed(self, key_code: int):
        pass

    def window_closed(self):
        pass


# TODO: Add here launcher GUI?
class GameGUI(Canvas):
    _widgets_root = tk_Tk()

    def __init__(self):
        """Method for correct Canvas initialization with not None master"""
        Canvas.__init__(self, self._widgets_root)

    def init(self, input_map: GameMap, input_engine_as_event_listener: EventListener):
        self._gameObjectsPainter = self.GameObjectsPainter(input_map, self)
        self._engine_as_event_listener = input_engine_as_event_listener

        self._setup_appearance(input_map)
        self._setup_mouse_and_keyboard_bindings()

    def _setup_appearance(self, input_map: GameMap):
        """Sets up appearance of game Canvas"""
        self._widgets_root.title('Squares battle')
        self._widgets_root.resizable(False, False)

        # WouldBeBetter recolor root's padding. This can be done with creating outer Frame
        #  that will serve as gui's colored borders with deletion root's padding at all

        self.configure(width=input_map.game_field_size.x)
        self.configure(height=input_map.game_field_size.y)
        self.configure(bg='deep sky blue')

        # Spawn game window at the screen center based on screen size
        screen_width = self._widgets_root.winfo_screenwidth()
        screen_height = self._widgets_root.winfo_screenheight()
        self._widgets_root.geometry(
            f'+{(screen_width // 2) - (int(self["width"]) // 2)}'
            # '- 20' because of title bar length  
            f'+{(screen_height // 2) - (int(self["height"]) // 2) - 20}')

        self.grid(sticky=TK_NSEW)

    _engine_as_event_listener: EventListener

    def _setup_mouse_and_keyboard_bindings(self):
        """Player's firing and moving bindings"""
        # TODO: Mouse bindings
        self._widgets_root.bind(
            '<KeyPress>',
            lambda event: self._engine_as_event_listener.key_pressed(event.keycode))
        self._widgets_root.bind(
            '<KeyRelease>',
            lambda event: self._engine_as_event_listener.key_released(event.keycode))

    def _setup_window_closing_binding(self):
        """Event on window closing"""
        # TODO
        pass

    def render(self):
        """Called by GameEngine when game field render is needed

        GameEngine DO NOT wait until method '_paint_all_game_objects' execution ends
        """
        self.after(0, self._paint_all_game_objects())

    @staticmethod
    def run_gui_loop():
        tk_mainloop()

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
