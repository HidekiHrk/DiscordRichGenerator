import pypresence
from tkinter import *
from widgets.window import Window
from app.config import Config
from widgets.flatButton import FButton

class MainWindow(Window):
    def __init__(self, title="", appId=None, icon=None):
        super().__init__(name=title, size=(400,300))
        self.config = Config()
        self.master.title(title)
        if icon:
            self.master.iconphoto(True, PhotoImage(file=icon))
        self.definePresence(appId)

    def createWidgets(self):
        pass

    # Rich Presence Controllers #

    def updatePresence(self, **kw):
        try:
            self.presence.update(**kw)
            return True
        except pypresence.exceptions.ServerError:
            return False

    def updatePresenceState(self):
        keys = [
            "large_image", "small_image",
            "large_text", "small_text",
            "state", "details"
        ]
        presenceDict = dict()
        for k in keys:
            if self.config[k]:
                presenceDict[k] = self.config[k]
        return self.updatePresence(**presenceDict)

    def definePresence(self, appId=None):
        if not appId:
            self.presence = None
        else:
            self.presence = pypresence.Presence(
                client_id=appId
            )
            self.presence.connect()
            self.updatePresenceState()
