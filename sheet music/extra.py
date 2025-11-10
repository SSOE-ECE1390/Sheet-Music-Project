import cv2
import os
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt

# THIS IS A BUNCH OF EXTRA CODE. PLEASE IGNORE.

# Remove line Second method (RLE)
rle = list()
for y in range(0,img.shape[1]):
    count = 1
    n = 0
    rle_in = list()
    for x in range(1,img.shape[0]):
        if(img[x][y] == img[x-1][y]):
            count+=1
        else :
            rle_in.append(count)
            count = 1
    rle_in.append(count)
    rle.append(np.array(rle_in))
rle = np.array(rle, dtype=object)
img3 = np.copy(img)
for i in range(img.shape[1]):
    for j in range(1,len(rle[i]),2):
        if rle[i][j] < 4:
            s = sum(rle[i][:j+1])
            img3[s - rle[i][j] - 1:s, i] = True
show_images([img, img3], ["Original Note", "Note Line Removed (img3)"])

# --------------------------------------------------------


# --- Part 2: Staff Line Removal using Morphology (using Sheet Music Example 1.png) ---
img = cv2.imread('C:/Users/isabe/Documents/GitHub/Sheet-Music-Project/sheet music/Sheet Music Example 1.png',cv2.IMREAD_GRAYSCALE)
img_inv = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 8)
# Replaced debug_print(img_inv) with nothing
img_inv = 1 - (img_inv // 255) # Convert to 0/1 (white on black)
# show_images([img_inv], ["Inverted Binary"]) # Optional check

horizontal = np.uint8(np.copy(img_inv))
vertical = np.uint8(np.copy(img_inv))

# Specify size on horizontal axis
cols = horizontal.shape[1]
horizontal_size = cols // 30

# Create structure element for extracting horizontal lines
horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

# Apply morphology to get horizontal lines (staff lines)
horizontal = cv2.erode(horizontal, horizontalStructure)
horizontal = cv2.dilate(horizontal, horizontalStructure)


# Specify size on vertical axis
rows = vertical.shape[0]
verticalsize = 4 

# Create structure element for extracting vertical lines
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))

# Apply morphology to get vertical lines (parts of symbols)
vertical = cv2.erode(vertical, verticalStructure)
vertical = cv2.dilate(vertical, verticalStructure)

# Replaced debug_show_images
show_images([img_inv, horizontal, vertical],["Original Binary","Staff lines (Horizontal)","Vertical Symbols (Vertical)"])

# Enhance Output
vertical = 1-vertical # Invert vertical back to black on white for Canny
final = np.copy(vertical)

# Step 1: Extract edges
edges = cv2.Canny(vertical,0.8,0.2)
show_images([edges], ["Canny Edges"]) # Replaced debug_show_images

# Step 2: Dilate edges
kernel = np.ones((2, 2), np.uint8)
edges = cv2.dilate(edges, kernel)
show_images([edges], ["Dilated Edges"]) # Replaced debug_show_images

# Step 3 & 4: Blur the smooth copy
smooth = np.copy(vertical)
smooth = cv2.blur(smooth, (2, 2))

# Step 5: Copy blurred smooth to vertical where edges are
(rows, cols) = np.where(edges != 0)
vertical[rows, cols] = smooth[rows, cols]

# Show final result
show_images([final, vertical],["Before Enhancement","After Enhancement"])