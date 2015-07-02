import ctypes
import json
import os
import platform
import sys
import textwrap
import threading
import time

from shard import constants
from shard import follow

class ShardUpdater:
    def __init__(self):
        if platform.system() == constants.PLATFORM_WINDOWS:
            ctypes.windll.kernel32.SetConsoleTitleA(constants.TITLE)

        self.checkSettings()

    def checkSettings(self):
        def _requestVariables():
            # Asks for variables to set in the settings.json file.
            directory = input('Toontown Directory: ')
            update = input('Update Interval (in seconds): ')
            _writeVariables(directory, update)
            _verifyIntegrity()

        def _writeVariables(dir, interval):
            with open(constants.SETTINGS_FILE, 'w') as settings:
                config = {'directory': dir, 'interval': interval}
                json.dump(config, settings)

        def _verifyExistance():
            if os.path.isfile(constants.SETTINGS_FILE):
                # This user already has a settings file. We don't need to bug them.
                # TODO: Verify everything we need is actually in the settings file!
                _verifyIntegrity()
            else:
                print(constants.NO_SETTINGS)
                _requestVariables()

        def _verifyIntegrity():
            # Verifies the variables set actually make sense.
            with open(constants.SETTINGS_FILE) as setting:
                settings = json.load(setting)
                if not os.path.isdir(settings['directory']):
                    # This isn't a directory. Notify the user.
                    print(constants.INVALID_DIRECTORY)
                    _requestVariables()

                if not settings['interval'].isdigit():
                    print(constants.INVALID_INTERVAL)
                    _requestVariables()

                # They've passed integrity checks. Bring them to the console!
                self.directory = settings['directory']
                self.interval = settings['interval']

                self.thread = threading.Thread(target=follow.Follow,
                                               args=(self.directory,
                                               self.interval), daemon=True)
                self.thread.start()

                self.invoker()

        _verifyExistance()

    def invoker(self):
        command = input('$ ')
        self.invokerParser(command)

    def invokerParser(self, command):
        command = command.split(constants.COMMAND_SPACE)
        if command[0] == constants.COMMAND_CLEAR:
            if platform.system() == constants.PLATFORM_WINDOWS:
                # Windows just had to use cls instead of clear.
                os.system('cls')
            else:
                os.system('clear')

        elif command[0] == constants.COMMAND_HELP:
            print(constants.GENERAL_HELP)
            print(constants.COMMANDS)

        elif command[0] == constants.COMMAND_EXIT:
            sys.exit(0)

        elif command[0] == constants.COMMAND_START:
            if threading.activeCount() is not 1:
                print(constants.THREAD_RUNNING)
            else:
                self.thread.start()

        elif command[0] == constants.COMMAND_STATUS:
            if threading.activeCount() is not 1:
                print(constants.THREAD_ONLINE)
            else:
                print(constants.THREAD_OFFLINE)

        elif command[0] == constants.COMMAND_STOP:
            follow.Follow.terminate()
            print(constants.THREAD_TERMINATED)

        else:
            print(constants.INVALID_COMMAND % command[0])

        self.invoker()


ShardUpdater = ShardUpdater()
