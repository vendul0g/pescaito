# File path: visual_comparator.py

import time
import numpy as np
import cv2
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from scipy.fftpack import dct
from scipy.spatial.distance import euclidean

def take_screenshot(url: str, file_name: str) -> None:
    """
    Takes a screenshot of the given URL and saves it as the specified file name.
    """
    options = Options()
    options.headless = True
    options.binary_location = "/home/alvaro/Documents/firefox/firefox"

    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()), options=options
    )
    driver.get(url)
    # Add a delay to allow the page to fully load
    time.sleep(5)
    driver.save_screenshot(file_name)
    driver.quit()

def calculate_dct(image: np.ndarray) -> np.ndarray:
    """
    Calculates the Discrete Cosine Transform (DCT) of the given image.
    """
    return dct(dct(image.T, norm='ortho').T, norm='ortho')

def compare_channels(image1: np.ndarray, image2: np.ndarray) -> float:
    """
    Compares two images using DCT and returns the RMS of the differences.
    """
    # Ensure the images are the same size
    if image1.shape != image2.shape:
        raise ValueError("Images must be the same size for comparison")
    
    # Calculate DCT for each channel
    dct1 = calculate_dct(image1)
    dct2 = calculate_dct(image2)
    
    # Calculate RMS of the differences
    rms = np.sqrt(np.mean((dct1 - dct2) ** 2))
    
    return rms

def compare_images(image1_path: str, image2_path: str) -> float:
    """
    Compares two images using DCT of RGB channels and calculates the normalized similarity.
    
    :return: Normalized similarity value between 0 and 1.
    """
    # Load images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Ensure the images are the same size
    if image1.shape != image2.shape:
        raise ValueError("Images must be the same size for comparison")

    # Split the images into R, G, B channels
    channels1 = cv2.split(image1)
    channels2 = cv2.split(image2)

    # Compare each channel
    rms_values = [compare_channels(c1, c2) for c1, c2 in zip(channels1, channels2)]

    # Average RMS values and normalize
    rms_mean = np.mean(rms_values)
    similarity = 1 / rms_mean if rms_mean != 0 else 1

    return similarity

def main():
    """
    Main function to take snapshots of two URLs and compare them.
    """
    url1 = "https://www.youtube.com/results?search_query=guitarra" 
    url2 = "https://www.youtube.com/results?search_query=sean+long" 
    file1 = "snapshot1.png"
    file2 = "snapshot2.png"

    # Take screenshots of both URLs
    take_screenshot(url1, file1)
    take_screenshot(url2, file2)

    # Compare the images and calculate the similarity value
    similarity_value = compare_images(file1, file2)

    # Print the similarity value
    print(f"Similarity value: {similarity_value}")

if __name__ == "__main__":
    main()
