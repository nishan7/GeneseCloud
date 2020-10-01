import json
import boto3
from pprint import pprint
from PIL import Image, ImageDraw, ImageFont

ACCESS_KEY = 'ASIASYIVRRFRQXIDET3U'
SECRET_KEY = '5I5OnpS9ovZxamBR0F/AZnXb6r5SMGtZ3xR9gCyk'
SESSION_TOKEN = 'FwoGZXIvYXdzEF8aDJa9SnvCnajl6nLYcSLYAWR2HauAOvq788bsjYC/vJX8S9NOsiZYcSgLiqgi4SyxdRc/RAA5k/bHjbtpFWH7cBMfOmF3ekYzQbCwue5MZq5bb5t4uuAY9f9RY+mSOQEaSOOByAhtiZOVIW3vTBphuW5ekmtSHOPuFOkaEbJFtP9LRl87uzx7PANFh9OM3qXFC91Q4YJNT/GvZVhwwr5rmNKHL0ZOGIsuDpoHXWOi7zK/UUNw4xBfyYpkbw/QfNWR+9Yeou2k+FYX0p7VOTvXCRnUJQo6QJyW5OnoKd47L9CVH6tnDPJYPyjlq9f7BTItY/LqjdM60/fY2AUYkMypmcK3zwEo3A7hANl8Ib26cnjwBLEoSQY3b6yzS14p'

# Input photo link
photo = 'week4\\images\\5.jpg'


# Create a rectangular box in the image 
def box_image(boxes, photo):
    with Image.open(photo) as im:
        for idx, box in enumerate(boxes):
            draw = ImageDraw.Draw(im)
            top_left = box['Left']*im.size[0], box['Top']*im.size[1]
            bottom_right = (box['Left']+box['Width']) * \
                im.size[0], (box['Top']+box['Height'])*im.size[1]
            top_right = (box['Left']+box['Width']) * \
                im.size[0], (box['Top'])*im.size[1]
            bottom_left = (box['Left']) * \
                im.size[0], (box['Top']+box['Height'])*im.size[1]
            draw.line(top_left + top_right, fill=128, width=20)
            draw.line(top_right + bottom_right, fill=128, width=20)
            draw.line(bottom_right + bottom_left, fill=128, width=20)
            draw.line(bottom_left + top_left, fill=128, width=20)

            fnt = ImageFont.truetype("week4\\FreeMono.ttf", 140)
            # draw text, half opacity
            draw.text((top_left[0], top_left[1]*1.15),
                      "Face "+str(idx+1), font=fnt, fill=(255, 255, 255, 255))
        return im




# Sets up the boto3 for rekognition 
client = boto3.client('rekognition',
                      region_name='us-east-1',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY,
                      aws_session_token=SESSION_TOKEN
                      )
# Reads the input image and requestst the rekognition and receives the response
with open(photo, 'rb') as image:
    response = client.detect_faces(
        Image={'Bytes': image.read()}, Attributes=['ALL'])
    faces = response['FaceDetails']

# Iterate through every face and gather the output
all_faces_data = []
for face in faces:
    face_data = {}
    face_data['age_range'] = face['AgeRange']['Low'], face['AgeRange']['High']
    face_data['Eyeglasses'] = face['Eyeglasses']['Value']
    face_data['Sunglasses'] = face['Sunglasses']['Value']
    face_data['Beard'] = face['Beard']['Value']
    face_data['Mustache'] = face['Mustache']['Value']
    face_data['Emotions'] = [emotion['Type']
                             for emotion in face['Emotions'] if emotion['Confidence'] > 70]
    face_data['BoundingBox'] = face['BoundingBox']
    all_faces_data.append(face_data)

# Create a box in the input photo for faces and saves the resultant image
boxes = [face['BoundingBox'] for face in all_faces_data]
im = box_image(boxes, photo)
im.save(photo+'box.png', "PNG")

# Print the results
for n,face in enumerate(all_faces_data):
    print()
    print('This is Face {}'.format(n+1))
    print('Age Range: {} to {} years'.format(*face_data['age_range']))
    if face['Emotions']:
        print('This face has emotions as: ', ' '.join(face['Emotions']))
    if face['Sunglasses']:
         print('This person seems to be wearing Sunglasses')
    if face['Eyeglasses']:
        print('This person seems to be wearing Eyeglasses')
    if face['Beard']:
        print('This person seems to have a Beard')



