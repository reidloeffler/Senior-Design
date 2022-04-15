#from __future__ import print_function
from google.cloud import vision

image_uri = 'https://th-thumbnailer.cdn-si-edu.com/4Nq8HbTKgX6djk07DqHqRsRuFq0=/1000x750/filters:no_upscale()/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/d5/24/d5243019-e0fc-4b3c-8cdb-48e22f38bff2/istock-183380744.jpg'

client = vision.ImageAnnotatorClient()

#remote image
image = vision.Image()
image.source.image_uri = image_uri

"""
#local image
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
"""

response = client.label_detection(image=image)

print('Labels (and confidence score):')
print('=' * 30)
for label in response.label_annotations:
    print(label.description, '(%.2f%%)' % (label.score*100.))

if response.error.message:
    raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))
