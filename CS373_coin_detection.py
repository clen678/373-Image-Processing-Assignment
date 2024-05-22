# Built in packages
import math
import sys

# Matplotlib will need to be installed if it isn't already. This is the only package allowed for this base part of the 
# assignment.
from matplotlib import pyplot
from matplotlib.patches import Rectangle

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
    imageFlattened = [item for sublist in greyscale_pixel_array for item in sublist]
    q = list(set(imageFlattened))

    # get histogram hq
    hq = []
    for b in (q):
        hq.append(imageFlattened.count(b))
        
    # get cumulative histogram cq
    cum = []
    for b in range(0,len(hq)):
        if b==0:
            cum.append(hq[0])
        else:
            cum.append(cum[b-1] + hq[b])
    
    print(image_height*image_width)
    print("q", q)
    print("hq", hq)
    print("cum", cum)

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
            greyscale_pixel_array[i][j] = max(0, min(255, imageValue))

    # ========================================================================================================
    # EXTENSION: Histogram Equalisation
    te = []
    cMin = cum[0]
    cMax = cum[len(cum)-1]

    for i in range(0,len(cum)):
        
        value = round( 255*((cum[i]-cMin)/(cMax-cMin)) )
        
        te.append(value)

    #calculate image value for equalisation
    # for i in range(0,image_height):
    #     for j in range(0,image_width):
    #         imageValue = (255/(qBeta-qAlpha))*(greyscale_pixel_array[i][j]-qAlpha)
    #         greyscale_pixel_array[i][j] = max(0, min(255, imageValue))
    # ========================================================================================================

    return greyscale_pixel_array

def HistogramEqualisation(cum):
    t = []

    for i in range(0,len(cum)):
        
        value = round( 255*((cum[i]-cum[0])/(cum[len(cum)]-cum[0])) )
        
        t.append(value)

    return t






# This is our code skeleton that performs the coin detection.
def main(input_path, output_path):
    # This is the default input image, you may change the 'image_name' variable to test other images.
    image_name = 'easy_case_1'
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
    
    bounding_box_list = [[150, 140, 200, 190]]  # This is a dummy bounding box list, please comment it out when testing your own code.
    px_array = normaliseImage(computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height), image_width, image_height)
    
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
    