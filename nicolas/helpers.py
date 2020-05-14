def get_actual_emoji_str(emoji):
    if isinstance(emoji, str):
        return emoji
    return emoji.name


def is_emoji(compare_to: str, emoji):
    return get_actual_emoji_str(emoji) == compare_to
