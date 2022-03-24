from tkinter import *
from tkinter.ttk import *           # modern look

from PIL import Image, ImageTk      # Python Image Library

from datetime import datetime       # current day & date

from CircularProgressbar import *

#----------------------------------------------------------------------
# callback function to update date and time every 100 ms

def update_datetime():
    timeLabel.configure(text=f"{datetime.now():%X}")
    dateLabel.configure(text=f"{datetime.now():%a, %b %d %Y}")
    window.after(100, update_datetime)

#----------------------------------------------------------------------
    
#----------------------------------------------------------------------
# callback functions to perform frame switch

def probe():        # hide the home frame and show the probe frame
    homeFrame.grid_remove()
    probeFrame.grid()

def camera():       # hide the home frame and show the camera frame
    homeFrame.grid_remove()
    cameraFrame.grid()

def logs():         # hide the home frame and show the logs frame
    homeFrame.grid_remove()
    logsFrame.grid()

def home():         # hide all the frames except the home frame
    probeFrame.grid_remove()
    cameraFrame.grid_remove()
    logsFrame.grid_remove()
    homeFrame.grid()

#----------------------------------------------------------------------

"""
    This will create a top-level window (root) having a frame with a title bar,
    control box with the minimize and close buttons,
    and a client area to hold other widgets.
"""
window=Tk()                         # setup the application object
                
window.title("K-Dx")                # title of the window
    
"""
    geometry("widthxheight+Xpos+Ypos")
    Xpos and YPos are the coordinates of the top left corner of the window
"""
# dimension of the window
screenWidth  = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

borWidth = screenHeight * 0.025

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
style.configure('Black.TFrame', background='black', foreground='white')
style.configure('TopBG.TFrame', background='#E0C0C0')

style.configure('PinkBG.TLabel', background='#FFE0E0', foreground='black', font=(None, 50, 'bold'))
style.configure('Light.TLabel', background='#E0F0F0', foreground='grey25', font=(None, 25))
style.configure('Dark.TLabel', background='black', foreground='grey50', font=(None, 50, 'bold'))

style.configure('Light.TButton', background='#E0F0F0', foreground='grey25', font=(None, 30))

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

# ----------------------------------Top bar------------------------------------- #

topFrame = Frame(backBorder, padding=borWidth/5, style='TopBG.TFrame')
topFrame['width']  = frameWidth
topFrame['height'] = 2 * borWidth
topFrame.grid(row=0, column=0)
topFrame.grid_propagate(False)              # disables fit to contents

logoSize = int(topFrame['height'] - 2*(borWidth/5))

logoImg = Image.open("images/banana2.png")
logoImg = logoImg.resize((logoSize, logoSize), Image.ANTIALIAS)
logoImg = ImageTk.PhotoImage(logoImg)

logoLabel = Label(topFrame, image = logoImg, background='#E0C0C0')
logoLabel.grid(row=0, column=0, sticky=(N, W, S))

timeLabel = Label(topFrame, foreground='black', background='#E0C0C0', font=(None, 25, 'bold'))
timeLabel.grid(row=0, column=1, sticky=(N, S))

dateLabel = Label(topFrame, foreground='black', background='#E0C0C0', font=(None, 25, 'bold'))
dateLabel.grid(row=0, column=2, sticky=(N, E, S))

update_datetime()

# center column expands to consume all extra space
topFrame.grid_columnconfigure(0, weight=1, uniform='top')
topFrame.grid_columnconfigure(1, weight=1, uniform='top')
topFrame.grid_columnconfigure(2, weight=1, uniform='top')

mainFrame = Frame(backBorder, style='PinkBG.TFrame')
mainFrame['width']  = frameWidth
mainFrame['height'] = screenHeight - (4 * borWidth)
mainFrame.grid(row=1, column=0)
mainFrame.grid_propagate(False)

homeFrame = Frame(mainFrame, style='PinkBG.TFrame')
homeFrame.grid(row=0, column=0)

