import os
import pymongo

from flask import Flask
from router import BundleRouters
from flask_socketio import SocketIO
from mongoengine import connect
from dotenv import load_dotenv
from helpers.check_status_requests import check_status_requests, handle_requests
from services.chat import ChatService

# Load environment variables.

load_dotenv()

# Connection to database.

try:
    connect(db=os.getenv("DATABASE_NAME"), host=os.getenv("DATABASE_URL"))

    clientDB = pymongo.MongoClient(host=os.getenv("DATABASE_URL"))

    print("Connected to database!")
except Exception as e:
    print(f"Error: {e}")

# Init Flask app.

app = Flask(__name__, template_folder="templates", static_folder="assets")

# Enable bundle routers for Flask app.

bundleRouters = BundleRouters(app)
bundleRouters.enable()

# Init socket IO.

socketio = SocketIO(app)

# Run services.

chatService = ChatService(socketio)

connections = chatService.connections()

# Run helpers.

check_status_requests(chatService, connections)

handle_requests(clientDB, chatService, connections)

# Run Flask app.

if __name__ == "__main__":
    socketio.run(app, host=os.getenv("HOST"), port=os.getenv("PORT"), allow_unsafe_werkzeug=True)
