from tkinter import *
from tkinter.ttk import *           # modern look

import io
import os

from time import sleep

from PIL import Image, ImageTk      # Python Image Library

from datetime import datetime       # current day & date

from godirect import GoDirect

from google.cloud import vision     # Google Vision API

from CircularProgressbar import *

#----------------------------------------------------------------------
# callback function to update date and time every 100 ms

def update_datetime():
    timeLabel.configure(text=f"{datetime.now():%X}")
    dateLabel.configure(text=f"{datetime.now():%a, %b %d %Y}")
    window.after(100, update_datetime)

#----------------------------------------------------------------------

probeInstructions = "1. Fill sample vial with food up to dotted line.\n2. Fill water up to solid line.\n3. Screw vial onto homogenizer and blend.\n4. Attach vial to probe and start measurement using the button above."

#----------------------------------------------------------------------
# callback function to start measuring using the probe

val = 0.0

def measure():

    global val
    val = 0.0

    msg = ''

    startProbe.state(["disabled"])

    probeContent.configure(text="Reading Sensor...")

    window.update()

    godirect = GoDirect(use_ble=False, use_usb=True)

    # returns a GoDirectDevice on success or None on failure
    device = godirect.get_device()

    # GDX-ISEA 0W1010Q5

    # open() returns True on success or False on failure.
    if device != None and device.open():

        device.enable_sensors([6])                              # Potassium sensor is no. 6

        # start data collection for the enabled sensor
        if device.start(period=1000):                           # sample period (milliseconds)

            sum = 0.0

            n = 5

            for i in range(0, n):
                if device.read():
                    for sensor in device.get_enabled_sensors():
                        sum += (sensor.value * ((5 + 10) / 5))  # 5 mL of sample, 10 mL of water
                        window.update()
                else:
                    msg = "Error: could not read sensor"

            val = sum / n
            msg = "K+ concentration (mg/L): " + "{:.2f}".format(val)

            device.stop()

        else:
            msg = "Error: failed to start data collection"

        device.close()

    else:

        if device == None:
            msg = "Error: could not detect probe device"
        else:
            msg = "Error: could not connect to the probe"

    godirect.quit()

    startProbe.state(["!disabled"])

    if val > 0.0:
        volumeContent.configure(text=msg)
        volume()
    else:
        probeContent.configure(text=msg)

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# callback function to take a picture

def take_pic():

    picButton.grid_remove()

    cameraPreview.configure(compound='text')
    cameraPreview.grid()

    window.update()

    w = int(picFrame['width'] - borWidth)
    h = int(picFrame['height'] - borWidth)

    os.system("libcamera-still -n --width " + str(w) + " --height " + str(h) + " --rotation 180 -o pic.jpg --autofocus")

    img = Image.open("pic.jpg")
    img = ImageTk.PhotoImage(img)

    cameraPreview.configure(image=img)
    cameraPreview.configure(compound='image')

    picButton.grid()

    helpB2.state(["!disabled"])

    img.close()     # window.update() ?

#----------------------------------------------------------------------

vision_results = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]

#----------------------------------------------------------------------
# callback function to recognize a picture

def cloud_vision():

    client = vision.ImageAnnotatorClient()

    #local image
    with io.open("pic.jpg", 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)

    i = 0
    for label in response.label_annotations:
        vision_results[i] = (label.description, str(int(label.score * 100)))
        i += 1
        if i == 6:
            break

    visionLabel.configure(text="Top 6 results (Confidence %'s):")

    visionB1.configure(text=vision_results[0][0]+" ("+vision_results[0][1]+"%)")
    visionB2.configure(text=vision_results[1][0]+" ("+vision_results[1][1]+"%)")
    visionB3.configure(text=vision_results[2][0]+" ("+vision_results[2][1]+"%)")
    visionB4.configure(text=vision_results[3][0]+" ("+vision_results[3][1]+"%)")
    visionB5.configure(text=vision_results[4][0]+" ("+vision_results[4][1]+"%)")
    visionB6.configure(text=vision_results[5][0]+" ("+vision_results[5][1]+"%)")

    visionButtons.grid()

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# callback functions for choosing recognized foods

