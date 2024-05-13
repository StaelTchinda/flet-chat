import flet as ft

from typing import Text


class Message():
    def __init__(self, user_name: Text, text: Text, message_type: Text):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

