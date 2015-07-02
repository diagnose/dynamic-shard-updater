import ctypes
import json
import os
import platform
import sys
import textwrap
import threading
import time

from shard import constants


class ShardUpdater:
    def __init__(self):
        if platform.system() == constants.PLATFORM_WINDOWS:
            ctypes.windll.kernel32.SetConsoleTitleA(constants.TITLE)

        self.checkSettings()

    def checkSettings(self):
        def _requestVariables():
            # Asks for variables to set in the settings.json file.
            directory = input('Toontown Directory: ')
            if not os.path.isdir(directory):
                # This isn't a directory. Alert the user.
                print(constants.INVALID_DIRECTORY)
                _requestVariables()

            update = input('Update Interval (in seconds): ')
            if update.isdigit():
                # The user has entered a positive integer. Thank you!
                _writeVariables(directory, update)
            else:
                print(constants.INVALID_INTERVAL)
                _requestVariables()

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
                    # The directory specified in the settings file doesn't
                    # exist. Perhaps they've moved folders?
                    print(constants.INVALID_DIRECTORY)
                    _requestVariables()

                if not settings['interval'].isdigit():
                    print(constants.INVALID_INTERVAL)
                    _requestVariables()

                # They've passed integrity checks. Bring them to the console!
                self.invoker()

        _verifyExistance()

    def invoker(self):
        command = input('> ')
        self.invokerParser(command.lower())

    def invokerParser(self, command):
        command = command.split(constants.COMMAND_SPACE)
        if command[0] == constants.COMMAND_CLEAR:
            if platform.system() == constants.PLATFORM_WINDOWS:
                # Windows just had to use cls instead of clear.
                os.system('cls')
            else:
                os.system('clear')

        if command[0] == constants.COMMAND_HELP:
            print(constants.GENERAL_HELP)
            print(constants.COMMANDS)

        if command[0] == constants.COMMAND_EXIT:
            sys.exit(0)

        self.invoker()

    def runScanner(self):
        pass

ShardUpdater = ShardUpdater()
