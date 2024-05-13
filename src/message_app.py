import flet as ft

from src.message_chat import MessageChat
from src.message import Message


class MessageApp():
    def __init__(self, page: ft.Page):
        self.page = page

        self.page.horizontal_alignment = "stretch"
        self.page.title = "Flet Chat"
        
        # A dialog asking for a user display name
        self.join_user_name = ft.TextField(
            label="Enter your name to join the chat",
            autofocus=True,
            on_submit=self.join_chat_click,
        )
        self.page.dialog = ft.AlertDialog(
            open=True,
            modal=True,
            title=ft.Text("Welcome!"),
            content=ft.Column([self.join_user_name], width=300, height=70, tight=True),
            actions=[ft.ElevatedButton(text="Join chat", on_click=self.join_chat_click)],
            actions_alignment="end",
        )

        # Chat messages
        self.chat = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
        )

        # A new message entry form
        self.new_message = ft.TextField(
            hint_text="Write a message...",
            autofocus=True,
            shift_enter=True,
            min_lines=1,
            max_lines=5,
            filled=True,
            expand=True,
            on_submit=self.send_message_click,
        )

        # Add everything to the page
        self.page.add(
            ft.Container(
                content=self.chat,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                [
                    self.new_message,
                    ft.IconButton(
                        icon=ft.icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=self.send_message_click,
                    ),
                ]
            ),
        )

        self.page.pubsub.subscribe(self.on_message)


    def join_chat_click(self, e):
        if not self.join_user_name.value:
            self.join_user_name.error_text = "Name cannot be blank!"
            self.join_user_name.update()
        else:
            self.page.session.set("user_name", self.join_user_name.value)
            self.page.dialog.open = False
            self.new_message.prefix = ft.Text(f"{self.join_user_name.value}: ")
            self.page.pubsub.send_all(Message(user_name=self.join_user_name.value, text=f"{self.join_user_name.value} has joined the chat.", message_type="login_message"))
            self.page.update()

    def send_message_click(self, e):
        if self.new_message.value != "":
            self.page.pubsub.send_all(Message(self.page.session.get("user_name"), self.new_message.value, message_type="chat_message"))
            self.new_message.value = ""
            self.new_message.focus()
            self.page.update()

    def on_message(self, message: Message):
        if message.message_type == "chat_message":
            m = MessageChat(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        self.chat.controls.append(m)
        self.page.update()

