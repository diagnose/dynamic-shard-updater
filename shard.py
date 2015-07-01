import ctypes
import os
import platform
import textwrap
import threading
import time

from shard import constants


class ShardUpdater:
    def __init__(self):
        if platform.system() == constants.PLATFORM_WINDOWS:
            ctypes.windll.kernel32.SetConsoleTitleA(constants.TITLE)

        self.CheckSettings()

    def checkSettings(self):
        if os.path.isfile(constants.SETTINGS_FILE):
            # This user already has a settings file. We don't need to bug them.
            # TODO: Verify everything we need is actually in the settings file!
            self.RunScanner()
        else:
            print(constants.NO_SETTINGS)

    def invoker(self):
        pass

    def invokerParser(self, command):
        command = command.split(constants.COMMAND_SPACE)
        if command[0] == constants.COMMAND_HELP:
            print(constants.GENERAL_HELP)
            print(constants.COMMANDS)

    def runScanner(self):
        pass

ShardUpdater = ShardUpdater()
