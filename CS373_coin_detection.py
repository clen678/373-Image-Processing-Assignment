# Built in packages
import math
import sys

# Matplotlib will need to be installed if it isn't already. This is the only package allowed for this base part of the 
# assignment.
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

# import our basic, light-weight png reader library
import imageIO.png

# Define constant and global variables
TEST_MODE = False    # Please, DO NOT change this variable!

def readRGBImageToSeparatePixelArrays(input_filename):
    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value
def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):
    new_pixel_array = []
    for _ in range(image_height):
        new_row = []
        for _ in range(image_width):
            new_row.append(initValue)
        new_pixel_array.append(new_row)

    return new_pixel_array


###########################################
### You can add your own functions here ###
###########################################

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    # STUDENT CODE HERE
    for i in range(0,image_height):
        for j in range(0,image_width):
            greyscale_pixel_array[i][j] = round(0.299*pixel_array_r[i][j]+ 0.587*pixel_array_g[i][j] + 0.114*pixel_array_b[i][j])

    return greyscale_pixel_array

def normaliseImage(image, image_width, image_height):
    
    greyscale_pixel_array = image

    # get histogram frequency for q by flattening the greyscale pixel array
    q = []
    flattenedImage = [element for element2 in greyscale_pixel_array for element in element2]
    q = list(set(flattenedImage))

    # get histogram hq
    hq = []
    for b in (q):
        hq.append(flattenedImage.count(b))
        
    # get cumulative histogram cq
    cum = []
    for b in range(0,len(hq)):
        if b==0:
            cum.append(hq[0])
        else:
            cum.append(cum[b-1] + hq[b])

    numPixels = image_width*image_height;
    alpha = 0.05*numPixels
    beta = 0.95*numPixels

    #find cq and then qAlpha
    for i in range(0,len(cum)):
        if cum[i] > alpha and cum[i-1] < alpha:
            qAlpha = q[i+1]
            break

    #find cq and then qBeta
    for i in range(0,len(cum)):
        if cum[i] < beta and cum[i+1] >= beta:
            qBeta = q[i]
            break

    #calculate image value
    for i in range(0,image_height):
        for j in range(0,image_width):
            imageValue = (255/(qBeta-qAlpha))*(greyscale_pixel_array[i][j]-qAlpha)
            greyscale_pixel_array[i][j] = round(max(0, min(255, imageValue)))

    return greyscale_pixel_array

def sharrFilter(image, image_width, image_height):
    
    sharrX = [[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]]
    sharrY = [[-3, -10, -3], [0, 0, 0], [3, 10, 3]]

    # create a new image array to store the sharr filter result
    newImage = createInitializedGreyscalePixelArray(image_width, image_height)
    newImage2 = createInitializedGreyscalePixelArray(image_width, image_height)

    # apply sharrX filter
    for i in range(0, image_height):
        for j in range(0, image_width):
            if i-1 < 0 or i+1 >= image_height or j-1 < 0 or j+1 >= image_width:
                newImage[i][j] = 0
            else:
                newImage[i][j] = (sharrX[0][0]*image[i-1][j-1] + sharrX[0][1]*image[i-1][j] + sharrX[0][2]*image[i-1][j+1] + sharrX[1][0]*image[i][j-1] + sharrX[1][1]*image[i][j] + sharrX[1][2]*image[i][j+1] + sharrX[2][0]*image[i+1][j-1] + sharrX[2][1]*image[i+1][j] + sharrX[2][2]*image[i+1][j+1])/32

    # apply sharrY filter
    for i in range(0, image_height):
        for j in range(0, image_width):
            if i-1 < 0 or i+1 >= image_height or j-1 < 0 or j+1 >= image_width:
                newImage2[i][j] = 0
            else:
                newImage2[i][j] = -(sharrY[0][0]*image[i-1][j-1] + sharrY[0][1]*image[i-1][j] + sharrY[0][2]*image[i-1][j+1] + sharrY[1][0]*image[i][j-1] + sharrY[1][1]*image[i][j] + sharrY[1][2]*image[i][j+1] + sharrY[2][0]*image[i+1][j-1] + sharrY[2][1]*image[i+1][j] + sharrY[2][2]*image[i+1][j+1])/32            

    # combine the two sharr filters
    for i in range(1, image_height-1):
        for j in range(1, image_width-1):
            newImage2[i][j] = abs(newImage[i][j]) + abs(newImage2[i][j])
    
    return newImage2

