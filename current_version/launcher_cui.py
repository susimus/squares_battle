from argparse import ArgumentParser  #  pragma: no cover
from maps.maps_proc import RawMapsContainer  #  pragma: no cover
from engine.engine_main import GameEngine  #  pragma: no cover


CURRENT_VERSION = 0  #  pragma: no cover


if __name__ == '__main__':  #  pragma: no cover
    parser = ArgumentParser(
        description='Videogame-platformer where squers fight for the win!')
        
    parser.add_argument(
        '--version',
        help="print program's current version number and exit",
        action='version',
        version=CURRENT_VERSION)

    args = parser.parse_args()
    
    game_engine = GameEngine(RawMapsContainer.get_map_1())
    game_engine.start_game()