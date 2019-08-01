from os.path import (
    join as os_path_join,
    dirname as os_path_dirname,
    abspath as os_path_abspath)
from os import pardir as os_pardir
from sys import path as sys_path

# This code just appends parent directory to 'sys_path' of the file
sys_path.append(os_path_join(
    os_path_dirname(os_path_abspath(__file__)),
    os_pardir))
