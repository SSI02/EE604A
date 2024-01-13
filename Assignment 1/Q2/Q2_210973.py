import librosa
import librosa.feature as lf
import numpy as np
import cv2
from skimage import exposure

def solution(audio_path):
    
    audio_file1 = audio_path

    y1, sr1 = librosa.load(audio_file1, sr=None)  # Use sr=None to preserve the original sample rate

    n_fft = 2048 

    hop_length = 512

    spec1 = librosa.feature.melspectrogram(y = y1 , sr = sr1)

    S_db1 = librosa.power_to_db(spec1 , ref=np.max)


    # Define the kernel size (adjust sigma as needed for smoothing)
    kernel_size = (5, 5)
    sigma = 1.0

    # Apply Gaussian blur
    spectrogram_smoothed1 = cv2.GaussianBlur(spec1, kernel_size, sigma)

    spectrogram_equalized1 = exposure.equalize_hist(spectrogram_smoothed1)

    sq = []
    # sex2 = []

    mini1 = 10000
    maxi1 = -1
    # mini2 = 10000
    for i in spectrogram_equalized1:
        for j in i:
            if j > maxi1:
                maxi1 = j
            if j<mini1:
                mini1 = j
            sq.append(j)
            

    if mini1 >= 0.85:
        return 'cardboard'
    else:
        return 'metal'