# ---------------------------------Left Side------------------------------------ #

leftFrame = Frame(homeFrame, padding=borWidth/5, style='PinkBG.TFrame')
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
buttonFrame['height'] = (leftFrame['height'] / 4) - borWidth
buttonFrame['width']  = leftFrame['width'] - borWidth
buttonFrame.grid(row=3, column=1)
buttonFrame.grid_propagate(False)

# give empty columns a weight so that they consume all extra space
leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.grid_columnconfigure(2, weight=1)

# give empty rows a weight so that they consume all extra space
leftFrame.grid_rowconfigure(0, weight=1)
leftFrame.grid_rowconfigure(2, weight=1)
leftFrame.grid_rowconfigure(4, weight=1)

probeImg = PhotoImage(file = "images/probe2.png")

# TODO: add image and format font
probeButton = Button(buttonFrame, text='Use Probe', style='Light.TButton', command=probe)
probeButton['image'] = probeImg
probeButton['compound'] = TOP
probeButton.grid(row=0, column=1)

cameraImg = PhotoImage(file = "images/camera2.png")

# TODO: add image and format font
cameraButton = Button(buttonFrame, text='Use Camera', style='Light.TButton', command=camera)
cameraButton['image'] = cameraImg
cameraButton['compound'] = TOP
cameraButton.grid(row=0, column=3)

logsImg = PhotoImage(file = "images/logs2.png")

# TODO: add image and format font
logsButton = Button(buttonFrame, text='Access Logs', style='Light.TButton', command=logs)
logsButton['image'] = logsImg
logsButton['compound'] = TOP
logsButton.grid(row=0, column=5)

# give empty columns a weight so that they consume all extra space
buttonFrame.grid_columnconfigure(0, weight=2)
buttonFrame.grid_columnconfigure(2, weight=1)
buttonFrame.grid_columnconfigure(4, weight=1)
buttonFrame.grid_columnconfigure(6, weight=2)

# --------------------------------Right Side------------------------------------ #

rightFrame = Frame(homeFrame, padding=borWidth/5, style='PinkBG.TFrame')
rightFrame['width']  = frameWidth * 0.5
rightFrame['height'] = mainFrame['height']
rightFrame.grid(row=0, column=1)
rightFrame.grid_propagate(False)

intakeImg = PhotoImage(file = "images/amount.png")

# TODO: center and format font
intakeLabel1 = Label(rightFrame, text='K+ intake today:', style='PinkBG.TLabel')
intakeLabel1['wraplength'] = rightFrame['width'] * (2/3)
intakeLabel1.grid(row=1, column=1)

# TODO: add image and dynamic number reporting
##intakeLabel2 = Label(rightFrame, text='xxxx mg', style='Light.TLabel')
##intakeLabel2['image'] = intakeImg
##intakeLabel2['compound'] = TOP
##intakeLabel2.grid(row=3, column=1)

intakeVisual = tk.Canvas(rightFrame, width=500, height=500, bg='#FFE0E0', highlightthickness=0)
intakeVisual.grid(row=3, column=1)

progressbar = CircularProgressbar(intakeVisual, 0, 0, 500, 500, 50)

progressbar.start()

# give empty columns a weight so that they consume all extra space
rightFrame.grid_columnconfigure(0, weight=1)
rightFrame.grid_columnconfigure(2, weight=1)

# give empty rows a weight so that they consume all extra space
rightFrame.grid_rowconfigure(0, weight=1)
rightFrame.grid_rowconfigure(2, weight=1)
rightFrame.grid_rowconfigure(4, weight=1)

#===================================================================================================

probeFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
probeFrame['width']  = frameWidth
probeFrame['height'] = mainFrame['height']
probeFrame.grid(row=1, column=0)
probeFrame.grid_propagate(False)

b1 = Button(probeFrame, text="< Back", style='Light.TButton', command=home)
b1.grid(row=2, column=0, sticky=(W, S))

