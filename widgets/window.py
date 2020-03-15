import asyncio
from tkinter import Frame, Tk, TclError

class Window(Frame):
    def __init__(self, name="", size:tuple = None, master=None):
        if name and master == None:
            master = Tk(className=name)
        Frame.__init__(self, master)
        if size != None:
            self.master.wm_maxsize(*size)
            self.master.wm_minsize(*size)
        self.pack()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run(loop))

    async def _run(self, loop):
        activated = True
        while activated:
            try:
                self.update()
                await asyncio.sleep(0.01)
            except TclError:
                activated = False
        loop.stop()
