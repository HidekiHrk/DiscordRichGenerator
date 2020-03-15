import asyncio
from app.config import Config
from app.mainWindow import MainWindow

loop = asyncio.new_event_loop()

config = Config()

mainw = MainWindow(
    title="Discord Rich Generator (By: HidekiHrk)",
    icon='./img/icon.png',
    appId=config['appId'])

def main():
    mainw.run()

main()