def choice1():
    if query(vision_results[0][0]):
        vision_to_vol()
    else:
        visionLabel.configure(text=vision_results[0][0]+" not in internal look-up table.")

def choice2():
    if query(vision_results[1][0]):
        vision_to_vol()
    else:
        visionLabel.configure(text=vision_results[1][0]+" not in internal look-up table.")

def choice3():
    if query(vision_results[2][0]):
        vision_to_vol()
    else:
        visionLabel.configure(text=vision_results[2][0]+" not in internal look-up table.")

def choice4():
    if query(vision_results[3][0]):
        vision_to_vol()
    else:
        visionLabel.configure(text=vision_results[3][0]+" not in internal look-up table.")

def choice5():
    if query(vision_results[4][0]):
        vision_to_vol()
    else:
        visionLabel.configure(text=vision_results[4][0]+" not in internal look-up table.")

def choice6():
    if query(vision_results[5][0]):
        vision_to_vol()
    else:
        visionLabel.configure(text=vision_results[5][0]+" not in internal look-up table.")

def query(string):
    global val
    val = 0.0

    search_term = string.strip().lower()

    found = False

    for line_num, line in enumerate(open('lookup_table.txt', 'rt')):
        if line_num % 2 == 0 and search_term in line.lower().split(", ")[0]:
            found = True
        elif (line_num + 1) % 2 == 0 and found:
            val = float(line.strip().split()[0])
            volumeContent.configure(text="K+ concentration (mg/L): " + "{:.2f}".format(val))
            break

    return found

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# callback functions for volume input

final_val = 0.0

def zero():
    volumeInput.configure(text=volumeInput['text'] + "0")

def one():
    volumeInput.configure(text=volumeInput['text'] + "1")

def two():
    volumeInput.configure(text=volumeInput['text'] + "2")

def three():
    volumeInput.configure(text=volumeInput['text'] + "3")

def four():
    volumeInput.configure(text=volumeInput['text'] + "4")

def five():
    volumeInput.configure(text=volumeInput['text'] + "5")

def six():
    volumeInput.configure(text=volumeInput['text'] + "6")

def seven():
    volumeInput.configure(text=volumeInput['text'] + "7")

def eight():
    volumeInput.configure(text=volumeInput['text'] + "8")

def nine():
    volumeInput.configure(text=volumeInput['text'] + "9")

def clear():
    volumeInput.configure(text='')

def submit():
    if not volumeInput['text'] == '':
        global final_val
        vol = int(volumeInput['text']) * 0.236588        # mL per cup
        final_val = val * vol
        resultsLabel.configure(text="This meal contains ≈\n\n" + "{:.2f}".format(final_val) + " mg of Potassium")
        progressbar.step(round((final_val/5000) * 360))
        clear()
        results()

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# callback functions to perform frame switch

def probe():        # hide the home frame and show the probe frame
    homeFrame.grid_remove()
    probeFrame.grid()

def camera():       # hide the home frame and show the camera frame
    homeFrame.grid_remove()
    cameraFrame.grid();

def logs():         # hide the home frame and show the logs frame
    homeFrame.grid_remove()
    logsFrame.grid()

def volume():       # hide the probe frame and show the volume frame
    probeFrame.grid_remove(); probeContent.configure(text=probeInstructions)
    volumeFrame.grid()

def results():      # hide the volume frame and show results for 5 seconds
    volumeFrame.grid_remove(); volumeContent.configure(text='')
    resultsFrame.grid()
    sleep(1)
    window.update()
    sleep(1)
    window.update()
    sleep(1)
    window.update()
    sleep(1)
    window.update()
    sleep(1)
    window.update()
    home()

