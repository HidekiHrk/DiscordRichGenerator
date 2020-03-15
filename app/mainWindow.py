import pypresence
import asyncio
from pypresence.exceptions import InvalidID, ServerError
from bindglobal import BindGlobal
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from app.constants import *
from widgets.window import Window
from app.config import Config
from widgets.flatButton import FButton
import os

class MainWindow(Window):
    def __init__(self, title="", appId=None, icon=None):
        super().__init__(name=title, size=(400,330))
        self.config = Config()
        self.master.title(title)
        if icon:
            self.master.iconphoto(True, PhotoImage(file=icon))
        self.master.protocol('WM_DELETE_WINDOW', self.on_closing)

        # Frames #
        self['bg'] = background_dark
        self.header = Frame(self, bg=background_darker, pady=5)
        self.middle = Frame(self, bg=background_dark, pady=5)
        self.footer = Frame(self, bg=background_dark)
        self.header.pack(fill=BOTH)
        self.middle.pack(fill=BOTH)
        self.footer.pack()
        self.createWidgets()
        self.bg = BindGlobal(widget=self.master.master)
        self.bg.gbind('<Control_R-r>', self.re_open)
        # self.definePresence(appId)

    def re_open(self, event):
        self.setVisibility(True)

    # Close Event #
    def on_closing(self):
        question = messagebox.askyesnocancel("Quit", 'Want to quit? (RCtrl+R to re-open)')
        if question:
            self.closeRunningLoop()
            self.master.destroy()
            os._exit(0)
        elif question == False:
            self.setVisibility(False)

    def createWidgets(self):
        # ------ Title ------ #
        self.titleLabel = Label(self.header,
                                text='Discord Rich Generator',
                                font=font, fg=foreground, bg=background_darker)
        self.titleLabel.grid(row=0, column=1)

        # ------ Logo ------ #
        img = Image.open(icon).resize((30, 30), Image.BICUBIC)
        logo = ImageTk.PhotoImage(img)
        self.logo = Label(self.header,
                          image=logo,
                          bg=background_darker)
        self.logo.image = logo
        self.logo.grid(row=0, column=0, padx=(90, 0))

        # ------ Inputs ------ #
        self.inputs = {}
        fields = ["appId", "large_image", "small_image",
            "large_text", "small_text",
            "state", "details"]
        for f in range(len(fields)):
            field = fields[f]
            flabel = Label(self.middle, text=f"{field}: ", fg=foreground, font=font, bg=background_dark)
            flabel.grid(row=f, column=0, padx=(30, 0))
            fentry = Entry(self.middle,
                           fg='#aaa', font=font,
                           bg='#131E25', relief=FLAT, highlightthickness=0,
                           insertbackground='#aaa')
            fentry.insert(0, self.config[field])
            fentry.grid(row=f, column=1, pady=1)
            fentry.bind('<Control-KeyRelease-a>', self.selectAll)
            self.inputs[field] = fentry

        # Buttons #
        # Update:
        self.updateButton = FButton(self.footer, text="Update", command=self.updatePresenceEvent)
        self.updateButton.pack(side=LEFT, padx=(0,2))
        # Save:
        self.saveButton = FButton(self.footer, text="Save", command=self.save)
        self.saveButton.pack(side=LEFT, padx=(2,2))
        # Load:
        self.loadButton = FButton(self.footer, text="Load", command=self.load)
        self.loadButton.pack(side=LEFT, padx=(2,0))

    # Button Events #

    def selectAll(self, event):
        event.widget.icursor('end')
        event.widget.select_range(0, 'end')

    def save(self):
        for k, v in self.inputs.items():
            self.config[k] = v.get()
        self.config.save()

    def load(self):
        self.config.refresh()
        for k, v in self.inputs.items():
            v.delete(0, 'end')
            v.insert(0, self.config[k])

    @property
    def updateObject(self):
        obj = {}
        for k, v in self.inputs.items():
            obj[k] = v.get()
        return obj

    def updatePresenceEvent(self):
        for k, v in self.inputs.items():
            self.config[k] = v.get()
        try:
            self.updatePresenceState()
        except AttributeError:
            messagebox.showerror('Error', 'Some field values are wrong.')

    # Rich Presence Controllers #

    def updatePresence(self, **kw):
        if (getattr(self, 'presence', None) == None or
        self.config['appId'] != self.presence.client_id):
            self.definePresence()
        try:
            self.presence.update(**kw)
            return True
        except (ServerError, InvalidID):
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

    def closeRunningLoop(self):
        try:
            rloop = asyncio.get_running_loop()
            rloop.stop()
        except RuntimeError:
            pass

    def definePresence(self, appId=None):
        if not appId:
            appId = self.config['appId']
        self.closeRunningLoop()
        self.presence = None
        self.presence = pypresence.Presence(
            client_id=appId,
            loop=asyncio.new_event_loop()
        )
        self.presence.connect()
        if not self.updatePresenceState():
            self.closeRunningLoop()
            self.presence = None
