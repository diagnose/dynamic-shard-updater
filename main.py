import cmd
import ctypes
import json
import os
import platform
import requests
import sys
import threading
import time
import webbrowser

from shard import constants
from shard import follow

class ShardUpdater(cmd.Cmd):
    def __init__(self):
        if platform.system() == constants.PLATFORM_WINDOWS:
            ctypes.windll.kernel32.SetConsoleTitleA(constants.TITLE)

        cmd.Cmd.__init__(self)
        self._checkSettings()

    def _start(self):
        if threading.activeCount() is 2:
            print(constants.THREAD_RUNNING)
        else:
            self.thread = threading.Thread(target=follow.Follow,
                                           args=(self.directory, self.interval))
            self.thread.daemon = True
            self.thread.start()
            print(constants.THREAD_STARTED)

    def _checkSettings(self):
        def requestVariables():
            # Asks for variables to set in the settings.json file.
            directory = raw_input('Toontown Directory: ')
            update = raw_input('Update Interval (in seconds): ')
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

                self._checkUpdates()
                self._start()

        verifyExistance()

    def _checkUpdates(self):
        latest = requests.get(constants.VERSION_URL, verify=False).text
        if latest == constants.VERSION:
            # We have the latest version. Nothing to do here.
            pass
        else:
            print(constants.OUTDATED_VERSION % (constants.VERSION, latest))

    def do_clear(self, args):
        if platform.system() == constants.PLATFORM_WINDOWS:
            # Windows just had to use cls instead of clear.
            os.system('cls')
        else:
            os.system('clear')

    def do_exit(self, args):
        try:
            # We're going to try and remove the text files, since they're ugly.
            os.remove(constants.DISTRICT_FILE)
            os.remove(constants.DISTRICT_NAME_FILE)
        except WindowsError:
            # These files don't exist. Odd.
            pass

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

    def do_update(self, args):
        if args == 'check':
            self._checkUpdates()
        elif args == 'download':
            webbrowser.open(constants.GITHUB_URL)
        else:
            print(constants.INVALID_ARGUMENT)

    def help_clear(self):
        print('Clears the command line of any text.')

    def help_exit(self):
        print('Exits the program.')

    def help_status(self):
        print('Returns the status of the shard updater thread.')

    def help_update(self):
        print('Allows the user to check for the latest version available.')

if __name__ == '__main__':
    console = ShardUpdater()
    console.prompt = '[console ~]# '
    console.cmdloop('Toontown Stream Shard Updater (%s)\n'
                    'Type "help" for more information.\n' % constants.VERSION)
