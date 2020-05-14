# pylint: disable=missing-docstring
import copy


def aggregate_channel(channel_dict, initial_stats=None, ban_list=None):
    if initial_stats is None:
        initial_stats = {}
    if ban_list is None:
        ban_list = []
    stats = initial_stats.copy()
    for user_id in channel_dict:
        if user_id in ban_list:
            continue
        initial_score = initial_stats.get(user_id, 0)
        score = channel_dict[user_id]
        stats[user_id] = initial_score + score
    return stats


def ensure_channel(store, channel):
    if not channel.id in store:
        store[channel.id] = {}


def ensure_user(store, channel, user):
    ensure_channel(store, channel)
    if not user.id in store[channel.id]:
        store[channel.id][user.id] = 0


def sort_stats(stats):
    return {name: stats[name] for name in sorted(stats, key=stats.get, reverse=True)}


class ConcombreStore:
    @property
    def store(self):
        return self._store

    @property
    def ban_list(self):
        return self._ban_list

    def __init__(
        self,
        initial_store: dict = None,
        initial_ban_list: list = None,
        initial_user_names: dict = None,
    ):
        self._user_names = (
            {} if initial_user_names is None else copy.deepcopy(initial_user_names)
        )
        self._store = {} if initial_store is None else copy.deepcopy(initial_store)
        self._ban_list = (
            [] if initial_ban_list is None else copy.deepcopy(initial_ban_list)
        )

    def reset(self):
        self._user_names = {}
        self._store = {}
        self._ban_list = []

    def add_concombre(self, channel, user):
        ensure_user(self._store, channel, user)
        self.store_user_name(user)
        self._store[channel.id][user.id] += 1

    def remove_concombre(self, channel, user):
        # Let's count even negative value, all should be balanced in the end.
        ensure_user(self._store, channel, user)
        self.store_user_name(user)
        self._store[channel.id][user.id] -= 1

    def store_user_name(self, user):
        self._user_names[user.id] = user.display_name

    def get_global_stats(self):
        stats = {}
        for channel_id in self._store:
            stats = aggregate_channel(self._store[channel_id], stats, self._ban_list)
        return self._unanonymize_stats(stats)

    def get_channel_stats(self, channel):
        if not channel.id in self._store:
            return None
        return self._unanonymize_stats(
            aggregate_channel(self._store[channel.id], None, self._ban_list)
        )

    def _unanonymize_stats(self, stats):
        return {self._user_names.get(id, "Anonymous"): stats[id] for id in stats}

    def delete_channel(self, channel):
        if channel.id in self._store:
            del self._store[channel.id]

    def ban_user(self, user):
        if not user.id in self._ban_list:
            self._ban_list.append(user.id)

    def unban_user(self, user):
        if user.id in self._ban_list:
            self._ban_list.remove(user.id)
