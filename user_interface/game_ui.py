from tkinter import (
    Canvas,
    Tk as tk_Tk,
    mainloop as tk_mainloop,
    NSEW as TK_NSEW)
from threading import Event

from maps.maps_processor import GameMap
from engine.game_objects import PaintingConst, Player
from engine import ApplicationException


class GameGUI(Canvas):
    class GameObjectsPainter:
        """Accumulates all painting methods"""
        _rendering_map: GameMap
        _game_canvas: Canvas

        def __init__(self, input_gui: Canvas, input_map: GameMap):
            self._game_canvas = input_gui
            self._rendering_map = input_map

        def paint_all_game_objects(self):
            """Accumulates all painting"""
            self._game_canvas.delete('all')
            # WouldBeBetter: Paint interface objects

            self._paint_immovable_objects()

            self._paint_movable_objects()

        def _paint_immovable_objects(self):
            for immovable_object in self._rendering_map.immovable_objects:
                GameUIException(
                    "While processing [_paint_immovable_objects] method, "
                    "got [immovable_object] with unknown type: "
                    + immovable_object.__class__.__name__)

        def _paint_movable_objects(self):
            for movable_object in self._rendering_map.movable_objects:
                if isinstance(movable_object, Player):
                    self._paint_player(movable_object)
                else:
                    GameUIException(
                        "While processing [_paint_movable_objects] method, "
                        "got [movable_object] with unknown type: "
                        + movable_object.__class__.__name__)

        def _paint_player(self, player: Player):
            self._game_canvas.create_rectangle(
                player.current_position.x,
                player.current_position.y,
                player.current_position.x
                + PaintingConst.PLAYER_SIDE_LENGTH,
                player.current_position.y
                + PaintingConst.PLAYER_SIDE_LENGTH,
                fill='blue',
                outline='blue')

    _widgets_root: tk_Tk

    _gameObjectsPainter: GameObjectsPainter

    _render_is_done: Event

    def __init__(self):
        """Method for correct Canvas initialization with not None master"""
        self._widgets_root = tk_Tk()

        Canvas.__init__(self, self._widgets_root)

    def init(
            self,
            input_map: GameMap,
            input_engine_as_event_listener: 'EventListener'):
        self._gameObjectsPainter = self.GameObjectsPainter(self, input_map)

        self._render_is_done = Event()
        self._render_is_done.set()

        self._setup_appearance(input_map)
        self._setup_bindings(input_engine_as_event_listener)

        # Start constant checking for rendering necessity
        self.after(0, self._check_render)

    def _setup_appearance(self, input_map: GameMap):
        """Sets up appearance of game Canvas"""
        self._widgets_root.title('Squares battle')
        self._widgets_root.resizable(False, False)

        # WouldBeBetter recolor root's padding. This can be done with creating
        #  outer Frame that will serve as user_interface's colored borders with
        #  deletion root's padding at all

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

    def _setup_bindings(self, engine_as_event_listener: 'EventListener'):
        """Player's firing and moving bindings"""
        # TODO: Mouse bindings

        # EventListener bindings
        self._widgets_root.bind(
            '<KeyPress>',
            lambda event: engine_as_event_listener.key_pressed(event.keycode))
        self._widgets_root.bind(
            '<KeyRelease>',
            lambda event: engine_as_event_listener.key_released(event.keycode))

    def render(self):
        """Called by GameEngine when game field render is needed"""
        self._render_is_done.clear()
        self._render_is_done.wait()

    def _check_render(self):
        """Every 2 milliseconds checking if rendering is needed"""
        if not self._render_is_done.is_set():
            self._gameObjectsPainter.paint_all_game_objects()

            self._render_is_done.set()

        self.after(2, self._check_render)

    @staticmethod
    def run_gui_loop():
        tk_mainloop()


class EventListener:
    """Interface for circular imports problem resolving.

    It is impossible to have GameEngine import here and GUI import in
    'engine.py' at the same time so GameEngine have this interface.
    """
    def key_released(self, key_code: int):
        pass

    def key_pressed(self, key_code: int):
        pass


class GameUIException(ApplicationException):
    pass
