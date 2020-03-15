import time
from tkinter import Frame, Tk, TclError, BOTH

class Window(Frame):
    def __init__(self, name="", size:tuple = None, master=None):
        if name and master == None:
            master = Tk(className=name)
        Frame.__init__(self, master)
        if size != None:
            self.master.wm_maxsize(*size)
            self.master.wm_minsize(*size)
        self.pack(fill=BOTH, expand=True)
        self.visible = True
        self.changed = False

    def setVisibility(self, value=True):
        self.changed = True
        self.visible = value

    def run(self):
        activated = True
        while activated:
            try:
                self.update()
                if self.changed:
                    self.changed = False
                    if self.visible:
                        self.master.deiconify()
                    else:
                        self.master.withdraw()
                time.sleep(0.01)
            except (TclError, KeyboardInterrupt):
                activated = False
