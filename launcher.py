from engine.engine import GameEngine
from maps.maps_processor import RawMapsContainer

from argparse import (
    ArgumentParser,
    RawDescriptionHelpFormatter)


GAME_VERSION = "0"


if __name__ == '__main__':  # pragma: no cover

    parser = ArgumentParser(
        description='Videogame-platformer where squares fight for the win!',
        formatter_class=RawDescriptionHelpFormatter,
        epilog="controls:"
               "W, A, S, D to move, 'q' to exit")

    parser.add_argument(
        '--version',
        help="print program's current version number and exit",
        action='version',
        version=GAME_VERSION)

    args = parser.parse_args()

    # TODO: make GUI version of launcher. For now launcher just loads some map

    game_engine = GameEngine(RawMapsContainer.get_map_1())
    game_engine.start_game()
