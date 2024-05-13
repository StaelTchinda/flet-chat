from src.message import Message
from src.message_chat import MessageComponent


import flet as ft


from typing import Optional, Text


class MessageListComponent(ft.ListView):
    def __init__(self, main_user_name: Optional[Text] = None):
        super().__init__(
            expand=True,
            spacing=10,
            auto_scroll=True
        )

        self._main_user_name = main_user_name

    @property
    def main_user_name(self):
        return self._main_user_name

    @main_user_name.setter
    def main_user_name(self, value):
        self._main_user_name = value


    def add_message(self, message: Message):
        if message.message_type == "chat_message":
            if message.user_name == self.main_user_name:
                m = MessageComponent(message)
            else:
                m = MessageComponent(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12, text_align=ft.TextAlign.CENTER)
        self.controls.append(m)