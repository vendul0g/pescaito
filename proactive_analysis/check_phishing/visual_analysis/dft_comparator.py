# File path: visual_comparator.py

import numpy as np
import cv2

class DFTComparator:
    def __calculate_dft(self, image: np.ndarray) -> np.ndarray:
        """
        Calcula la DFT de una imagen
        """
        return np.fft.fft2(image)

    def __calculate_rms_dft(
        self, image1_dft: np.ndarray, image2_dft: np.ndarray
    ) -> float:
        """
        Calcula el error RMS del resultado de 2 DFT
        """
        diff = image1_dft - image2_dft
        rms = np.sqrt(np.mean(np.abs(diff) ** 2))
        return rms

    def compare_images(self, image1_path: str, image2_path: str) -> float:
        """
        Compara dos imágenes utilizando el error RMS de sus DFT en los canales RGB.

        :return: double con el resultado RMS normalizado de la comparación.
        """
        # Cargamos las imágenes
        image1 = cv2.imread(image1_path)
        image2 = cv2.imread(image2_path)

        # Ensure the images are the same size
        if image1.shape != image2.shape:
            raise ValueError("Images must be the same size for comparison")

        # Separate the channels
        channels1 = cv2.split(image1)
        channels2 = cv2.split(image2)

        # Calculate DFTs and RMS for each channel (RGB)
        rms_values = []
        for ch1, ch2 in zip(channels1, channels2):
            dft1 = self.__calculate_dft(ch1)
            dft2 = self.__calculate_dft(ch2)
            rms = self.__calculate_rms_dft(dft1, dft2)
            rms_values.append(rms)

        # Average RMS value across all channels
        average_rms = np.mean(rms_values)

        # Normalize RMS value to be between 0 and 1
        normalized_rms = 1 / (1 + average_rms)

        return normalized_rms

DFT_COMPARATOR = DFTComparator()