def recognize():
    cameraFrame.grid_remove(); cameraPreview.grid_remove(); helpB2.state(["disabled"])
    visionFrame.grid()
    window.update()
    cloud_vision()

def vision_to_cam():
    visionLabel.configure(text="Processing Image...")
    visionButtons.grid_remove()
    visionFrame.grid_remove()
    cameraFrame.grid()

def vision_to_vol():
    visionLabel.configure(text="Processing Image...")
    visionButtons.grid_remove()
    visionFrame.grid_remove()
    volumeFrame.grid()

def home():         # hide all the frames except the home frame
    probeFrame.grid_remove(); probeContent.configure(text=probeInstructions)
    cameraFrame.grid_remove(); cameraPreview.grid_remove(); helpB2.state(["disabled"])
    logsFrame.grid_remove()
    volumeFrame.grid_remove(); volumeContent.configure(text='')
    resultsFrame.grid_remove()
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

borWidth = screenHeight * 0.05

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

style.configure('Welcome.TLabel', background='#FFE0E0', foreground='black', font=(None, 35, 'bold'))
style.configure('Results.TLabel', background='#FFE0E0', foreground='black', font=(None, 25, 'bold'))
style.configure('PinkBG.TLabel', background='#FFE0E0', foreground='black', font=(None, 20, 'bold'))
style.configure('PinkBG_small.TLabel', background='#FFE0E0', foreground='black', font=(None, 17, 'bold'))
style.configure('Light.TLabel', background='#E0F0F0', foreground='grey25', font=(None, 15))
style.configure('Dark.TLabel', background='black', foreground='grey50', font=(None, 25, 'bold'))

style.configure('Light.TButton', background='#E0F0F0', foreground='grey25', font=(None, 13), borderwidth=5)
style.configure('Dark.TButton', background='grey75', foreground='black', font=(None, 15, 'bold'), borderwidth=5)

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

timeLabel = Label(topFrame, foreground='black', background='#E0C0C0', font=(None, 15, 'bold'))
timeLabel.grid(row=0, column=1, sticky=(N, S))

dateLabel = Label(topFrame, foreground='black', background='#E0C0C0', font=(None, 15, 'bold'))
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
leftFrame['width']  = frameWidth * 0.6
leftFrame['height'] = mainFrame['height']
leftFrame.grid(row=0, column=0)
leftFrame.grid_propagate(False)

"""
    Label(parent, options...)
    text: text to display
    textvariable: to monitor and display the value of a variable in the label
    image: to use an image file in the label
"""
welcomeLabel = Label(leftFrame, text='Welcome!', style='Welcome.TLabel')
welcomeLabel.grid(row=1, column=1)

Exit = Button(leftFrame, text='Exit', style='Dark.TButton', command=window.destroy)
Exit.grid(row=4, column=1)
#Exit.grid_remove()

"""
    Button(parent, options...)
"""
buttonFrame = Frame(leftFrame, style='PinkBG.TFrame')
buttonFrame['height'] = (leftFrame['height'] / 3) - borWidth
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

probeImg = Image.open("images/probe2.png")
probeImg = probeImg.resize((logoSize, logoSize), Image.ANTIALIAS)
probeImg = ImageTk.PhotoImage(probeImg)

probeButton = Button(buttonFrame, text='Probe', style='Light.TButton', command=probe)
probeButton['image'] = probeImg
probeButton['compound'] = TOP
probeButton.grid(row=0, column=1)

cameraImg = Image.open("images/camera2.png")
cameraImg = cameraImg.resize((logoSize, logoSize), Image.ANTIALIAS)
cameraImg = ImageTk.PhotoImage(cameraImg)

cameraButton = Button(buttonFrame, text='Camera', style='Light.TButton', command=camera)
cameraButton['image'] = cameraImg
cameraButton['compound'] = TOP
cameraButton.grid(row=0, column=3)

