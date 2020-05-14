import pytest
from nicolas import ResponseBuilder
from nicolas.command import Command, STATS
from .utils import mock_channel


class EmojiMock:
    def __init__(self):
        self.id = 1234
        self.name = "test"


class ResponseGeneratorMock:
    def generate(self, key):
        return key


def get_global_stats_mock():
    return {"Kevin": 12, "Bob": 4, "Jennifer": 5}


def get_channel_stats_mock(channel):
    return {"Bob": 3, "Jennifer": 1}


def always_true(*args):
    return True


def always_false(*args):
    return False


def get_discord_emoji_mock():
    return EmojiMock()


def create_response_builder(
    is_crawling_mock=always_false, is_crawling_channel_mock=always_false
):
    return ResponseBuilder(
        "test",
        generator=ResponseGeneratorMock(),
        get_global_stats=get_global_stats_mock,
        get_channel_stats=get_channel_stats_mock,
        get_discord_emoji=get_discord_emoji_mock,
        is_crawling=is_crawling_mock,
        is_crawling_channel=is_crawling_channel_mock,
    )


def test_build_global_stats():
    response_builder = create_response_builder()
    command = Command(STATS)

    expected = (
        "stats.global.intro\n"
        "1. 🥇 **Kevin** : 12 <:test:1234>\n"
        "2. 🥈 **Jennifer** : 5 <:test:1234>\n"
        "3. 🥉 **Bob** : 4 <:test:1234>"
    )

    actual = response_builder.build_stats(command)

    assert actual == expected


def test_build_channel_stats():
    response_builder = create_response_builder()
    command = Command(STATS, channel=mock_channel(id=123456789))

    expected = (
        "stats.channel.intro\n"
        "1. 🥇 **Bob** : 3 <:test:1234>\n"
        "2. 🥈 **Jennifer** : 1 <:test:1234>"
    )

    actual = response_builder.build_stats(command)

    assert actual == expected


def test_build_global_stats_when_crawling():
    response_builder = create_response_builder(is_crawling_mock=always_true)
    command = Command(STATS)

    expected = "computing.global"

    actual = response_builder.build_stats(command)

    assert actual == expected


def test_build_channel_stats():
    response_builder = create_response_builder(is_crawling_channel_mock=always_true)
    command = Command(STATS, channel=mock_channel(id=123456789))

    expected = "computing.channel"

    actual = response_builder.build_stats(command)

    assert actual == expected
