#!/usr/bin/env python3
import argparse
from nicolas import ConcombreNicolas


def parse_args():
    parser = argparse.ArgumentParser(
        description="Lance Concombre Nicolas le compteur de comcombres."
    )
    parser.add_argument("token", metavar="TOKEN", type=str, help="Token discord")
    parser.add_argument(
        "--emoji",
        dest="emoji",
        type=str,
        help="Emoji to track",
        default="pickle_rick_5332",
    )
    parser.add_argument(
        "--channel", dest="channel", type=int, help="Track only the given channel ID"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    nicolas = ConcombreNicolas(emoji=args.emoji, channel=args.channel)
    nicolas.run(args.token)


if __name__ == "__main__":
    main()
