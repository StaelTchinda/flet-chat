import argparse
from typing import Callable, Optional
import flet as ft

from src.message_app import MessageApp
from src.message import Message


def parse_args():
    parser = argparse.ArgumentParser("Message App")

    parser.add_argument("--answer_channel", type=str, help="Route to the answer channel",
                        default="scripts.answer.hello:answer_hello")


    return parser.parse_args()


def parse_answerer(answer_channel: str) -> Optional[Callable[[Message], Message]]:
    parts = answer_channel.split(":")
    module = __import__(parts[0], fromlist=[parts[1]])
    return getattr(module, parts[1])


def main():
    args = parse_args()
    answerer = parse_answerer(args.answer_channel)
    ft.app(lambda page: MessageApp(page, answerer))


if __name__ == "__main__":
    main()