def blurImage(image, image_width, image_height):

    blurred = []
    
    #apply 5x5 mean blur filter ignoring borders    
    for i in range(0, image_height):
        temp = []
        for j in range(0, image_width):
            if i+2 >= image_height or j+2 >= image_width or j-2 < 0 or i-2 < 0:
                temp.append(0)
            else:
                sum = image[i-2][j-2] + image[i-2][j-1] + image[i-2][j] + image[i-2][j+1] + image[i-2][j+2] + image[i-1][j-2] + image[i-1][j-1] + image[i-1][j] + image[i-1][j+1] + image[i-1][j+2] + image[i][j-2] + image[i][j-1] + image[i][j] + image[i][j+1] + image[i][j+2] + image[i+1][j-2] + image[i+1][j-1] + image[i+1][j] + image[i+1][j+1] + image[i+1][j+2] + image[i+2][j-2] + image[i+2][j-1] + image[i+2][j] + image[i+2][j+1] + image[i+2][j+2]
                temp.append(round(sum/25))
        blurred.append(temp)
    
    # taking absolute value of the blurred image
    for i in range(0, image_height):
        for j in range(0, image_width):
            blurred[i][j] = abs(blurred[i][j])
    
    # ////////////////////////////////////// TESTING PURPOSES ///////////////////////////////////////////////////////////
    # generate the equalised histogram for new q
    # qEqualised1 = []
    # imageFlattened1 = [item for sublist in blurred for item in sublist]
    # qEqualised1 = list(set(imageFlattened1))

    # # get histogram hq
    # hqEqualised1 = []
    # for b in (qEqualised1):
    #     hqEqualised1.append(imageFlattened1.count(b))

    # # get cumulative histogram cq
    # cumEqualised1 = []
    # for b in range(0,len(hqEqualised1)):
    #     if b==0:
    #         cumEqualised1.append(hqEqualised1[0])
    #     else:
    #         cumEqualised1.append(cumEqualised1[b-1] + hqEqualised1[b])

    # plt.bar(range(len(hqEqualised1)), hqEqualised1)
    # plt.xlabel('Bin')
    # plt.ylabel('Frequency')
    # plt.title('Histogram')
    # plt.show()
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
    return blurred

def thresholdImage(image, image_width, image_height):
    
    for i in range(0, image_height):
        for j in range(0, image_width):
            if image[i][j] < 22:
                image[i][j] = 0
            else:
                image[i][j] = 255
    
    return image

def dilateImage(pixel_array, image_width, image_height):
    padding = createInitializedGreyscalePixelArray(image_width+4, image_height+4)
    padded = createInitializedGreyscalePixelArray(image_width+4, image_height+4)
    depadded = createInitializedGreyscalePixelArray(image_width, image_height)

    kernel = [[0, 0, 1, 0, 0],
              [0, 1, 1, 1, 0],
              [1, 1, 1, 1, 1],
              [0, 1, 1, 1, 0],
              [0, 0, 1, 0, 0]]
    
    # adding borderZeroPadding
    for i in range(0, image_height):
        for j in range(0, image_width):
            padding[i+2][j+2] = pixel_array[i][j]
    
    #dilate the image
    for i in range(2, image_height+2):
        for j in range(2, image_width+2):
            #if kernel hits in the image
            if padding[i-2][j] >=1 or padding[i-1][j-1] >=1 or padding[i-1][j] >=1 or padding[i-1][j+1] >=1 or padding[i][j-2] >=1 or padding[i][j-1] >=1 or padding[i][j] >=1 or padding[i][j+1] >=1 or padding[i][j+2] >=1 or padding[i+1][j-1] >=1 or padding[i+1][j] >=1 or padding[i+1][j+1] >=1 or padding[i+2][j] >=1:
                # 5x5 around i j is set to 255
                padded[i-2][j-2] = 255
                padded[i-2][j-1] = 255
                padded[i-2][j] = 255
                padded[i-2][j+1] = 255
                padded[i-2][j+2] = 255
                padded[i-1][j-2] = 255
                padded[i-1][j-1] = 255
                padded[i-1][j] = 255
                padded[i-1][j+1] = 255
                padded[i-1][j+2] = 255
                padded[i][j-2] = 255
                padded[i][j-1] = 255
                padded[i][j] = 255
                padded[i][j+1] = 255
                padded[i][j+2] = 255
                padded[i+1][j-2] = 255
                padded[i+1][j-1] = 255
                padded[i+1][j] = 255
                padded[i+1][j+1] = 255
                padded[i+1][j+2] = 255
                padded[i+2][j-2] = 255
                padded[i+2][j-1] = 255
                padded[i+2][j] = 255
                padded[i+2][j+1] = 255
                padded[i+2][j+2] = 255
                
    #removing borderZeroPadding
    for i in range(0, image_height):
        for j in range(0, image_width):
            depadded[i][j] = padded[i+2][j+2]
       
    return depadded

