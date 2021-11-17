from tkinter import *
from tkinter.ttk import *           # modern look

"""
    This will create a top-level window (root) having a frame with a title bar,
    control box with the minimize and close buttons,
    and a client area to hold other widgets.
"""
window=Tk()                         # setup the application object
                
window.title("KDx")                 # title of the window

"""
    geometry("widthxheight+Xpos+Ypos")
    Xpos and YPos are the coordinates of the top left corner of the window
"""
# dimension of the window
screenWidth  = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

borWidth  = screenHeight * 0.025

# calculates the center position
##XPos = int(window.winfo_screenwidth()/2  - {reqWidth}/2)
##YPos = int(window.winfo_screenheight()/2 - {reqHeight}/2)

# Positions the window in the center of the screen.
##window.geometry("{}x{}+{}+{}".format({reqWidth}, {reqHeight}, XPos, YPos))

# all-round border color: 64, 64, 64 (RGB)
# background color: 255, 224, 224 (RGB)
# top-bar color: 224, 192, 192 (RGB)

# button color: 224, 240, 240 (RGB)
# special color (logo, button labels, etc.): grey50; 128, 128, 128 (RGB)

"""
    configure("customName.TWidgetName", options...)
"""
style = Style()
style.configure('Border.TFrame', background='#404040')
style.configure('PinkBG.TFrame', background='#FFE0E0', foreground='#000000')
style.configure('TopBG.TFrame', background='#E0C0C0')

style.configure('PinkBG.TLabel', background='#FFE0E0', foreground='#000000')

style.configure('LightBlueWhite.TButton', background='#E0F0F0', foreground='grey50')

"""
    Frame(parent, options...)
    size does not explicitly need to be specified 
    width:
    height:
    padding: padding around each widget child
    borderwidth: weight of border
    relief: flat (default), raised, sunken, solid, ridge, or groove. (Border style)
"""
backBorder = Frame(window, padding=borWidth, style='Border.TFrame')
backBorder.grid(row=0, column=0, sticky=(N, W, E, S))

# The columnconfigure/rowconfigure bits tell Tk that the frame should expand to
# fill any extra space if the window is resized.
##window.columnconfigure(0, weight=1)
##window.rowconfigure(0, weight=1)

frameWidth = screenWidth  - (2 * borWidth)

topFrame = Frame(backBorder, padding=borWidth/5, style='TopBG.TFrame')
topFrame['width']  = frameWidth
topFrame['height'] = 2 * borWidth
topFrame.grid(row=0, column=0)
topFrame.grid_propagate(False)

mainFrame = Frame(backBorder, padding=borWidth/5, style='PinkBG.TFrame')
mainFrame['width']  = frameWidth
mainFrame['height'] = screenHeight - (4 * borWidth)
mainFrame.grid(row=1, column=0)
mainFrame.grid_propagate(False)

"""
    Label(parent, options...)
    text: text to display
    textvariable: to monitor and display the value of a variable in the label
    image: to use an image file in the label
"""
# TODO: center and format font
# TODO: Dynamic username
welcomeLabel = Label(mainFrame, text='Welcome, USER!', style='PinkBG.TLabel')
welcomeLabel.grid(row=0, column=0)

"""
    Button(parent, options...)
"""
# TODO: center button frame
buttonFrame = Frame(mainFrame)
buttonFrame.grid(row=1, column=0)

# TODO: add image and format font
probeButton = Button(buttonFrame, text='Probe', style='LightBlueWhite.TButton')
probeButton.grid(row=0, column=0)

# TODO: add image and format font
cameraButton = Button(buttonFrame, text='Camera', style='LightBlueWhite.TButton')
cameraButton.grid(row=0, column=1)

# TODO: add image and format font
logsButton = Button(buttonFrame, text='Logs', style='LightBlueWhite.TButton')
logsButton.grid(row=0, column=2)

# --------------------------------Right Side------------------------------------ #

# TODO: center and format font
intakeLabel = Label(mainFrame, text='Potassium intake today:', style='PinkBG.TLabel')
intakeLabel.grid(row=0, column=1)

# TODO: add image and dynamic number reporting
intakeButton = Button(mainFrame, text='xxxx mg', style='LightBlueWhite.TButton')
intakeButton.grid(row=1, column=1)

# prevent resizing
window.attributes('-fullscreen', True)
window.resizable(False, False)

# The application object then enters an event listening loop:
window.mainloop()

# The application is now constantly waiting for any event generated
# on the elements in it. The event could be text entered in a text field,
# a selection made from the dropdown or radio button,
# single/double click actions of mouse, etc.
# The application's functionality involves executing appropriate
# callback functions in response to a particular type of event.
# The event loop will terminate as and when the close button is clicked
