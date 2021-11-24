import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

class CircularProgressbar(object):
    def __init__(self, canvas, x0, y0, x1, y1, width=2, start_ang=0, full_extent=360):

        self.custom_font = tkFont.Font(family='Consolas', size=20, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent
        
        # draw static bar outline
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2)
        self.running = False

    def start(self, interval=100):
        self.interval = interval
        self.increment = self.full_extent / interval
        self.extent = 0
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                             width=self.width, style='arc')
        percent = '0\nmg'
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                font=self.custom_font)
        self.running = True
        self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        """Increment extent and update arc and label displaying how much completed."""
        if self.running:
            self.extent = (self.extent + delta) % 360
            self.canvas.itemconfigure(self.arc_id, extent=self.extent)
            percent = "{:0>4}".format(str(round((self.extent * 3000) / self.full_extent))) + "\n mg "
            self.canvas.itemconfigure(self.label_id, text=percent)

        self.after_id = self.canvas.after(self.interval, self.step, delta)

    def toggle_pause(self):
        self.running = not self.running