def erodeImage(pixel_array, image_width, image_height):
    padding = createInitializedGreyscalePixelArray(image_width+4, image_height+4)
    paddedErosion = createInitializedGreyscalePixelArray(image_width+4, image_height+4)
    depadded = createInitializedGreyscalePixelArray(image_width, image_height)
    
    # adding borderZeroPadding
    for i in range(0, image_height):
        for j in range(0, image_width):
            padding[i+2][j+2] = pixel_array[i][j]
    
    #dilate the image
    for i in range(2, image_height+2):
        for j in range(2, image_width+2):
            #if kernel hits in the image
            if padding[i-2][j] >=1 and padding[i-1][j-1] >=1 and padding[i-1][j] >=1 and padding[i-1][j+1] >=1 and padding[i][j-2] >=1 and padding[i][j-1] >=1 and padding[i][j] >=1 and padding[i][j+1] >=1 and padding[i][j+2] >=1 and padding[i+1][j-1] >=1 and padding[i+1][j] >=1 and padding[i+1][j+1] >=1 and padding[i+2][j] >=1:
                paddedErosion[i][j] = 255
                
    #removing borderZeroPadding
    for i in range(0, image_height):
        for j in range(0, image_width):
            depadded[i][j] = paddedErosion[i+2][j+2]
                
    return depadded

def connectedComponents(image, image_width, image_height):

    labels = createInitializedGreyscalePixelArray(image_width, image_height)
    seen = createInitializedGreyscalePixelArray(image_width, image_height)
    label = 1

    for i in range(0, image_height):
        for j in range(0, image_width):

            # if pixel is not object and not seen
            if image[i][j] != 0 and seen[i][j] == 0:
                q = []
                q.append((i, j))

                while len(q) > 0:
                    (row, cols) = q.pop()
                    labels[row][cols] = label
                    seen[row][cols] = 1

                    if cols+1 < image_width and row+1 < image_height:
                        # check if the pixel is object and not seen and add to queue
                        if seen[row][cols+1] == 0 and image[row][cols+1] != 0:
                            q.append((row, cols+1))
                            seen[row][cols+1] = 1

                        if seen[row-1][cols] == 0 and image[row-1][cols] != 0 and row-1 >= 0:
                            q.append((row-1, cols))
                            seen[row-1][cols] = 1

                        if seen[row][cols-1] == 0 and image[row][cols-1] != 0 and cols >= 0:
                            q.append((row, cols-1))
                            seen[row][cols-1] = 1

                        if seen[row+1][cols] == 0 and image[row+1][cols] != 0:
                            q.append((row+1, cols))
                            seen[row+1][cols] = 1

                label = label + 1

                # get list of different labels generated from the image
                uniqueLabels = []
                for i in range(0, image_height):
                    for j in range(0, image_width):
                        if labels[i][j] not in uniqueLabels:
                            uniqueLabels.append(labels[i][j])

                uniqueLabels.remove(0)
                
    return labels, uniqueLabels
    