logsImg = Image.open("images/logs2.png")
logsImg = logsImg.resize((logoSize, logoSize), Image.ANTIALIAS)
logsImg = ImageTk.PhotoImage(logsImg)

logsButton = Button(buttonFrame, text='Logs', style='Light.TButton', command=logs)
logsButton['image'] = logsImg
logsButton['compound'] = TOP
logsButton.grid(row=0, column=5)

# give empty columns a weight so that they consume all extra space
buttonFrame.grid_columnconfigure(0, weight=1)
buttonFrame.grid_columnconfigure(2, weight=1)
buttonFrame.grid_columnconfigure(4, weight=1)
buttonFrame.grid_columnconfigure(6, weight=1)

# --------------------------------Right Side------------------------------------ #

rightFrame = Frame(homeFrame, padding=borWidth/5, style='PinkBG.TFrame')
rightFrame['width']  = frameWidth * 0.4
rightFrame['height'] = mainFrame['height']
rightFrame.grid(row=0, column=1)
rightFrame.grid_propagate(False)

intakeImg = PhotoImage(file = "images/amount.png")

intakeLabel1 = Label(rightFrame, text='K+ intake today:', style='PinkBG.TLabel')
intakeLabel1['wraplength'] = rightFrame['width'] * (2/3)
intakeLabel1.grid(row=1, column=1)

intakeVisual = tk.Canvas(rightFrame, width=200, height=200, bg='#FFE0E0', highlightthickness=0)
intakeVisual.grid(row=3, column=1)

progressbar = CircularProgressbar(intakeVisual, 0, 0, 200, 200, 20)

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
b1.grid(row=4, column=0, sticky=(W, S))

startProbe = Button(probeFrame, text="Take Measurement", style='Light.TButton', command=measure)
startProbe.grid(row=0, column=1, sticky=(N))

probeContent = Label(probeFrame, text=probeInstructions, style='PinkBG_small.TLabel')
probeContent['wraplength'] = probeFrame['width'] * (2/3)
probeContent.grid(row=2, column=1)

helpB1 = Button(probeFrame, text="Help", style='Light.TButton')                     # TODO: command
helpB1.grid(row=4, column=2, sticky=(E, S))

probeFrame.grid_columnconfigure(0, weight=1)
probeFrame.grid_columnconfigure(2, weight=1)

probeFrame.grid_rowconfigure(0, weight=1)
probeFrame.grid_rowconfigure(1, weight=1)
probeFrame.grid_rowconfigure(3, weight=1)

#===================================================================================================

cameraFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
cameraFrame['width']  = frameWidth
cameraFrame['height'] = mainFrame['height']
cameraFrame.grid(row=2, column=0)
cameraFrame.grid_propagate(False)

picFrame = Frame(cameraFrame, style='Black.TFrame')
picFrame['width']  = frameWidth - borWidth
picFrame['height'] = (cameraFrame['height'] - borWidth) * 0.80
picFrame.grid(row=0, column=0)
picFrame.grid_propagate(False)

cameraPreview = Label(picFrame, text="Taking Picture...", image=None, style='Dark.TLabel')
cameraPreview.grid(row=1, column=1)

picFrame.grid_columnconfigure(0, weight=1)
picFrame.grid_columnconfigure(2, weight=1)

picFrame.grid_rowconfigure(0, weight=1)
picFrame.grid_rowconfigure(2, weight=1)

cameraPreview.grid_remove()

buttonsFrame = Frame(cameraFrame, style='PinkBG.TFrame')
buttonsFrame['width']  = frameWidth - borWidth
buttonsFrame['height'] = (cameraFrame['height'] - borWidth) * 0.15
buttonsFrame.grid(row=2, column=0)
buttonsFrame.grid_propagate(False)

b2 = Button(buttonsFrame, text="< Back", style='Light.TButton', command=home)
b2.grid(row=0, column=0)

picButton = Button(buttonsFrame, text="Take Picture", style='Light.TButton', command=take_pic)
picButton.grid(row=0, column=2)

