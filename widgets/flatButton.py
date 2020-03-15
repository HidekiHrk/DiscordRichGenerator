from app.constants import *
from tkinter import Button, FLAT


class FButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self['relief'] = FLAT
        self['fg'] = '#ddd'
        self['bg'] = foreground
        self['font'] = font
        self['cursor'] = 'hand1'
        self['highlightbackground'] = foreground
        self['activebackground'] = h_foreground
        self['activeforeground'] = '#ddd'
        self['pady'] = 0
