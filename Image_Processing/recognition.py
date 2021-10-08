# Testing individual detect.py, Vanessa Silbar
import os
import cv2
import torch
import time

# Take a picture

#videoCaptureObject = cv2.VideoCapture(0)
#result = True
#while(result):
#    ret,frame = videoCaptureObject.read()
#    cv2.imwrite("NewPicture.jpg",frame)
#    result = False
#videoCaptureObject.release()
#cv2.destroyAllWindows()

#Use webcam

capture = cv2.VideoCapture(0)
result = True

frame_width = int(capture.get(3))
frame_height = int(capture.get(4))

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

while(result):
    ret, frame = capture.read()
    out.write(frame)
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
capture.release()

cv2.destroyAllWindows()


# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Images
# imgs = r'C:\Users\00vsi\Documents\yolov5\NewPicture.jpg'  # batch of images
imgs = os.path.join(os.getcwd(), 'NewPicture.jpg')

# Inference
results = model(frame)

# Results
results.print()
results.save()  # or .save()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)
