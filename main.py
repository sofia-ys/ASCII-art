''' Load an image from file and print as ASCII art to the screen! '''
import numpy as np
import pygame as pg
   
#pre-calculated values:

#dimensions of a single, fixed-width character:
#(determined for Courier New: co
char_width = 12
char_height = 5
char_hw_ratio = char_height / char_width

#a list of characters that you can use in your ASCII art...
characters = ['M', 'W', 'Q', 'B', 'E', 'R', 'N', '@', 'H', 'q', 'p', 'g', 'K', 'A', '#', 'm', 'b', '8', '0', 'd', 'X', 'D', 'G', 'F', 'P', 'e', 'h', 'U', '9', '6', 'k', 'Z', '%', 'S', '4', 'O', 'x', 'y', 'T', '5', 'w', 'f', 'a', 'V', 's',
                '2', 'L', '$', 'Y', '&', 'n', '3', 'C', 'J', 'u', 'o', 'z', 'I', 'j', 'v', 'c', 'r', 't', 'l', 'i', '1', '=', '?', '7', '>', '<', ']', '[', '(', ')', '+', '*', ';', '}', '{', ':', '/', '\\', '!', '|', '_', ',', '^', '-', '~', '.', ' ']
characters = characters[::-1] #making the colours inverted lol because of the dark theme
n_characters = len(characters)

#... and the corresponding grayscale values
grayscale = np.array([217.56944444, 218.82291667, 219.89236111, 220.19444444,
                      222.14583333, 222.94097222, 223.0625, 223.17361111,
                      223.22222222, 223.23958333, 223.45486111, 223.60416667,
                      224.05208333, 224.09722222, 224.33333333, 225.25,
                      225.59722222, 225.62152778, 225.91666667, 225.96180556,
                      226.10763889, 226.74305556, 226.80208333, 227.04861111,
                      227.42361111, 228.45833333, 228.61458333, 228.73958333,
                      228.76736111, 228.80555556, 228.8125, 228.90625,
                      228.98611111, 229.06597222, 229.28472222, 229.61805556,
                      229.96527778, 230.07291667, 230.17361111, 230.21875,
                      230.60416667, 230.62847222, 230.84375, 231.03472222,
                      231.05555556, 231.46875, 231.55555556, 231.9375,
                      232.04861111, 232.07291667, 232.64583333, 232.68055556,
                      233.16319444, 233.53472222, 233.70138889, 234.20833333,
                      234.40625, 234.76388889, 234.93055556, 235.30208333,
                      235.36805556, 235.44791667, 235.5, 236.53472222,
                      237.32986111, 237.67361111, 237.70138889, 238.61458333,
                      238.61805556, 238.78125, 238.78472222, 238.79166667,
                      238.98611111, 239.07638889, 239.08680556, 239.97569444,
                      240.32291667, 240.78125, 241.50694444, 241.57291667,
                      242.25694444, 243.13194444, 243.18055556, 243.31944444,
                      244.30208333, 244.61805556, 245.03819444, 246.62847222,
                      247.58333333, 247.60763889, 248.62847222, 255.0])

#start writing your code here!

image = pg.image.load("grail.jpg") #importing the image as a pygame surface

imageRed = pg.surfarray.pixels_red(image) #getting the red rgb value as an array for each pixel in the image
imageGreen = pg.surfarray.pixels_green(image) 
imageBlue = pg.surfarray.pixels_blue(image)

imageGrey = [] #making an empty list for the greyscale values

for i in range(len(imageRed)): #for the index of every row in the length of imageRed (since it has the length of the whole list, could be blue or green though)
    greySublist = [] #creating a sublist to keep the row and column data (the fact that it's separated) from the array

    for j in range(len(imageRed[i])): #for each index in the column of imageRed
        greySublist.append((int(imageRed[i][j]) + int(imageBlue[i][j]) + int(imageGreen[i][j]))/3) #taking the average of the three pixel values and appending it to this sublist

    imageGrey.append(greySublist) #adding all the sublists made to the big greyscale list that i want so that it's a list of lists

patchWidth = 8 #allowing for adjustable resolution
patchHeight = int(patchWidth * char_hw_ratio) #determining patch height (also with adjustable resolution)

def computePatch(imageGrey,row,col): #creating a function for computing the average greyscale of a given patch
    patchSum = 0 #initialising

    for i in range(patchHeight): #i iterating between 0 and patchHeight value

        for j in range(patchWidth): #j iterating between 0 and patchWidth value
            patchSum = patchSum + imageGrey[row + i][col + j] #takes the sum of all the column values in the patchwidth of a certain row

    patchAvg = patchSum / (patchWidth * patchHeight) #takes the average
    return patchAvg


patchList = [] #creating an empty list for my patches which will have the rows be the same as the original imageGrey but just "compressed" kind of

for i in range(0,len(imageGrey),patchHeight): #for loop starting at 0, ending at the length of the number of rows imageGrey but skipping in intervals of patchWidth
    patchSublist = [] #empty list for the rows in the patchList (these will be essentially the same as the rows in the imageGrey just compressed)

    if i > (len(imageGrey)-patchHeight): #checking for the edges
        break

    for j in range(0,len(imageGrey[i]),patchWidth): #iterating over patchHeight
        if j > (len(imageGrey[i])-patchWidth): #checking for the edges (just ignoring them in the image)
            continue

        patchGrey = computePatch(imageGrey,i,j) #passing the variables needed for the function where i and j are the row and column (they get renamed in the function)
        patchSublist.append(patchGrey)

    patchList.append(patchSublist)

minValTab = [] #find min value in the patchList
for list in patchList:
    minVal = min(list)
    minValTab.append(minVal)
minVal = min(minValTab)

maxValTab = [] #find max value in the patchList
for list in patchList:
    maxVal = max(list)
    maxValTab.append(maxVal)
maxVal = max(maxValTab)

def charForValue(val, minVal, maxVal, charList):
    spacing = (maxVal - minVal) / (len(charList)-1) #calculating the range of grey values assigned to each character
    ind = int((val - minVal) / spacing) #normalising the value
    return charList[ind]

art = '' #creating an empty string for the art
for i in range(len(patchList[0])):

    for j in range(len(patchList)):
        val = charForValue(patchList[j][i], minVal, maxVal, characters) #finding the character for the patch, i and j are flipped to make sure the image is rotated lol
        art = art + val #adding the character 

    art = art + '\n' #making sure there's a new line with every new row 

print(art) #ascii art!!
