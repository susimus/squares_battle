from tkinter import (
    Canvas,
    Tk as tk_Tk,
    mainloop as tk_mainloop,
    NSEW as TK_NSEW)
from threading import Event

from maps import GameMap
from engine.game_objects import *
from engine import ApplicationException
from user_interface import EventListener


class GameGUI(Canvas):
    class GameObjectsDrawer:
        """Accumulates all painting methods"""
        _rendering_map: GameMap
        # Improvement: Create second canvas for double buffering
        _game_canvas: Canvas

        def __init__(self, input_gui: Canvas, input_map: GameMap):
            self._game_canvas = input_gui
            self._rendering_map = input_map

        def draw_all_game_objects(self):
            """Accumulates all painting"""
            self._game_canvas.delete('all')
            # Improvement: Paint interface objects

            self._draw_immovable_objects()

            self._draw_movable_objects()

        def _draw_immovable_objects(self):
            for immovable_object in self._rendering_map.immovable_objects:
                if isinstance(immovable_object, SpeedUpBuff):
                    self._draw_speed_up_buff(immovable_object)

                elif isinstance(immovable_object, JumpHeightUpBuff):
                    self._draw_jump_height_up_buff(immovable_object)

                elif isinstance(immovable_object, BasicPlatform):
                    self._draw_basic_platform(immovable_object)

                else:
                    GameUIException(
                        "While processing [_paint_immovable_objects] method, "
                        "got [immovable_object] with unknown type: "
                        + immovable_object.__class__.__name__)

        def _draw_speed_up_buff(self, speed_buff: SpeedUpBuff):
            if not speed_buff.is_charging():
                self._game_canvas.create_rectangle(
                    speed_buff.location.x,
                    speed_buff.location.y,
                    speed_buff.location.x + AbstractBuff.SIDE_LENGTH,
                    speed_buff.location.y + AbstractBuff.SIDE_LENGTH,
                    fill='green',
                    outline='green')

        def _draw_jump_height_up_buff(self, jump_buff: JumpHeightUpBuff):
            if not jump_buff.is_charging():
                self._game_canvas.create_rectangle(
                    jump_buff.location.x,
                    jump_buff.location.y,
                    jump_buff.location.x + AbstractBuff.SIDE_LENGTH,
                    jump_buff.location.y + AbstractBuff.SIDE_LENGTH,
                    fill='yellow',
                    outline='yellow')

        def _draw_basic_platform(self, basic_platform: BasicPlatform):
            self._game_canvas.create_rectangle(
                basic_platform.location.x,
                basic_platform.location.y,
                basic_platform.location.x
                + basic_platform.width,
                basic_platform.location.y
                + basic_platform.height,
                fill='brown',
                outline='brown')

        def _draw_movable_objects(self):
            for movable_object in self._rendering_map.movable_objects:
                if isinstance(movable_object, Player):
                    self._draw_player(movable_object)

                elif isinstance(movable_object, HandgunProjectile):
                    self._draw_handgun_projectile(movable_object)

                elif isinstance(movable_object, MachineGunProjectile):
                    self._draw_machine_gun_projectile(movable_object)

                else:
                    GameUIException(
                        "While processing [_paint_movable_objects] method, "
                        "got [movable_object] with unknown type: "
                        + movable_object.__class__.__name__)

        def _draw_player(self, player: Player):
            self._game_canvas.create_rectangle(
                player.location.x,
                player.location.y,
                player.location.x
                + Player.SIDE_LENGTH,
                player.location.y
                + Player.SIDE_LENGTH,
                fill='blue',
                outline='blue')

        def _draw_handgun_projectile(self, projectile: HandgunProjectile):
            self._game_canvas.create_oval(
                projectile.location.x,
                projectile.location.y,
                projectile.location.x
                + HandgunProjectile.CIRCLE_DIAMETER,
                projectile.location.y
                + HandgunProjectile.CIRCLE_DIAMETER,
                fill='white',
                outline='white')

        def _draw_machine_gun_projectile(
                self, projectile: MachineGunProjectile):
            self._game_canvas.create_oval(
                projectile.location.x,
                projectile.location.y,
                projectile.location.x
                + MachineGunProjectile.CIRCLE_DIAMETER,
                projectile.location.y
                + MachineGunProjectile.CIRCLE_DIAMETER,
                fill='white',
                outline='white')

    _widgets_root: tk_Tk

    _game_objects_painter: GameObjectsDrawer

    _render_is_done: Event

    def __init__(
            self, input_widgets_root: Optional[tk_Tk] = None, *args, **kwargs):
        """Method for correct Canvas initialization with not None master"""
        if input_widgets_root is None:
            self._widgets_root = tk_Tk()

            Canvas.__init__(self, master=self._widgets_root)
        else:
            self._widgets_root = input_widgets_root

            Canvas.__init__(self, *args, **kwargs)

    def init(
            self,
            input_map: GameMap,
            input_event_listeners: List['EventListener']):
        self._game_objects_painter = self.GameObjectsDrawer(self, input_map)

        self._render_is_done = Event()
        self._render_is_done.set()

        self._init_appearance(input_map)
        self._init_bindings(input_event_listeners)

        # Start constant checking for rendering necessity
        if self.master.__class__.__name__ != 'MapEditor':
            self.after(0, self._check_render)

    # Improvement: Sync this init with [MapEditor] init
    def _init_appearance(self, input_map: GameMap):
        """Sets up appearance of game Canvas"""
        self._widgets_root.title('Squares battle')
        self._widgets_root.resizable(False, False)

        # Improvement recolor root's padding. This can be done with creating
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

    def _init_bindings(self, input_event_listeners: List['EventListener']):
        """Player's firing and moving bindings"""
        def notify_listeners_about_lmb_event(event):
            for event_listener in input_event_listeners:
                event_listener.lmb_event_happened(event)

        def notify_listeners_about_key_pressed(event):
            for event_listener in input_event_listeners:
                event_listener.key_pressed(event.keycode)

        def notify_listeners_about_key_released(event):
            for event_listener in input_event_listeners:
                event_listener.key_released(event.keycode)

        # Mouse bindings
        self._widgets_root.bind(
            '<Button-1>', notify_listeners_about_lmb_event)
        self._widgets_root.bind(
            '<ButtonRelease-1>', notify_listeners_about_lmb_event)
        self._widgets_root.bind(
            '<B1-Motion>', notify_listeners_about_lmb_event)

        # EventListener bindings
        self._widgets_root.bind(
            '<KeyPress>', notify_listeners_about_key_pressed)
        self._widgets_root.bind(
            '<KeyRelease>', notify_listeners_about_key_released)

    def render(self):
        """Called by GameEngine when game field render is needed"""
        if self.master.__class__.__name__ != 'MapEditor':
            self._render_is_done.clear()
            self._render_is_done.wait()
        else:
            self._game_objects_painter.draw_all_game_objects()

    def _check_render(self):
        """Every 2 milliseconds checking if rendering is needed"""
        if not self._render_is_done.is_set():
            self._game_objects_painter.draw_all_game_objects()

            self._render_is_done.set()

        self.after(2, self._check_render)

    @staticmethod
    def run_gui_loop():
        tk_mainloop()


class GameUIException(ApplicationException):
    pass
