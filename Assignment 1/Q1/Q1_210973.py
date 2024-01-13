import cv2
import numpy as np
# import matplotlib.pyplot as plt
def solution(image_path):
    # Load the input image
    image = cv2.imread(image_path)  # Replace with the path to your image

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper HSV values for the orange color
    lower_orange = np.array([10, 100, 100])  # Adjust these values as needed
    upper_orange = np.array([30, 255, 255])  # Adjust these values as needed

    # Create a binary mask for the orange color
    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

    m,n = orange_mask.shape
    top_left = np.sum(orange_mask.copy()[:m//2, :n//2])
    top_right = np.sum(orange_mask.copy()[:m//2,n//2:])
    bottom_right = np.sum(orange_mask.copy()[m//2:, n//2:])
    bottom_left = np.sum(orange_mask.copy()[:m//2,n//2:])


    flag_width = 600
    flag_height = 600
    flag = np.zeros((flag_height, flag_width, 3), dtype=np.uint8)

    # Define colors
    orange_color = (51, 153, 255)  # Orange in BGR format
    green_color = (0, 128, 0)     # Green in BGR format
    blue_color = (255, 0, 0)  # Blue in BGR format
    white_color = (255,255,255)

    # Fill the upper part of the flag with orange
    flag[:200, :] = orange_color

    flag[200:400, :] = white_color

    # Fill the lower part of the flag with green
    flag[400:, :] = green_color


    if (top_left == 0 and top_right == 0):
        # add bottom flag
        flag = cv2.rotate(flag,cv2.ROTATE_180)
        # Calculate the center of the flag
        # correct_flag = flag
    elif (top_left == 0 and bottom_left == 0):
        flag = cv2.rotate(flag,cv2.ROTATE_90_CLOCKWISE)
        # add right flag
        # correct_flag = 
    elif (top_right == 0 and bottom_right == 0):
        # add left flag
        flag = cv2.rotate(flag,cv2.ROTATE_90_COUNTERCLOCKWISE)
        # correct_flag = 
    elif (bottom_left == 0 and bottom_right == 0):
        pass
        # add top flag
        # correct_flag = 

    center_x = flag_width // 2
    center_y = flag_height // 2

    # Draw the blue circle in the center
    cv2.circle(flag, (center_x, center_y), 100, blue_color, thickness=2)

    # Draw the spokes (lines) of the chakra (circle)
    for angle in range(0, 360, 15):
        angle_rad = np.deg2rad(angle)
        x1 = int(center_x + 0 * np.cos(angle_rad))  # Inner circle radius = 90
        y1 = int(center_y + 0 * np.sin(angle_rad))
        x2 = int(center_x + 100 * np.cos(angle_rad))  # Outer circle radius = 100
        y2 = int(center_y + 100 * np.sin(angle_rad))
        cv2.line(flag, (x1, y1), (x2, y2), blue_color, thickness=1)
    # return correct_flag

    return flag