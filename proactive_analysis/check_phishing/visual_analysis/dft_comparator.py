# File path: visual_comparator.py

import time
import numpy as np
import cv2
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def take_screenshot(url: str, file_name: str) -> None:
    """
    Takes a screenshot of the given URL and saves it as the specified file name.
    """
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    driver.get(url)
    # Add a delay to allow the page to fully load
    time.sleep(10)
    driver.save_screenshot(file_name)
    driver.quit()

def calculate_dft(image: np.ndarray) -> np.ndarray:
    """
    Calculates the Discrete Fourier Transform (DFT) of an image.
    """
    return np.fft.fft2(image)

def calculate_rms_dft(image1_dft: np.ndarray, image2_dft: np.ndarray) -> float:
    """
    Calculates the Root Mean Square (RMS) error between two DFTs.
    """
    diff = image1_dft - image2_dft
    rms = np.sqrt(np.mean(np.abs(diff) ** 2))
    return rms

def compare_images(image1_path: str, image2_path: str, threshold: float = 10e-6) -> bool:
    """
    Compares two images using the RMS error of their DFTs in RGB channels.
    
    :return: Boolean indicating if images are similar based on the threshold.
    """
    # Load images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Ensure the images are the same size
    if image1.shape != image2.shape:
        raise ValueError("Images must be the same size for comparison")

    # Separate the channels
    channels1 = cv2.split(image1)
    channels2 = cv2.split(image2)

    # Calculate DFTs and RMS for each channel
    rms_values = []
    for ch1, ch2 in zip(channels1, channels2):
        dft1 = calculate_dft(ch1)
        dft2 = calculate_dft(ch2)
        rms = calculate_rms_dft(dft1, dft2)
        rms_values.append(rms)

    # Average RMS value across all channels
    average_rms = np.mean(rms_values)

    # Normalize RMS value to be between 0 and 1
    normalized_rms = 1 / (1 + average_rms)

    return normalized_rms >= threshold

def main():
    """
    Main function to take snapshots of two URLs and compare them.
    """
    url1 = "https://formacion.legitec.com/acceso"  # Replace with the first URL
    url2 = "https://iegitec.com"  # Replace with the second URL
    file1 = "snapshot1.png"
    file2 = "snapshot2.png"
    threshold = 10e-6  # Chosen threshold

    # Take screenshots of both URLs
    take_screenshot(url1, file1)
    take_screenshot(url2, file2)

    # Compare the images and determine if they are similar
    similar = compare_images(file1, file2, threshold)

    # Print the result
    if similar:
        print("The images are similar.")
    else:
        print("The images are not similar.")

if __name__ == "__main__":
    main()
