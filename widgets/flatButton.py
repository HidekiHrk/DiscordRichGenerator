from tkinter import Button, FLAT

class FButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self['relief'] = FLAT
        self['fg'] = '#99ffbb'
        self['bg'] = '#333'
        self['font'] = ('BalooChettan2', '14')