this python script will go through a folder and create a list that includes every image and some metadata
for that image

it will then go through each image and compare it to each other image by checking 20 random pixels from each image and seeing if they all match. if at any point it matches perfectly to another image then the current image is considered a duplicate, and the loop moves on. If an image goes through the rest of the list and doesnt find a duplicate, we copy that image to a new location

this keeps all original images untouched in their original folder while also only copying the last duplicate of each image into the new location

** NEED TO FIND OUT A WAY TO ENSURE PHOTO WITH MORE META DATA IS COPIED **