#!/usr/bin/env python
import os
import cv2
import numpy as np
from plantcv import plantcv as pcv
import argparse


def options():
    parser = argparse.ArgumentParser(description="Imaging processing with PlantCV.")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-r","--result", help="Result file.", required= True )
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-w","--writeimg", help="Write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.")
    args = parser.parse_args()
    return args


def main():
    # Create input arguments object
    args = options()

    # Set debug mode
    pcv.params.debug = args.debug

    # Open a single image
    img, imgpath, imgname = pcv.readimage(filename=args.image)

    # Visualize colorspaces
    all_cs = pcv.visualize.colorspaces(rgb_img=img)

    # Extract the Blue-Yellow ("b") channel from the LAB colorspace
    gray_img = pcv.rgb2gray_lab(rgb_img=img, channel="b")

    # Plot a histogram of pixel values for the Blue-Yellow ("b") channel.
    hist_plot = pcv.visualize.histogram(gray_img=gray_img)

    # Apply a binary threshold to the Blue-Yellow ("b") grayscale image.
    thresh_img = pcv.threshold.binary(gray_img=gray_img, threshold=140, 
                                      max_value=255, object_type="light")

    # Apply a dilation with a 5x5 kernel and 3 iterations
    dil_img = pcv.dilate(gray_img=thresh_img, ksize=5, i=3)

    # Fill in small holes in the leaves
    closed_img = pcv.fill_holes(bin_img=dil_img)

    # Erode the plant pixels using a 5x5 kernel and 3 iterations
    er_img = pcv.erode(gray_img=closed_img, ksize=5, i=3)

    # Apply a Gaussian blur with a 5 x 5 kernel.
    blur_img = pcv.gaussian_blur(img=er_img, ksize=(5, 5))

    # Set pixel values less than 255 to 0
    blur_img[np.where(blur_img < 255)] = 0

    # Fill/remove objects less than 300 pixels in area
    cleaned = pcv.fill(bin_img=blur_img, size=300)

    # Create a circular ROI
    roi, roi_str = pcv.roi.circle(img=img, x=1725, y=1155, r=400)

    # Identify objects in the binary image
    cnts, cnts_str = pcv.find_objects(img=img, mask=cleaned)

    # Filter objects by region of interest
    plant_cnt, plant_str, plant_mask, plant_area = pcv.roi_objects(img=img, roi_contour=roi, 
                                                                   roi_hierarchy=roi_str,
                                                                   object_contour=cnts, 
                                                                   obj_hierarchy=cnts_str)

    # Combine objects into one
    plant, mask = pcv.object_composition(img=img, contours=plant_cnt, hierarchy=plant_str)

    # Measure size and shape properties
    shape_img = pcv.analyze_object(img=img, obj=plant, mask=mask)
    if args.writeimg:
        pcv.print_image(img=shape_img, filename=os.path.join(args.outdir, "shapes_" + imgname))

    # Analyze color properties
    color_img = pcv.analyze_color(rgb_img=img, mask=mask, hist_plot_type="hsv")
    if args.writeimg:
        pcv.print_image(img=color_img, filename=os.path.join(args.outdir, "histogram_" + imgname))

    # Save the measurements to a file
    pcv.print_results(filename=args.result)

if __name__ == '__main__':
    main()
