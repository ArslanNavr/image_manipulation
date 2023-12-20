from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.ndimage import zoom


# Rotates the given image by 90 degrees counterclockwise
def rotate_image(image):
    return np.rot90(image)


# Pads the image to the specified target height and width
def pad_image(image, target_height, target_width):
    pad_y = max(target_height - image.shape[0], 0)  # Calculate padding for height
    pad_x = max(target_width - image.shape[1], 0)  # Calculate padding for width
    return np.pad(image, [(0, pad_y), (0, pad_x), (0, 0)], mode='constant')


# Creates a tiled image by repeating the given image a specified number of times
def create_tiled_image(image, num_rows, num_cols):
    return np.tile(image, (num_rows, num_cols, 1))


# Flips the image horizontally
def create_flipped_image(image):
    return image[:, ::-1]


# Applies a color filter to the image, zeroing out channels not in the filter
def create_color_filtered_image(image, color_filter):
    filtered_image = image.copy()
    for i in range(3):  # Iterate over color channels
        if i not in color_filter:
            filtered_image[:, :, i] = 0  # Zero out the channel if not in the filter
    return filtered_image


# Enlarges the image by a given scale factor using zoom
def create_enlarged_image(image, scale):
    return zoom(image, (scale, scale, 1))


# Concatenates a list of images along a specified axis
def concatenate_images(images, axis):
    return np.concatenate(images, axis=axis)


# Changes specific pixels to red based on a color range, preserving the alpha channel
def create_red_shirt_image(image):
    lower_bound = np.array([75, 5, 225])  # Lower bound of the color range
    upper_bound = np.array([110, 45, 255])  # Upper bound of the color range

    # Create mask based on the color range
    mask = np.all(np.logical_and(lower_bound <= image[:, :, :3], image[:, :, :3] <= upper_bound), axis=-1)

    # Apply the mask and set the selected pixels to red
    image[mask] = [255, 0, 0, 255]  # Set red color, assuming alpha channel is unchanged
    return image


# Main function to process and display the images
def process_images(image_path):
    np_image = np.array(Image.open(image_path))  # Load image as a NumPy array

    # Perform various image manipulations
    np_image_tiled = create_tiled_image(np_image, 3, 8)
    flipped_img = create_flipped_image(np_image)
    basic_and_flipped_tiled_img = concatenate_images(
        [create_tiled_image(np_image, 1, 6), create_tiled_image(flipped_img, 1, 6)], axis=0)
    basic_and_flipped_tiled_img = create_tiled_image(basic_and_flipped_tiled_img, 2, 1)
    blue_line = create_tiled_image(create_color_filtered_image(np_image, [2]), 1, 4)
    red_column = create_tiled_image(create_color_filtered_image(np_image, [0]), 2, 1)
    green_line = create_tiled_image(create_color_filtered_image(np_image, [1]), 1, 4)
    big_line = concatenate_images([red_column, create_enlarged_image(np_image, 2), red_column], axis=1)
    total_image = concatenate_images([blue_line, big_line, green_line], axis=0)

    # Rotate and pad images to create a sequence
    rotating_images = [rotate_image(np_image) for _ in range(4)]
    max_height, max_width = max(img.shape[0] for img in rotating_images), max(img.shape[1] for img in rotating_images)
    padded_rotating_images = [pad_image(img, max_height, max_width) for img in rotating_images]
    rotating_image = concatenate_images(padded_rotating_images, axis=1)

    # Create an image with red shirt effect
    red_shirt = create_red_shirt_image(np_image.copy())

    # Display the processed images
    fig, ax = plt.subplots(5, 1, figsize=(20, 20))
    ax[0].imshow(np_image_tiled)
    ax[1].imshow(basic_and_flipped_tiled_img)
    ax[2].imshow(total_image)
    ax[3].imshow(rotating_image)
    ax[4].imshow(red_shirt)

    plt.show()


# Load and process the image
loc_input_img = os.path.join('..', '..', 'data', 'input', 'pickle.png')
process_images(loc_input_img)


#lets upload this shit and get it over with