import pytest
from nicolas import ConcombreStore

from .utils import mock_user, mock_channel

existing_store_mock = {
    123456789: {111111111: 45, 222222222: 33, 333333333: 75},
    234567890: {111111111: 34, 222222222: 5},
    345678901: {111111111: 20, 333333333: 1},
}

existing_users = {111111111: "Kevin", 222222222: "Jennifer"}


def create_concombre_store(
    initial_store=None, initial_ban_list=None, initial_user_names=None
):
    return ConcombreStore(initial_store, initial_ban_list, initial_user_names)


def test_get_global_stats_default():
    store = create_concombre_store()
    assert store.get_global_stats() == {}


def test_get_global_stats():
    store = create_concombre_store(
        existing_store_mock, initial_user_names=existing_users
    )

    expected = {"Kevin": 99, "Anonymous": 76, "Jennifer": 38}

    actual = store.get_global_stats()

    assert actual == expected


def test_get_global_stats_with_banned_user():
    store = create_concombre_store(
        existing_store_mock, [111111111, 333333333], initial_user_names=existing_users
    )

    expected = {"Jennifer": 38}

    actual = store.get_global_stats()

    assert actual == expected


def test_get_channel_stats_default():
    channel = mock_channel(123456789)
    store = create_concombre_store()
    assert store.get_channel_stats(channel) == None


def test_get_channel_stats():
    channel = mock_channel(234567890)
    store = create_concombre_store(
        existing_store_mock, initial_user_names=existing_users
    )

    expected = {"Kevin": 34, "Jennifer": 5}

    actual = store.get_channel_stats(channel)

    assert actual == expected


def test_get_channel_stats_with_banned_users():
    channel = mock_channel(234567890)
    store = create_concombre_store(
        existing_store_mock, [222222222], initial_user_names=existing_users
    )

    expected = {"Kevin": 34}

    actual = store.get_channel_stats(channel)

    assert actual == expected


def test_add_concombre():
    channel = mock_channel(123456789)
    user = mock_user(111111111, "Kevin")
    store = create_concombre_store(existing_store_mock)

    expected = {
        123456789: {111111111: 46, 222222222: 33, 333333333: 75},
        234567890: {111111111: 34, 222222222: 5},
        345678901: {111111111: 20, 333333333: 1},
    }

    store.add_concombre(channel, user)
    actual = store.store

    assert actual == expected


def test_remove_concombre():
    channel = mock_channel(234567890)
    user = mock_user(222222222, "Jennifer")
    store = create_concombre_store(existing_store_mock)

    expected = {
        123456789: {111111111: 45, 222222222: 33, 333333333: 75},
        234567890: {111111111: 34, 222222222: 4},
        345678901: {111111111: 20, 333333333: 1},
    }

    store.remove_concombre(channel, user)
    actual = store.store

    assert actual == expected


def test_delete_channel():
    channel = mock_channel(234567890)
    store = create_concombre_store(existing_store_mock)

    expected = {
        123456789: {111111111: 45, 222222222: 33, 333333333: 75},
        345678901: {111111111: 20, 333333333: 1},
    }

    store.delete_channel(channel)
    actual = store.store

    assert actual == expected


def test_ban_user():
    user = mock_user(111111111, "Kevin")
    store = create_concombre_store()

    expected = [111111111]

    store.ban_user(user)
    actual = store.ban_list

    assert actual == expected


def test_unban_user():
    user = mock_user(111111111, "Kevin")
    store = create_concombre_store({}, [111111111])

    expected = []
    store.unban_user(user)

    actual = store.ban_list

    assert actual == expected
