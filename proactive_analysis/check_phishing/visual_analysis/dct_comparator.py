import numpy as np
import cv2
from scipy.fftpack import dct

class DCTComparator:
    def calculate_dct(self, image: np.ndarray) -> np.ndarray:
        """
        Calcula la Transformada de Coseno Discreta (DCT) de la imagen dada.
        """
        return dct(dct(image.T, norm='ortho').T, norm='ortho')

    def compare_channels(self, image1: np.ndarray, image2: np.ndarray) -> float:
        """
        Compara dos imágenes utilizando DCT y devuelve la raíz cuadrada de la media de 
        los cuadrados de las diferencias.
        """
        # Aseguramos el mismo tamaño de las imágenes
        if image1.shape != image2.shape:
            raise ValueError("Images must be the same size for comparison")
        
        # Calculamso la DCT de los canales
        dct1 = self.calculate_dct(image1)
        dct2 = self.calculate_dct(image2)
        
        # Calculamos RMS
        rms = np.sqrt(np.mean((dct1 - dct2) ** 2))
        
        return rms

    def compare_images(self, image1_path: str, image2_path: str) -> float:
        """
        Compara dos imágenes utilizando DCT de los canales RGB y calcula la similitud 
        normalizada.
        
        :return: Valor de similitud normalizado entre 0 y 1
        """
        # Carga las imágenes
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        # Aseguramos el mismo tamaño de imagen
        if image1.shape != image2.shape:
            raise ValueError("Images must be the same size for comparison")

        # Dividimos canales: R, G, B 
        channels1 = cv2.split(image1)
        channels2 = cv2.split(image2)

        # Comparamos cada canal
        rms_values = [self.compare_channels(c1, c2) for c1, c2 in zip(channels1, channels2)]

        # Media del RMS 
        rms_mean = np.mean(rms_values)

        # Normalizamos
        similarity = 1 / rms_mean if rms_mean != 0 else 1

        return similarity

DCT_COMPARATOR = DCTComparator()

# def main():
#     """
#     Main function to take snapshots of two URLs and compare them.
#     """
#     url1 = "https://www.youtube.com/results?search_query=guitarra" 
#     url2 = "https://www.youtube.com/results?search_query=sean+long" 
#     file1 = "snapshot1.png"
#     file2 = "snapshot2.png"

#     # Take screenshots of both URLs
#     take_screenshot(url1, file1)
#     take_screenshot(url2, file2)

#     # Compare the images and calculate the similarity value
#     similarity_value = compare_images(file1, file2)

#     # Print the similarity value
#     print(f"Similarity value: {similarity_value}")

# if __name__ == "__main__":
#     main()
