from sys import version_info as sys_version_info, exit as sys_exit

try:
    from user_interface.launcher_ui import run_launcher_logic
finally:
    if sys_version_info[:3] < (3, 7, 4):
        print('Python version 3.7.4 or greater is required')
        sys_exit('Python version error: ' + str(sys_version_info))

if __name__ == '__main__':
    run_launcher_logic()
