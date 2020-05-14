from .command import Command, HELP, UNKNOWN, STATS, STATUS


class MessageParser:
    def __init__(self, command: str):
        self._command = command

    def parse(self, message):
        segments = message.content.split(" ")
        iterator = iter(segments)
        if not next(iterator) == "!{}".format(self._command):
            return None

        subcommand = next(iterator)

        if not subcommand or subcommand == "help":
            return Command(HELP)

        if subcommand == "channel":
            return Command(STATS, channel=message.channel)

        if subcommand == "global":
            return Command(STATS)

        if subcommand == "status":
            return Command(STATUS)

        return Command(UNKNOWN, subcommand)
