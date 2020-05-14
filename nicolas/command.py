# pylint: disable=missing-docstring
HELP = "HELP"
STATUS = "STATUS"
STATS = "STATS"
UNKNOWN = "UNKNOWN"

COMMAND_NAMES = [HELP, STATS, STATUS, UNKNOWN]


class Command:
    def __init__(self, name: str, subcommand: str = None, channel=None):
        if not name in COMMAND_NAMES:
            raise Exception("Invalid command name")
        self._channel = channel
        self._name = name
        self._subcommand = subcommand

    @property
    def channel(self):
        return self._channel

    @property
    def name(self):
        return self._name

    @property
    def subcommand(self):
        return self._subcommand
