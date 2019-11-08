from argparse import ArgumentParser, Namespace
from typing import TextIO, Optional
from sys import exit as sys_exit

from engine import ApplicationException
from engine.engine import GameEngine
from maps import RawMapsContainer


def exit_with_exception(
        info_for_user: str,
        input_exception: ApplicationException,
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

        if readme_file.readline().rstrip() == '#### Версия':
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

    parser.add_argument(
        '-d', '--debug',
        help="turn on debug info printing",
        action='store_true')

    arguments: Namespace = parser.parse_args()

    # WouldBeBetter: make GUI version of launcher. For now launcher just loads
    #  some map

    map_name: str = input(
        'Enter map name. Raw maps names have format: "raw <name>".\n')

    game_engine: Optional[GameEngine] = None

    if map_name.startswith('raw '):
        try:
            game_engine = GameEngine(
                getattr(
                    RawMapsContainer,
                    'get_map_' + map_name.split(' ')[1])())
        except AttributeError:
            exit_with_exception(
                'Wrong raw map name',
                LauncherException('Wrong raw map name: ' + map_name),
                arguments.debug)

    # TODO: Finish custom maps loading from 'maps' folder

    if game_engine is None:
        pass

    game_engine.start_game()


class LauncherException(ApplicationException):
    pass
