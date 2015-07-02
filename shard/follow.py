import glob
import json
import os
import sys
import time

from shard import constants
from threading import Thread

class Follow(Thread):
    def __init__(self, directory, interval):
        self.directory = directory
        self.interval = int(interval)

        newest = max(glob.iglob(self.directory + '*.log'), key=os.path.getctime)
        self.logfile = open(newest)
        loglines = self.follow()

        for line in loglines:
            if constants.OTP_ENTERING_SHARD in line:
                shard_line = line.split(constants.COMMAND_SPACE)
                shard_list = json.loads(constants.SHARDS_FILE)
                shard_id = int(shard_line[-1].rstrip())
                print(shard_list)
                print(shard_id)
                print(shard_line)
                shard_name = shard_list[shard_id][constants.SHARD_NAME]

                print(constants.NEW_SHARD % (shard_id, shard_name))
                self.write(shard_id, shard_name)

    def follow(self):
        self.logfile.seek(0, 2)
        while True:
            line = self.logfile.readline()
            if not line:
                time.sleep(self.interval)
                continue
            yield line

    def write(self, shard, shard_name):
        with open(constants.DISTRICT_FILE, 'w') as district:
            if shard_name is None:
                district.write(constants.CURRENT_DISTRICT %
                               constants.DISTRICT_UNKNOWN)
            else:
                district.write(constants.CURRENT_DISTRICT % shard_name)

    def terminate(self):
        sys.exit(0)