helpB2 = Button(buttonsFrame, text="Next >", style='Light.TButton', command=recognize)
helpB2.grid(row=0, column=4)
helpB2.state(["disabled"])

buttonsFrame.grid_columnconfigure(1, weight=1)
buttonsFrame.grid_columnconfigure(3, weight=1)

cameraFrame.grid_rowconfigure(1, weight=1)

#===================================================================================================

logsFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
logsFrame['width']  = frameWidth
logsFrame['height'] = mainFrame['height']
logsFrame.grid(row=3, column=0)
logsFrame.grid_propagate(False)

numHeading = Label(logsFrame, text="Number", style='PinkBG_small.TLabel')
numHeading.grid(row=0, column=0)

dayHeading = Label(logsFrame, text="Day", style='PinkBG_small.TLabel')
dayHeading.grid(row=0, column=1)

dateHeading = Label(logsFrame, text="Date", style='PinkBG_small.TLabel')
dateHeading.grid(row=0, column=2)

timeHeading = Label(logsFrame, text="Time", style='PinkBG_small.TLabel')
timeHeading.grid(row=0, column=3)

KHeading = Label(logsFrame, text="K+ intake", style='PinkBG_small.TLabel')
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

volumeFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
volumeFrame['width']  = frameWidth
volumeFrame['height'] = mainFrame['height']
volumeFrame.grid(row=4, column=0)
volumeFrame.grid_propagate(False)

volumeContent = Label(volumeFrame, text='', style='PinkBG_small.TLabel')
volumeContent.grid(row=1, column=1)

volumeInputInstructions = Label(volumeFrame, text='How many cups of total food? (1 cup ≈ 237 mL)', style='PinkBG_small.TLabel')
volumeInputInstructions.grid(row=3, column=1)

volumeInput = Label(volumeFrame, text='', style='PinkBG_small.TLabel')
volumeInput.grid(row=4, column=1)

numpadFrame = Frame(volumeFrame, style='PinkBG.TFrame')
numpadFrame.grid(row=6, column=1)

# commands simulate input by updating volumeInput Label
button7 = Button(numpadFrame, text='7', style='Dark.TButton', command=seven)
button7.grid(row=1, column=1)

button8 = Button(numpadFrame, text='8', style='Dark.TButton', command=eight)
button8.grid(row=1, column=2)

button9 = Button(numpadFrame, text='9', style='Dark.TButton', command=nine)
button9.grid(row=1, column=3)

button4 = Button(numpadFrame, text='4', style='Dark.TButton', command=four)
button4.grid(row=2, column=1)

button5 = Button(numpadFrame, text='5', style='Dark.TButton', command=five)
button5.grid(row=2, column=2)

button6 = Button(numpadFrame, text='6', style='Dark.TButton', command=six)
button6.grid(row=2, column=3)

button1 = Button(numpadFrame, text='1', style='Dark.TButton', command=one)
button1.grid(row=3, column=1)

button2 = Button(numpadFrame, text='2', style='Dark.TButton', command=two)
button2.grid(row=3, column=2)

button3 = Button(numpadFrame, text='3', style='Dark.TButton', command=three)
button3.grid(row=3, column=3)

button0 = Button(numpadFrame, text='0', style='Dark.TButton', command=zero)
button0.grid(row=4, column=2)

button_ = Button(numpadFrame, text='Clear', style='Dark.TButton', command=clear)
button_.grid(row=5, column=1)

buttonSubmit = Button(numpadFrame, text='Submit', style='Dark.TButton', command=submit)
buttonSubmit.grid(row=5, column=3)

volumeFrame.grid_columnconfigure(0, weight=1)
volumeFrame.grid_columnconfigure(2, weight=1)

volumeFrame.grid_rowconfigure(0, weight=1)
volumeFrame.grid_rowconfigure(2, weight=1)
volumeFrame.grid_rowconfigure(5, weight=1)
volumeFrame.grid_rowconfigure(7, weight=1)

