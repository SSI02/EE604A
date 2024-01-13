import cv2
import numpy as np

def face_detection(cartoon_image):
    
    grayscale_image = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2GRAY)
    
    l,m =  grayscale_image.shape
    
    left_img = grayscale_image[:, :m // 2]
    right_img = grayscale_image[:, m // 2:]
    
    # cv2.imshow('hello' , left_img)
    # cv2.imshow('hello1' , right_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_alt.xml')
    
    detected_faces = face_cascade.detectMultiScale(grayscale_image)
    detected_faces_left = face_cascade.detectMultiScale(left_img)
    detected_faces_right = face_cascade.detectMultiScale(right_img)
    
    
    for (x, y, w, h) in detected_faces:
        cv2.rectangle(cartoon_image,(x, y),(x + w, y + h),( 0, 0, 255 ),2)
        
    cv2.imshow('hello', cartoon_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return len(detected_faces_left), len(detected_faces_right), len(detected_faces)



def solution(image_path):
    
    image = cv2.imread(image_path)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to create a blurred version
    blurred = cv2.GaussianBlur(gray, (0, 0), 6)

# Calculate the Unsharp Mask by subtracting the blurred image from the original
    unsharp_mask = cv2.addWeighted(gray, 1.5, blurred, -0.7, 0)

# Convert back to BGR if needed
    sharp_img = cv2.cvtColor(unsharp_mask, cv2.COLOR_GRAY2BGR)
    
    # sharp_img = cv2.bilateralFilter(sharp_img, d=9, sigmaColor=75, sigmaSpace=75)
    
    # kernel = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])

    # image = cv2.filter2D(sharp_img, -1, kernel)
    
    l , r , t = face_detection(sharp_img)
    
    if t == 10:
        if l == 4 and r == 5:
            return 'real'
        else:
            return 'fake'
    else:
        return 'fake'

# print(solution('test/r1.jpg'))