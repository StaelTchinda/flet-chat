

from src.message import Message


def answer_hello(message: Message):
    return Message("World", f"Hello {message.user_name}", "chat_message")