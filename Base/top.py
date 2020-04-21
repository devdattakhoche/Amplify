import tkinter as tk
from .topLeft import TopLeft
from .topRight import TopRight
from Pages.HomePage.Home import Home
from Pages.Browse.browse import Browse
from Pages.MusicPage.main import Main
from .listOfPage import *


class Top(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self['background'] = 'yellow'

        self.topleft = TopLeft(self)
        self.topRight = TopRight(self)
        # --------------------------------------------------------------------------
        # Loading all the frames

        self.frames = {}
        for F in (Home, Browse):
            frame = F(self.topRight.topRightBottom, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        # Displaying the frame
        self.show_frame(Home)
        # --------------------------------------------------------------------------

        self.topleft.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        self.topRight.grid(row=0, column=1, sticky=tk.N + tk.S + tk.W + tk.E)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=40)

    def show_frame_directly(self, frame):
        if frame == self.frames[Home]:
            if len(pages) == 0:
                if frame == pages[len(pages) - 1]:
                    pass
                else:
                    pages.append(frame)
        frame.tkraise()

    def show_frame(self, context):
        frame = self.frames[context]
        if len(pages) > 1:
            if pages[len(pages) - 1] == frame:
                return
        rightPage.clear()
        resetCount()
        pages.append(frame)
        frame.tkraise()

    def show_frame_Main(self, data, image, r, c, text):
        from Base.listOfPage import musicPages
        if musicPages[r][c] == 0:
            frame = Main(self.topRight.topRightBottom,
                         self,
                         data=data,
                         image=image,
                         text=text)
            musicPages[r][c] = frame
        else:
            frame = musicPages[r][c]

        self.frames[Main] = frame
        frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        if pages[len(pages) - 1] == frame:
            return
        rightPage.clear()
        resetCount()
        pages.append(frame)
        frame.update()
        frame.tkraise()
