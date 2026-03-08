import cv2
import os
import numpy as np
from test1_module import test1  # Ensure this import is correct
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def rgb2gray(rgb):
    return 0.2989 * rgb[:, :, 0] + 0.5870 * rgb[:, :, 1] + 0.1140 * rgb[:, :, 2]


def process_image(image_path, sigma=1.4, kernel_size=5, lowthreshold=0.09, highthreshold=0.20, weak_pixel=100):
    print(f"Processing image: {image_path}")

    # Read image
    img = mpimg.imread(image_path)
    img_gray = rgb2gray(img)
    print(f"Image converted to grayscale. Shape: {img_gray.shape}")

    # Initialize test1 class and detect edges
    t = test1([img_gray], sigma=sigma, kernel_size=kernel_size, lowthreshold=lowthreshold, highthreshold=highthreshold,
              weak_pixel=weak_pixel)
    processed_imgs = t.detect()

    if processed_imgs is None or len(processed_imgs) == 0:
        print("Error: No processed images returned.")
        return None

    # Save processed images
    output_path = f"gray/{os.path.basename(image_path)}"
    print(f"Saving processed image to: {output_path}")

    # Handling multiple processed images (if any)
    for processed_img in processed_imgs:
        if processed_img.shape[0] == 3:
            processed_img = processed_img.transpose(1, 2, 0)

        # Ensure output directory exists
        if not os.path.exists("gray"):
            os.makedirs("gray")

        cv2.imwrite(output_path, processed_img)

    return output_path


def count_white_pixels(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    white_pixels = np.sum(img == 255)
    return white_pixels


def main():
    if not os.path.exists('gray'):
        os.makedirs('gray')

    img_paths = ['images/D.png', 'images/refrence.png']  # Add other image paths as necessary
    white_pixel_counts = {}

    for img_path in img_paths:
        processed_img_path = process_image(img_path)
        if processed_img_path:
            white_pixels = count_white_pixels(processed_img_path)
            white_pixel_counts[img_path] = white_pixels
            print(f"White pixels in {img_path}: {white_pixels}")

    # Calculate percentage of white pixels
    if len(white_pixel_counts) == 2:
        pixel1 = white_pixel_counts['images/D.png']
        pixel2 = white_pixel_counts['images/refrence.png']
        avg = (pixel1 / pixel2) * 100
        print(f"Percentage of white pixels (D.png to refrence.png): {avg}%")


if __name__ == "__main__":
    main()
