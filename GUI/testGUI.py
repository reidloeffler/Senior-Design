from tkinter import *
from tkinter.ttk import *           # modern look

"""
    This will create a top-level window (root) having a frame with a title bar,
    control box with the minimize and close buttons,
    and a client area to hold other widgets.
"""
window=Tk()                         # setup the application object
                
window.title("Hello Python")        # title of the window

"""
    geometry("widthxheight+Xpos+Ypos")
    Xpos and YPos are the coordinates of the top left corner of the window
"""
# dimension of the window
winWidth  = 1600
winHeight = 900

# calculates the center position
XPos = int(window.winfo_screenwidth()/2  - winWidth/2)
YPos = int(window.winfo_screenheight()/2 - winHeight/2)

# Positions the window in the center of the page.
window.geometry("{}x{}+{}+{}".format(winWidth, winHeight, XPos, YPos))

"""
    Frame(parent, options...)

    size does not explicitly need to be specified 
    width:
    height:
    padding: padding around each widget child
    borderwidth: weight of border
    relief: flat (default), raised, sunken, solid, ridge, or groove. (Border style)
    
"""
frame = Frame(window, padding=10)
frame.grid()

"""
    configure("customName.TWidgetName", options...)
"""
style = Style()
##style.configure("Danger.TFrame", background="red", borderwidth=5, relief='raised')

"""
    Label(parent, options...)

    text: text to display
    textvariable: to monitor and display the value of a variable in the label
    image: to use an image file in the label
"""
label = Label(frame, text='This is a Label.', font="TkMenuFont").grid(column=0, row=0)

"""
    
"""

"""
    
"""

# The application object then enters an event listening loop:
window.mainloop()

# The application is now constantly waiting for any event generated
# on the elements in it. The event could be text entered in a text field,
# a selection made from the dropdown or radio button,
# single/double click actions of mouse, etc.
# The application's functionality involves executing appropriate
# callback functions in response to a particular type of event.
# The event loop will terminate as and when the close button is clicked
