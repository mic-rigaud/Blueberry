# @Author: michael
# @Date:   02-Apr-2020
# @Filename: ArpWatchError.py
# @Last modified by:   michael
# @Last modified time: 02-Apr-2020
# @License: GNU GPL v3


class ArpWatchError(Exception):
    def __init__(self, value):
        self.value = value
        #super(ArpWatchError, self).__init__(value)

    def __str__(self):
        return repr(self.value)
