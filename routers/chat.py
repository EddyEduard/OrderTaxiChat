from flask import Blueprint
from controllers.chat import index, check_phone_number, send_message


def chat_routers():
    chat = Blueprint("chat", __name__)
    chat.route("/", methods=["GET"])(index)
    chat.route("/check_phone_number", methods=["GET"])(check_phone_number)
    chat.route("/send_message", methods=["POST"])(send_message)

    return chat
