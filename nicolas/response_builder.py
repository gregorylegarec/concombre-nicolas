# pylint: disable=missing-docstring
import random
from .command import Command, STATS, STATUS, HELP, UNKNOWN

DEFAULT_STATS_LIMIT = 10
HELP_COMMANDS = ["help", "global", "channel", "status"]
EOL = "\n"
MEDALS = ["🥇", "🥈", "🥉"]


def add_stats_medals(lines: list):
    return [
        "{} {}".format(MEDALS[index], line) if index < len(MEDALS) else line
        for index, line in enumerate(lines)
    ]


def add_stats_ranks(lines: list):
    return ["{}. {}".format(index + 1, line) for index, line in enumerate(lines)]


class ResponseBuilder:
    def __init__(
        self,
        command: str,
        generator,
        get_global_stats,
        get_channel_stats,
        get_discord_emoji,
        is_crawling,
        is_crawling_channel,
    ):
        self._command_str = command
        self._generator = generator
        self._get_global_stats = get_global_stats
        self._get_channel_stats = get_channel_stats
        self._get_discord_emoji = get_discord_emoji
        self._is_crawling = is_crawling
        self._is_crawling_channel = is_crawling_channel

    def build_response(self, command: Command):
        response_methods = {
            HELP: "build_help",
            STATS: "build_stats",
            STATUS: "build_status",
            UNKNOWN: "build_unknown",
        }

        method_name = response_methods.get(command.name)
        if not method_name:
            return self.build_unknown(command)
        method = getattr(ResponseBuilder, method_name)
        return method(self, command)

    def build_help(self, command: Command):
        response_intro = random.choice(
            [
                "L'utilisation de `!{}` est très simple :",
                "Attention ça va aller très vite :",
                "Amusez-vous :",
            ]
        )

        commands = {
            "help": "Affiche les commandes disponibles (c'est moi)",
            "status": "Affiche l'état de Concombre Nicolas",
            "global": "Affiche le classement global",
            "channel": "Affiche le classement du channel",
        }

        command_list = [
            "`!{} {}` : {}".format(self._command_str, command, commands.get(command))
            for command in commands
        ]

        return response_intro.format(self._command_str) + EOL + EOL.join(command_list)

    def build_stats(self, command: Command):
        is_channel = bool(command.channel)
        if is_channel:
            if self._is_crawling_channel(command.channel):
                return self._generator.generate("computing.channel").format(
                    command.channel.name
                )
            stats = self._get_channel_stats(command.channel)
            intro = self._generator.generate("stats.channel.intro").format(
                command.channel.name
            )
        else:
            if self._is_crawling():
                return self._generator.generate("computing.global")
            stats = self._get_global_stats()
            intro = self._generator.generate("stats.global.intro")

        return intro + EOL + self._build_stats_ranking(stats)

    def _build_stats_ranking(self, stats):
        emoji = self._get_discord_emoji()

        lines = []
        for name in sorted(stats, key=stats.get, reverse=True)[:DEFAULT_STATS_LIMIT]:
            lines += [
                "**{}** : {} <:{}:{}>".format(name, stats[name], emoji.name, emoji.id)
            ]

        lines_with_medals = add_stats_medals(lines)
        ranked_lines = add_stats_ranks(lines_with_medals)

        return EOL.join(ranked_lines)

    def build_status(self, command: Command):
        return "Commande pas encore implémentée et oui guess what mon développeur a une vie."

    def build_unknown(self, command: Command):
        help_command = "`!{} help`".format(self._command_str)
        response_intro = self._generator.generate("unknown.intro")
        response_help_command = self._generator.generate("unknown.help")
        return (
            response_intro.format(command.subcommand)
            + EOL
            + response_help_command.format(help_command)
        )
