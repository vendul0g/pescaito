import numpy as np
from scipy.fftpack import dct
import favicon
from PIL import Image
import requests


class FaviconComparator:
    def get_favicon_url(self, url: str) -> str:
        """
        Dada la URL, consigue el favicon

        :param url: URL de la web
        :return: URL del favicon
        """
        try:
            icons = favicon.get(url)
            icon = icons[0]
            return icon.url
        except Exception as e:
            print(f"[!] Error fetching favicon: {e}")
            return None

    def __rgb_dct(self, image: Image.Image) -> tuple:
        """
        Realiza la DCT de los canales RGB de una imagen.

        :param image: PIL Image.
        :return: DCT de los canales R, G y B.
        """
        # Comprobamos el modo de la imagen
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Redimiensionamos la imagen a 32x32
        image = image.resize((32, 32))

        # Dividimos en canales
        r, g, b = image.split()

        # Hacemos la DCT de cada canal
        r_dct = dct(dct(np.array(r), axis=0), axis=1)
        g_dct = dct(dct(np.array(g), axis=0), axis=1)
        b_dct = dct(dct(np.array(b), axis=0), axis=1)

        return r_dct, g_dct, b_dct

    def __rms_diff(self, dct1: np.ndarray, dct2: np.ndarray) -> float:
        """
        Calcula la diferencia entre RMS

        :param dct1: Primer array DCT.
        :param dct2: Segundo array DCT.
        :return: RMS.
        """
        return np.sqrt(np.mean((dct1 - dct2) ** 2))

    def compare_favicons(self, file1: str, file2: str) -> float:
        """
        Compara los favicon de dos URLs.

        :param url1: primera URL.
        :param url2: segunda URL.
        :return: Similitud normalizada entre 0 y 1.
        """
        # Obtenemos las imágenes de los favicons
        img1 = Image.open(file1)
        img2 = Image.open(file2)

        # Calculamos la DCT de los canales RGBs
        r_dct1, g_dct1, b_dct1 = self.__rgb_dct(img1)
        r_dct2, g_dct2, b_dct2 = self.__rgb_dct(img2)

        # Calculamos la diferencia RMS de los canales
        r_rms = self.__rms_diff(r_dct1, r_dct2)
        g_rms = self.__rms_diff(g_dct1, g_dct2)
        b_rms = self.__rms_diff(b_dct1, b_dct2)

        # Media de los RMS
        avg_rms = (r_rms + g_rms + b_rms) / 3.0

        # Normalizamos
        normalized_similarity = 1 / (1 + avg_rms)

        return normalized_similarity


FAVICON_COMPARATOR = FaviconComparator()

# def main():
#     """
#     Main function to compare favicons of two URLs.
#     """
#     url1 = "https://iegitec.com"  # Replace with the first URL
#     url2 = "https://legitec.com"  # Replace with the second URL

#     similarity_value = compare_favicons(url1, url2)
#     print(f"Similarity value: {similarity_value}")


# if __name__ == "__main__":
#     main()
