from argparse import (
    ArgumentParser,
    RawDescriptionHelpFormatter)
from configparser import ConfigParser
# from engine.engine_main import GameEngine
# from maps.maps_proc import RawMapsContainer


if __name__ == '__main__':  # pragma: no cover
    STARTUP_DATA = ConfigParser()
    STARTUP_DATA.read('startup_data.ini')

    parser = ArgumentParser(
        description='Videogame-platformer where squares fight for the win!',
        formatter_class=RawDescriptionHelpFormatter,
        epilog="controls:"
               "Arrows to move, 'q' to exit")

    parser.add_argument(
        '--version',
        help="print program's current version number and exit",
        action='version',
        version=STARTUP_DATA['Common']['VERSION'])

    args = parser.parse_args()

    # game_engine = GameEngine(RawMapsContainer.get_map_1())
    # game_engine.start_game()
