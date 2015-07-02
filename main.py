import cmd
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

class ShardUpdater(cmd.Cmd):
    def __init__(self):
        if platform.system() == constants.PLATFORM_WINDOWS:
            ctypes.windll.kernel32.SetConsoleTitleA(constants.TITLE)

        super(ShardUpdater, self).__init__()
        self._checkSettings()

    def _start(self):
        if threading.activeCount() is 2:
            print(constants.THREAD_RUNNING)
        else:
            print(constants.STARTING)
            self.thread = threading.Thread(target=follow.Follow,
                                           args=(self.directory,
                                           self.interval), daemon=True)
            self.thread.start()
            print(constants.THREAD_STARTED)

    def _checkSettings(self):
        def requestVariables():
            # Asks for variables to set in the settings.json file.
            directory = input('Toontown Directory: ')
            update = input('Update Interval (in seconds): ')
            writeVariables(directory, update)
            verifyIntegrity()

        def writeVariables(dir, interval):
            with open(constants.SETTINGS_FILE, 'w') as settings:
                config = {'directory': dir, 'interval': interval}
                json.dump(config, settings)

        def verifyExistance():
            if os.path.isfile(constants.SETTINGS_FILE):
                # This user already has a settings file. We don't need to bug them.
                verifyIntegrity()
            else:
                print(constants.NO_SETTINGS)
                requestVariables()

        def verifyIntegrity():
            # Verifies the variables set actually make sense.
            with open(constants.SETTINGS_FILE) as setting:
                settings = json.load(setting)
                if not os.path.isdir(settings['directory']):
                    # This isn't a directory. Notify the user.
                    print(constants.INVALID_DIRECTORY)
                    requestVariables()

                if not settings['interval'].isdigit():
                    print(constants.INVALID_INTERVAL)
                    requestVariables()

                # They've passed integrity checks. Bring them to the console!
                self.directory = settings['directory']
                self.interval = settings['interval']

                self.do_start(args='')

        verifyExistance()

    def do_clear(self, args):
        if platform.system() == constants.PLATFORM_WINDOWS:
            # Windows just had to use cls instead of clear.
            os.system('cls')
        else:
            os.system('clear')

    def do_exit(self, args):
        sys.exit(0)

    def do_start(self, args):
        self._start()

    """
    # TODO: Let's find a way to actually stop a thread!
    def do_stop(self, args):
        if threading.activeCount() is 2:
            self.thread.stop()
            self.thread.join()
            print(constants.THREAD_TERMINATED)
        else:
            print(constants.THREAD_NOT_RUNNING)
    """

    def do_status(self, args):
        if threading.activeCount() is 2:
            print(constants.THREAD_ONLINE)
        else:
            print(constants.THREAD_OFFLINE)

    def help_clear(self):
        print('Clears the command line of any text.')

    def help_exit(self):
        print('Exits the program.')

    def help_status(self):
        print('Returns the status of the shard updater thread.')

if __name__ == '__main__':
    console = ShardUpdater()
    console.prompt = '[console ~]# '
    console.cmdloop('Toontown Stream Shard Updater (%s)\n'
                    'Type "help" for more information.\n' % constants.VERSION)
