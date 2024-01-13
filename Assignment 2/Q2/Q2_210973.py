import cv2
import numpy as np


def bilateral_filter(image, d, sigma_color, sigma_space):
    height, width = image.shape[:2]

    # Create an output image with the same shape as the input, but single channel
    output = np.zeros_like(image[:, :, 0], dtype=np.float64)

    for i in range(height):
        for j in range(width):
            i_min = max(0, i - d)
            i_max = min(height - 1, i + d)
            j_min = max(0, j - d)
            j_max = min(width - 1, j + d)

            # Extract the local region of interest
            patch = image[i_min:i_max + 1, j_min:j_max + 1].astype(np.float64)

            # Compute Gaussian weights based on intensity differences
            intensity_diff = patch - image[i, j]
            intensity_weights = np.exp(-(intensity_diff**2) / (2 * sigma_color**2))

            # Compute Gaussian weights based on spatial differences
            spatial_diff_i, spatial_diff_j = np.meshgrid(np.arange(i_min, i_max + 1) - i, np.arange(j_min, j_max + 1) - j)
            spatial_diff_i = spatial_diff_i.T  # Transpose spatial_diff_i
            spatial_diff_j = spatial_diff_j.T  # Transpose spatial_diff_j
            spatial_distances = np.sqrt(spatial_diff_i**2 + spatial_diff_j**2)
            spatial_weights = np.exp(-(spatial_distances**2) / (2 * sigma_space**2))

            # Combine intensity and spatial weights
            bilateral_weights = intensity_weights * spatial_weights[:,:,np.newaxis]

            # Normalize weights and apply to the pixel
            normalized_weights = bilateral_weights / np.sum(bilateral_weights)
            output[i, j] = np.sum(patch * normalized_weights)

    return output.astype(np.uint8)





def fuse_flash_images_bilateral(image_with_flash, image_without_flash, alpha=0.5):
    # Resize images to ensure they have the same dimensions
    image_with_flash = cv2.resize(image_with_flash, (640, 480))
    image_without_flash = cv2.resize(image_without_flash, (640, 480))

    # Apply bilateral filter to both images
    sigma_color = 30
    sigma_space = 30
    filtered_image_with_flash = bilateral_filter(image_with_flash, 9 , sigma_color, sigma_space)
    filtered_image_without_flash = bilateral_filter(image_without_flash, 9 , sigma_color, sigma_space)

    # Combine the two filtered images using element-wise maximum
#     combined_image = np.maximum(filtered_image_with_flash, filtered_image_without_flash)

    # Combine images using a weighted sum
    fused_image = cv2.addWeighted(filtered_image_with_flash, alpha, filtered_image_without_flash, 1 - alpha, 0)

    return fused_image

# Example usage

def solution(image_path_wf , image_path_f):
    image_with_flash = cv2.imread(image_path_f)
    image_without_flash = cv2.imread(image_path_wf)
    
    cv2.imshow('hello' , image_with_flash)
    cv2.imshow('hello1' , image_without_flash)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    fused_image_bilateral = fuse_flash_images_bilateral(image_with_flash, image_without_flash, alpha=0.5)
    
    return fused_image_bilateral
