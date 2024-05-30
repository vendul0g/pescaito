import time
import numpy as np
from scipy.fftpack import dct
import favicon
from PIL import Image
import requests
from io import BytesIO

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"

def fetch_favicon(url: str) -> Image.Image:
    """
    Fetches the favicon of a given URL.
    
    :param url: URL of the website.
    :return: Image object of the favicon.
    """
    icons = favicon.get(url)
    icon = icons[0]
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(icon.url, headers=headers, stream=True)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    return img


def rgb_dct(image: Image.Image) -> tuple:
    """
    Computes the DCT of the RGB channels of an image.
    
    :param image: PIL Image object.
    :return: DCT of the red, green, and blue channels.
    """
    # Ensure the image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize the image to a common size
    image = image.resize((32, 32))
    
    # Split the image into R, G, B channels
    r, g, b = image.split()
    
    # Compute the DCT of each channel
    r_dct = dct(dct(np.array(r), axis=0), axis=1)
    g_dct = dct(dct(np.array(g), axis=0), axis=1)
    b_dct = dct(dct(np.array(b), axis=0), axis=1)
    
    return r_dct, g_dct, b_dct

def rms_diff(dct1: np.ndarray, dct2: np.ndarray) -> float:
    """
    Computes the RMS difference between two DCTs.
    
    :param dct1: First DCT array.
    :param dct2: Second DCT array.
    :return: RMS difference.
    """
    return np.sqrt(np.mean((dct1 - dct2) ** 2))

def compare_favicons(url1: str, url2: str) -> float:
    """
    Compares the favicons of two URLs using DCT and RMS.
    
    :param url1: First URL.
    :param url2: Second URL.
    :return: Normalized similarity value between 0 and 1.
    """
    img1 = fetch_favicon(url1)
    img2 = fetch_favicon(url2)

    img1.save("favicon1.png")
    img2.save("favicon2.png")
    
    
    r_dct1, g_dct1, b_dct1 = rgb_dct(img1)
    r_dct2, g_dct2, b_dct2 = rgb_dct(img2)
    
    r_rms = rms_diff(r_dct1, r_dct2)
    g_rms = rms_diff(g_dct1, g_dct2)
    b_rms = rms_diff(b_dct1, b_dct2)
    
    avg_rms = (r_rms + g_rms + b_rms) / 3.0
    normalized_similarity = 1 / (1 + avg_rms)
    
    return normalized_similarity

def main():
    """
    Main function to compare favicons of two URLs.
    """
    url1 = "https://iegitec.com"  # Replace with the first URL
    url2 = "https://legitec.com"  # Replace with the second URL
    
    similarity_value = compare_favicons(url1, url2)
    print(f"Similarity value: {similarity_value}")

if __name__ == "__main__":
    main()
