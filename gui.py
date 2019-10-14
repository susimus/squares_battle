from argparse import ArgumentParser
from typing import TextIO
from sys import exit as sys_exit

from engine.engine import GameEngine
from maps.maps_processor import RawMapsContainer


def exit_with_exception(
        info_for_user: str,
        input_exception: Exception,
        debugging_mode: bool):
    """Exits with exception

    Prints info to stdout for user and to stderr for debugging. Instead of
    error codes, 'error strings' are used. 'Error strings' have format:
    '\n' + (exception name) + ': ' + (exception args)
    """
    print(info_for_user)

    if debugging_mode:
        sys_exit(
            "\n"
            + input_exception.__class__.__name__
            + ": "
            + str(input_exception))
    else:
        sys_exit(0)


def get_current_version() -> str:
    """Gives current version str

    Gives version based on 3 and 5 lines of 'README.md' in application's
    folder. If data cannot be read then "Cannot read 'README.md' file" str
    returns
    """
    readme_file: TextIO
    version_info: str

    try:
        readme_file = open('README.md', 'r', encoding="utf8")

        for _ in range(4):
            readme_file.readline()

        if readme_file.readline() == '#### Версия\n':
            readme_file.readline()

            return readme_file.readline().rstrip()

    except OSError:
        pass

    return "Cannot read 'README.md' file"


def run_launcher_logic():
    parser = ArgumentParser(
        description='Videogame-platformer where squares fight for the win!')

    parser.add_argument(
        '--version',
        help="print program's current version number and exit",
        action='version',
        version=get_current_version())

    parser.parse_args()

    # TODO: make GUI version of launcher. For now launcher just loads some map
    game_engine = GameEngine(RawMapsContainer.get_map_1())
    game_engine.start_game()
