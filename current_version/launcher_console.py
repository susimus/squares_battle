from argparse import ArgumentParser, RawDescriptionHelpFormatter
from maps.maps_proc import RawMapsContainer
from engine.engine_main import GameEngine


CURRENT_VERSION = 0


if __name__ == '__main__':  # pragma: no cover
    parser = ArgumentParser(
        description='Videogame-platformer where squers fight for the win!',
        formatter_class=RawDescriptionHelpFormatter,
        epilog='''controls:
  Arrows to move, "q" to exit''')

    parser.add_argument(
        '--version',
        help="print program's current version number and exit",
        action='version',
        version=CURRENT_VERSION)

    args = parser.parse_args()

    game_engine = GameEngine(RawMapsContainer.get_map_1())
    game_engine.start_game()
