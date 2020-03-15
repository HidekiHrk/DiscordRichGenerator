import asyncio
from app.constants import *
from app.config import Config
from app.mainWindow import MainWindow

loop = asyncio.new_event_loop()

config = Config()

def defaultConfig():
    fields = ["appId", "large_image", "small_image",
            "large_text", "small_text",
            "state", "details"]
    for f in fields:
        if not config[f]:
            config[f] = ""
    config.save()

def main():
    defaultConfig()
    mainw = MainWindow(
        title=app_title,
        icon=icon)

    mainw.run()
main()



