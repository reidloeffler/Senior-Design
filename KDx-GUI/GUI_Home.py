from tkinter import *
from tkinter.ttk import *           # modern look

from PIL import Image, ImageTk      # Python Image Library

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
style.configure('PinkBG.TFrame', background='#FFE0E0', foreground='black')
style.configure('TopBG.TFrame', background='#E0C0C0')

style.configure('PinkBG.TLabel', background='#FFE0E0', foreground='black',
                font=(None, 32, 'bold'))
style.configure('Light.TLabel', background='#E0F0F0', foreground='black',
                font=(None, 16))

style.configure('Light.TButton', background='#E0F0F0', foreground='grey50',
                font=(None, 16))

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

logoSize = int(topFrame['height'] - 2*(borWidth/5))

logoImg = Image.open("images/banana2.png")
logoImg = logoImg.resize((logoSize, logoSize), Image.ANTIALIAS)
logoImg = ImageTk.PhotoImage(logoImg)

logoLabel = Label(topFrame, image = logoImg, background='#E0C0C0')
logoLabel.grid(row=0, column=0)

mainFrame = Frame(backBorder, style='PinkBG.TFrame')
mainFrame['width']  = frameWidth
mainFrame['height'] = screenHeight - (4 * borWidth)
mainFrame.grid(row=1, column=0)
mainFrame.grid_propagate(False)

# ---------------------------------Left Side------------------------------------ #

leftFrame = Frame(mainFrame, padding=borWidth/5, style='PinkBG.TFrame')
leftFrame['width']  = frameWidth * 0.5
leftFrame['height'] = mainFrame['height']
leftFrame.grid(row=0, column=0)
leftFrame.grid_propagate(False)

"""
    Label(parent, options...)
    text: text to display
    textvariable: to monitor and display the value of a variable in the label
    image: to use an image file in the label
"""
# TODO: center and format font
# TODO: Dynamic username
welcomeLabel = Label(leftFrame, text='Welcome, USER!', style='PinkBG.TLabel')
welcomeLabel['wraplength'] = leftFrame['width'] * (2/3)
welcomeLabel.grid(row=1, column=1)

"""
    Button(parent, options...)
"""
# TODO: center button frame
buttonFrame = Frame(leftFrame, style='PinkBG.TFrame')
buttonFrame.grid(row=3, column=1)

# give empty columns a weight so that they consume all extra space
leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.grid_columnconfigure(2, weight=1)

# give empty rows a weight so that they consume all extra space
leftFrame.grid_rowconfigure(0, weight=1)
leftFrame.grid_rowconfigure(2, weight=1)
leftFrame.grid_rowconfigure(4, weight=1)

probeImg = PhotoImage(file = "images/probe2.png")

# TODO: add image and format font
probeButton = Button(buttonFrame, text='Use Probe', style='Light.TButton')
probeButton['image'] = probeImg
probeButton['compound'] = TOP
probeButton.grid(row=0, column=0)

cameraImg = PhotoImage(file = "images/camera2.png")

# TODO: add image and format font
cameraButton = Button(buttonFrame, text='Use Camera', style='Light.TButton')
cameraButton['image'] = cameraImg
cameraButton['compound'] = TOP
cameraButton.grid(row=0, column=1)

logsImg = PhotoImage(file = "images/logs2.png")

# TODO: add image and format font
logsButton = Button(buttonFrame, text='Access Logs', style='Light.TButton')
logsButton['image'] = logsImg
logsButton['compound'] = TOP
logsButton.grid(row=0, column=2)

# --------------------------------Right Side------------------------------------ #

rightFrame = Frame(mainFrame, padding=borWidth/5, style='PinkBG.TFrame')
rightFrame['width']  = frameWidth * 0.5
rightFrame['height'] = mainFrame['height']
rightFrame.grid(row=0, column=1)
rightFrame.grid_propagate(False)

intakeImg = PhotoImage(file = "images/amount.png")

# TODO: center and format font
intakeLabel1 = Label(rightFrame, text='Potassium intake today:', style='PinkBG.TLabel')
intakeLabel1['wraplength'] = rightFrame['width'] * (2/3)
intakeLabel1.grid(row=1, column=1)

# TODO: add image and dynamic number reporting
intakeLabel2 = Label(rightFrame, text='xxxx mg', style='Light.TLabel')
intakeLabel2['image'] = intakeImg
intakeLabel2['compound'] = TOP
intakeLabel2.grid(row=3, column=1)

# give empty columns a weight so that they consume all extra space
rightFrame.grid_columnconfigure(0, weight=1)
rightFrame.grid_columnconfigure(2, weight=1)

# give empty rows a weight so that they consume all extra space
rightFrame.grid_rowconfigure(0, weight=1)
rightFrame.grid_rowconfigure(2, weight=1)
rightFrame.grid_rowconfigure(4, weight=1)

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
