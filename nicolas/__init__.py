# pylint: disable=missing-docstring
import asyncio
import pprint
import discord
from .helpers import is_emoji
from .history_crawler import HistoryCrawler
from .message_parser import MessageParser
from .response_builder import ResponseBuilder
from .response_generator import ResponseGenerator
from .store import ConcombreStore


class ConcombreNicolas(discord.Client):
    def __init__(self, emoji: str, channel: int = None):
        super().__init__()
        self._command_str = "concombres"
        self._store = ConcombreStore()
        self._emoji = emoji
        self._channel = channel
        self._message_parser = MessageParser(self._command_str)
        self._history_crawler = HistoryCrawler(listener=self)
        self._crawling = []
        self._response_builder = ResponseBuilder(
            self._command_str,
            generator=ResponseGenerator(),
            get_global_stats=self._store.get_global_stats,
            get_channel_stats=self._store.get_channel_stats,
            get_discord_emoji=self._get_discord_emoji,
            is_crawling=self.is_crawling,
            is_crawling_channel=self.is_crawling_channel,
        )
        self._users = {}
        print("Concombre Nicolas tracking emoji {}".format(self._emoji))

    async def on_ready(self):
        print("Logged in")
        self._store.reset()
        self._guild = self.guilds[0]
        self._discord_emoji = next(
            (x for x in self._guild.emojis if x.name == self._emoji), None
        )
        self._emoji_id = self._discord_emoji.id
        pprint.pprint(self._emoji_id)
        self._channels = [
            channel
            for channel in self.get_all_channels()
            if not self._ignore_channel(channel)
        ]
        self._history_crawler.crawl(self._channels)

    async def on_message(self, message):
        if self._ignore_channel(message.channel):
            return

        command = self._message_parser.parse(message)
        if command:
            response = self._response_builder.build_response(command)
            await message.channel.send(response)

    async def on_raw_reaction_add(self, payload):
        await self._handle_raw_reaction_action(payload, self._store.add_concombre)

    async def on_raw_reaction_remove(self, payload):
        await self._handle_raw_reaction_action(payload, self._store.remove_concombre)

    # Custom event handlers
    async def on_history_message(self, channel, message):
        pprint.pprint("History message : {}".format(message.content))
        for reaction in message.reactions:
            if is_emoji(self._emoji, reaction.emoji):
                users = await reaction.users().flatten()
                for reacting_user in users:
                    self._store.add_concombre(channel, message.author)

    def on_history_crawling_start(self, channel):
        self._crawling.append(channel.id)

    def on_crawling_end(self, channel):
        self._crawling.remove(channel.id)

    def is_crawling(self):
        return bool(self._crawling)

    def is_crawling_channel(self, channel):
        return channel.id in self._crawling

    def _get_discord_emoji(self):
        return self._discord_emoji

    def _ignore_channel(self, channel):
        return self._channel and self._channel != channel.id

    def _get_status(self):
        return {
            channel.name: self._history_crawler.is_crawling_channel(channel)
            for channel in self._channels
        }

    def ignore_emoji(self, emoji):
        return not is_emoji(self._emoji, emoji)

    def ignore_reaction_author(self, message, reaction_author):
        # Ignore if message author is reaction author
        return message.author.id == reaction_author.id

    async def _handle_raw_reaction_action(self, payload, store_callback):
        if self.ignore_emoji(payload.emoji):
            return

        channel = await self.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.fetch_user(payload.user_id)

        if self.ignore_reaction_author(message, user):
            pprint.pprint("Ignored emoji")
            return
        pprint.pprint(message.author.name)
        store_callback(channel, message.author)
        pprint.pprint(self._store.get_channel_stats(channel))
