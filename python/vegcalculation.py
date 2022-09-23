# Imports
import cv2
import numpy as np

# Here, you define your target color as
# a tuple of three values: RGB
green = [110, 158, 80]

# You define an interval that covers the values
# in the tuple and are below and above them by 20
diff = 95

# Be aware that opencv loads image in BGR format,
# that's why the color values have been adjusted here:
boundaries = [([green[2], green[1]-diff, green[0]-diff],
               [green[2]+diff, green[1]+diff, green[0]+diff])]

np.seterr(invalid='ignore')
class VegetationCalculation:
    def getVegetationPercentage():
        # Read image
        img = cv2.imread("ndvi.png")
        # for each range in your boundary list:
        for (lower, upper) in boundaries:

            # You get the lower and upper part of the interval:
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)

            # cv2.inRange is used to binarize (i.e., render in white/black) an image
            # All the pixels that fall inside your interval [lower, uipper] will be white
            # All the pixels that do not fall inside this interval will
            # be rendered in black, for all three channels:
            mask = cv2.inRange(img, lower, upper)

            # Now, you AND the mask and the input image
            # All the pixels that are white in the mask will
            # survive the AND operation, all the black pixels
            # will remain black
            output = cv2.bitwise_and(img, img, mask=mask)

            cv2.imwrite("vegmask.png", removeBackground(output))

            # You can use the mask to count the number of white pixels.
            # Remember that the white pixels in the mask are those that
            # fall in your defined range, that is, every white pixel corresponds
            # to a green pixel. Divide by the image size and you got the
            # percentage of green pixels in the original image:
            ratio_green = cv2.countNonZero(mask)/(img.size)

            # This is the color percent calculation, considering the resize I did earlier.
            colorPercent = (ratio_green * 100) / 0.1

            # Print the color percent, use 2 figures past the decimal point
            return str(np.round(colorPercent, 2))


def removeBackground(image):
    tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Applying thresholding technique
    _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)

    # Using cv2.split() to split channels
    # of coloured image
    b, g, r = cv2.split(image)

    # Making list of Red, Green, Blue
    # Channels and alpha
    rgba = [b, g, r, alpha]

    # Using cv2.merge() to merge rgba
    # into a coloured/multi-channeled image
    dst = cv2.merge(rgba, 4)

    # Writing and saving to a new image
    return dst
