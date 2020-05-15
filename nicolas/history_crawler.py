# pylint: disable=missing-docstring
import asyncio

HISTORY_SLICE_SIZE = 20
DEFAULT_MAX_RETRIES = 10


# pylint: disable=too-few-public-methods
class ChannelHistoryCrawler:
    def __init__(self, channel, listener=None):
        self._channel = channel
        self._listener = listener

    async def crawl(self):
        self._listener.on_history_crawling_start(self._channel)
        try:
            last_message = await self._channel.fetch_message(
                self._channel.last_message_id
            )

            history_slice = await self._fetch_history_slice(
                last_message, DEFAULT_MAX_RETRIES
            )

            while history_slice:
                for message in history_slice:
                    await self._listener.on_history_message(self._channel, message)
                last_message = history_slice[-1]
                history_slice = await self._fetch_history_slice(
                    last_message, DEFAULT_MAX_RETRIES
                )
        finally:
            self._listener.on_crawling_end(self._channel)

    async def _fetch_history_slice(self, last_message, tries_left: int):
        try:
            history = self._channel.history(
                limit=HISTORY_SLICE_SIZE, before=last_message
            )
            return await history.flatten()
        except Exception as e:
            if tries_left == 0:
                raise e
            return self._fetch_history_slice(last_message, tries_left - 1)


class HistoryCrawler:
    def __init__(self, listener=None):
        self._listener = listener

    def crawl(self, channels: list):
        for channel in channels:
            self.crawl_channel(channel)

    def crawl_channel(self, channel):
        channel_history_crawler = ChannelHistoryCrawler(
            channel, listener=self._listener
        )
        asyncio.ensure_future(channel_history_crawler.crawl())