startProbe = Button(probeFrame, text="Start Measuring", style='Light.TButton')      # TODO: command
startProbe.grid(row=0, column=1)

helpB1 = Button(probeFrame, text="Help", style='Light.TButton')                     # TODO: command
helpB1.grid(row=2, column=2, sticky=(E, S))

probeFrame.grid_columnconfigure(0, weight=1)
probeFrame.grid_columnconfigure(2, weight=1)

probeFrame.grid_rowconfigure(0, weight=1)
probeFrame.grid_rowconfigure(1, weight=1)

#===================================================================================================

cameraFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
cameraFrame['width']  = frameWidth
cameraFrame['height'] = mainFrame['height']
cameraFrame.grid(row=2, column=0)
cameraFrame.grid_propagate(False)

picFrame = Frame(cameraFrame, style='Black.TFrame')
picFrame['width']  = frameWidth - borWidth
picFrame['height'] = mainFrame['height'] * 0.80
picFrame.grid(row=0, column=0)
picFrame.grid_propagate(False)

cameraPlaceholder = Label(picFrame, style='Dark.TLabel', text="[Camera Feed]")
cameraPlaceholder.grid(row=1, column=1)

picFrame.grid_rowconfigure(0, weight=1)
picFrame.grid_rowconfigure(2, weight=1)
picFrame.grid_columnconfigure(0, weight=1)
picFrame.grid_columnconfigure(2, weight=1)

buttonsFrame = Frame(cameraFrame, style='PinkBG.TFrame')
buttonsFrame['width']  = frameWidth - borWidth
buttonsFrame['height'] = mainFrame['height'] * 0.10
buttonsFrame.grid(row=2, column=0)
buttonsFrame.grid_propagate(False)

b2 = Button(buttonsFrame, text="< Back", style='Light.TButton', command=home)
b2.grid(row=0, column=0)

picButton = Button(buttonsFrame, text="Take Picture", style='Light.TButton')        # TODO: command
picButton.grid(row=0, column=2)

helpB2 = Button(buttonsFrame, text="Help", style='Light.TButton')                   # TODO: command
helpB2.grid(row=0, column=4)

buttonsFrame.grid_columnconfigure(1, weight=1)
buttonsFrame.grid_columnconfigure(3, weight=1)

cameraFrame.grid_rowconfigure(1, weight=1)

#===================================================================================================

logsFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
logsFrame['width']  = frameWidth
logsFrame['height'] = mainFrame['height']
logsFrame.grid(row=3, column=0)
logsFrame.grid_propagate(False)

numHeading = Label(logsFrame, text="Number", style='PinkBG.TLabel')
numHeading.grid(row=0, column=0)

dayHeading = Label(logsFrame, text="Day", style='PinkBG.TLabel')
dayHeading.grid(row=0, column=1)

dateHeading = Label(logsFrame, text="Date", style='PinkBG.TLabel')
dateHeading.grid(row=0, column=2)

timeHeading = Label(logsFrame, text="Time", style='PinkBG.TLabel')
timeHeading.grid(row=0, column=3)

KHeading = Label(logsFrame, text="K intake", style='PinkBG.TLabel')
KHeading.grid(row=0, column=4)

# TODO: add table entries

b3 = Button(logsFrame, text="< Back", style='Light.TButton', command=home)
b3.grid(row=10, column=0, sticky=(W, S))

helpB3 = Button(logsFrame, text="Help", style='Light.TButton')                      # TODO: command
helpB3.grid(row=10, column=4, sticky=(E, S))

logsFrame.grid_columnconfigure(0, weight=1)
logsFrame.grid_columnconfigure(1, weight=1)
logsFrame.grid_columnconfigure(2, weight=1)
logsFrame.grid_columnconfigure(3, weight=1)
logsFrame.grid_columnconfigure(4, weight=1)

logsFrame.grid_rowconfigure(10, weight=1)

#===================================================================================================

# hide the other frames
probeFrame.grid_remove()
cameraFrame.grid_remove()
logsFrame.grid_remove()

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
