#!/bin/bash

# Direct URL to the image
API_URL="https://storage.googleapis.com/readbee-public-dev/flower-kitten.gif"

# Specify the path and filename for saving the image
IMAGE_FILE="/path/to/save/cat_image.gif" # Change extension to .gif to match the image type

# Use curl to download the cat image and save it to the specified file
curl -s "$API_URL" -o "$IMAGE_FILE"

echo "Cat image saved to $IMAGE_FILE"