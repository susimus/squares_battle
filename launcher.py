from argparse import ArgumentParser
from sys import version_info as sys_version_info, exit as sys_exit

from engine.engine import GameEngine
from maps.maps_processor import RawMapsContainer


GAME_VERSION = "1"


if __name__ == '__main__':  # pragma: no cover

    if (sys_version_info.major < 3
            or (sys_version_info.major == 3 and sys_version_info.minor < 7)):
        sys_exit('Python version 3.7 or upper is required')

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
