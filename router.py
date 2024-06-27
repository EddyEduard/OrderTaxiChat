from routers.chat import chat_routers

class BundleRouters:
    def __init__(self, app):
        self.chat = chat_routers()
        self.app = app

    def enable(self):
        self.app.register_blueprint(self.chat, url_prefix="/")
