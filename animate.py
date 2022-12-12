import json
from PIL import Image, ImageDraw
from moviepy.editor import ImageSequenceClip
import numpy as np
import cv2
import os

# Load the data from the JSON file
with open("graffitiwall.json", "r") as f:
    data = json.load(f)

image_size = 1000
pixel_size = 4

limit_min_x = 60
limit_max_x = 90
limit_min_y = 30
limit_max_y = 50

pixel_min_x = image_size
pixel_max_x = 0
pixel_min_y = image_size
pixel_max_y = 0

background_color = (255, 255, 255)
highlight_color = (255, 0, 0)

validators = []

# Create a pixel image
output_size = (
    (limit_max_x - limit_min_x) * pixel_size,
    (limit_max_y - limit_min_y) * pixel_size
)
img = Image.new("RGB", output_size, background_color)

output_file = "output.mp4"
video_fps = 15
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_file, fourcc, video_fps, output_size)

first_step = True

def is_inside_limits(item):
    return item["x"] >= limit_min_x and item["x"] <= limit_max_x and item["y"] >= limit_min_y and item["y"] <= limit_max_y

for index, item in enumerate(data["data"]):
    # Get the coordinates of the point to be placed on the image
    x = int(item["x"])
    y = int(item["y"])

    if is_inside_limits(item):

        # append item to validators
        validators.append(item)

        if x < pixel_min_x:
            pixel_min_x = x

        if x > pixel_max_x:
            pixel_max_x = x

        if y < pixel_min_y:
            pixel_min_y = y

        if y > pixel_max_y:
            pixel_max_y = y

        data = np.array(img)
        img = Image.fromarray(data, mode='RGB')

        # Get the drawing context for the image
        draw = ImageDraw.Draw(img)

        # Draw a pixel_size red square at position
        position = (
            (x - limit_min_x) * pixel_size,
            (y - limit_min_y) * pixel_size,
            (x - limit_min_x) * pixel_size + pixel_size,
            (y - limit_min_y) * pixel_size + pixel_size
        )
        draw.rectangle(position, fill=highlight_color)

        open_cv_image = np.array(img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        out.write(open_cv_image)

        color = tuple(int(item["color"][i:i+2], 16) for i in (0, 2, 4))
        draw.rectangle(position, fill=color)

        open_cv_image = np.array(img)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        out.write(open_cv_image)

print("pixels: {validators}".format(validators=len(validators)))
print("unique validators: {unique_validators}".format(unique_validators=len(set([item["validator"] for item in validators]))))
print("validator list: {item_validator_list}".format(item_validator_list=set([item["validator"] for item in validators])))

out.release()