#===================================================================================================

visionFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
visionFrame['width']  = frameWidth
visionFrame['height'] = mainFrame['height']
visionFrame.grid(row=5, column=0)
visionFrame.grid_propagate(False)

visionLabel = Label(visionFrame, text="Processing Image...", style='Results.TLabel')
visionLabel['wraplength'] = frameWidth - (2 * borWidth)
visionLabel.grid(row=1, column=1)

visionButtons = Frame(visionFrame, style='PinkBG.TFrame')
visionButtons['width'] = visionLabel['wraplength'] + borWidth
visionButtons['height'] = mainFrame['height'] * (2/3)
visionButtons.grid(row=3, column=1)
visionButtons.grid_propagate(False)

visionB1 = Button(visionButtons, text='Food-1', style='Light.TButton', command=choice1)
visionB1.grid(row=1, column=1, sticky=(N, W))

visionB2 = Button(visionButtons, text='Food-2', style='Light.TButton', command=choice2)
visionB2.grid(row=1, column=3, sticky=(N))

visionB3 = Button(visionButtons, text='Food-3', style='Light.TButton', command=choice3)
visionB3.grid(row=1, column=5, sticky=(N, E))

visionB4 = Button(visionButtons, text='Food-4', style='Light.TButton', command=choice4)
visionB4.grid(row=3, column=1, sticky=(W))

visionB5 = Button(visionButtons, text='Food-5', style='Light.TButton', command=choice5)
visionB5.grid(row=3, column=3)

visionB6 = Button(visionButtons, text='Food-6', style='Light.TButton', command=choice6)
visionB6.grid(row=3, column=5, sticky=(E))

visionBack = Button(visionButtons, text='< Retake', style='Dark.TButton', command=vision_to_cam)
visionBack.grid(row=5, column=3, sticky=(S))

visionButtons.grid_columnconfigure(1, weight=1, uniform='buttons')
visionButtons.grid_columnconfigure(3, weight=1, uniform='buttons')
visionButtons.grid_columnconfigure(5, weight=1, uniform='buttons')

"""
visionButtons.grid_columnconfigure(0, weight=1)
visionButtons.grid_columnconfigure(2, weight=1)
visionButtons.grid_columnconfigure(4, weight=1)
visionButtons.grid_columnconfigure(6, weight=1)
"""

visionButtons.grid_rowconfigure(0, weight=1)
visionButtons.grid_rowconfigure(2, weight=1)
visionButtons.grid_rowconfigure(4, weight=1)
visionButtons.grid_rowconfigure(6, weight=1)

visionButtons.grid_remove()

visionFrame.grid_columnconfigure(0, weight=1)
visionFrame.grid_columnconfigure(2, weight=1)

visionFrame.grid_rowconfigure(0, weight=1)
visionFrame.grid_rowconfigure(2, weight=1)
visionFrame.grid_rowconfigure(4, weight=1)

#===================================================================================================

resultsFrame = Frame(mainFrame, style='PinkBG.TFrame', padding=borWidth/2)
resultsFrame['width']  = frameWidth
resultsFrame['height'] = mainFrame['height']
resultsFrame.grid(row=6, column=0)
resultsFrame.grid_propagate(False)

resultsLabel = Label(resultsFrame, text='', style='Results.TLabel')
resultsLabel['wraplength'] = frameWidth - (2 * borWidth)
resultsLabel.grid(row=1, column=1)

resultsFrame.grid_columnconfigure(0, weight=1)
resultsFrame.grid_columnconfigure(2, weight=1)

resultsFrame.grid_rowconfigure(0, weight=1)
resultsFrame.grid_rowconfigure(2, weight=1)

#===================================================================================================

# hide the other frames
probeFrame.grid_remove()
cameraFrame.grid_remove()
logsFrame.grid_remove()
visionFrame.grid_remove()
volumeFrame.grid_remove()
resultsFrame.grid_remove()

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