def findBoundingboxLimits(labels, image_width, image_height, object_labels):
    boundingBoxLimits = []

    # for the amount of objects in the image, get bounding box values
    for objects in range(0, len(object_labels)):

        limits = [0, 0, 0, 0]
        x = []
        y = []

        # find min and max x and y values for each object
        for i in range(0, image_height):
            for j in range(0, image_width):
                if labels[i][j] == object_labels[objects]:
                    x.append(j)
                    y.append(i)
        limits[0] = min(x)
        limits[1] = min(y)
        limits[2] = max(x)
        limits[3] = max(y)
        boundingBoxLimits.append(limits)

    return boundingBoxLimits


# This is our code skeleton that performs the coin detection.
def main(input_path, output_path):
    # This is the default input image, you may change the 'image_name' variable to test other images.
    image_name = 'easy_case_6'
    input_filename = f'./Images/easy/{image_name}.png'

    if TEST_MODE:
        input_filename = input_path

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(input_filename)
    # computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)



    
    ###################################
    ### STUDENT IMPLEMENTATION Here ###
    ###################################
    
    
    
    
    
    
    
    
    
    ############################################
    ### Bounding box coordinates information ###
    ### bounding_box[0] = min x
    ### bounding_box[1] = min y
    ### bounding_box[2] = max x
    ### bounding_box[3] = max y
    ############################################
    
    # bounding_box_list = [[150, 140, 200, 190]]  # This is a dummy bounding box list, please comment it out when testing your own code.
    greyscaled = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    normalised = normaliseImage(greyscaled, image_width, image_height)
    sharred = sharrFilter(normalised, image_width, image_height)
    blurred = blurImage(sharred, image_width, image_height)
    blurred2 = blurImage(blurred, image_width, image_height)
    blurred3 = blurImage(blurred2, image_width, image_height)
    thresholded = thresholdImage(blurred3, image_width, image_height)
    dilated = dilateImage(thresholded, image_width, image_height)
    dilated2 = dilateImage(dilated, image_width, image_height)
    eroded = erodeImage(dilated2, image_width, image_height)
    eroded2 = erodeImage(eroded, image_width, image_height)
    eroded3 = erodeImage(eroded2, image_width, image_height)
    eroded4 = erodeImage(eroded3, image_width, image_height)
    labels, uniqueLabels = connectedComponents(eroded4, image_width, image_height)
    bounding_box_list = findBoundingboxLimits(labels, image_width, image_height, uniqueLabels)

    px_array = labels
    px_array = pyplot.imread(input_filename)
    
    fig, axs = pyplot.subplots(1, 1)
    axs.imshow(px_array, aspect='equal')
    
    # Loop through all bounding boxes
    for bounding_box in bounding_box_list:
        bbox_min_x = bounding_box[0]
        bbox_min_y = bounding_box[1]
        bbox_max_x = bounding_box[2]
        bbox_max_y = bounding_box[3]
        
        bbox_xy = (bbox_min_x, bbox_min_y)
        bbox_width = bbox_max_x - bbox_min_x
        bbox_height = bbox_max_y - bbox_min_y
        rect = Rectangle(bbox_xy, bbox_width, bbox_height, linewidth=2, edgecolor='r', facecolor='none')
        axs.add_patch(rect)
        
    pyplot.axis('off')
    pyplot.tight_layout()
    default_output_path = f'./output_images/{image_name}_with_bbox.png'
    if not TEST_MODE:
        # Saving output image to the above directory
        pyplot.savefig(default_output_path, bbox_inches='tight', pad_inches=0)
        
        # Show image with bounding box on the screen
        pyplot.imshow(px_array, cmap='gray', aspect='equal')
        pyplot.show()
    else:
        # Please, DO NOT change this code block!
        pyplot.savefig(output_path, bbox_inches='tight', pad_inches=0)



if __name__ == "__main__":
    num_of_args = len(sys.argv) - 1
    
    input_path = None
    output_path = None
    if num_of_args > 0:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        TEST_MODE = True
    
    main(input_path, output_path)
    