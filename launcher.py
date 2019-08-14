from engine.engine import GameEngine
from maps.maps_processor import RawMapsContainer

from argparse import ArgumentParser


GAME_VERSION = "1"


if __name__ == '__main__':  # pragma: no cover

    parser = ArgumentParser(
        description='Videogame-platformer where squares fight for the win!')

    parser.add_argument(
        '--version',
        help="print program's current version number and exit",
        action='version',
        version=GAME_VERSION)

    args = parser.parse_args()

    # TODO: make GUI version of launcher. For now launcher just loads some map

    game_engine = GameEngine(RawMapsContainer.get_map_1())
    game_engine.start_game()
