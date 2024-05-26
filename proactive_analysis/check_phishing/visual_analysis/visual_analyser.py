import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from .dft_comparator import DFT_COMPARATOR
from django.conf import settings


class VisualAnalyser:
    """
    Clase que se encarga de analizar el contenido visual de una página
    web
    """

    def __take_screenshot(self, url: str, file_name: str):
        """
        Dada una URL y el nombre del fichero donde se guarda, hace una captura de pantalla
        de la web
        """
        options = Options()
        options.headless = True
        options.binary_location = "/home/alvaro/Documents/firefox/firefox"

        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()), options=options
        )
        driver.get(url)
        # Add a delay to allow the page to fully load
        time.sleep(10)
        driver.save_screenshot(file_name)
        driver.quit()

    def __favicon_analyse(self, url1: str, url2: str) -> float:
        """
        Método para analizar el contenido visual de dos favicon
        """
        return 0  # TODO implementar

    def __webpage_analyse(self, url1: str, url2: str) -> tuple:
        """
        Método para analizar el contenido visual de dos páginas web
        """
        # Creamos los nombres de los ficheros: a las URLs les quitamos el protocolo y cambiamos '.' por '_' + '.png'
        file1 = os.path.join(
            settings.MEDIA_ROOT,
            url1.split("//")[1].replace(".", "_").replace("/", "-") + ".png",
        )
        file2 = os.path.join(
            settings.MEDIA_ROOT,
            url2.split("//")[1].replace(".", "_").replace("/", "-") + ".png",
        )
        print(f"[*] Files: {file1} and {file2}")

        # Obtenemos las imágenes de las web
        if not os.path.exists(file1):
            self.__take_screenshot(url1, file1)
        if not os.path.exists(file2):
            self.__take_screenshot(url2, file2)

        # Comparamos las imágenes
        # 1. DFT
        r1 = DFT_COMPARATOR.compare_images(file1, file2)

        # 2. DCT TODO implementar
        r2 = self.__favicon_analyse(url1, url2)

        return r1, r2

    def visual_analysis(self, url1: str, url2: str) -> dict:
        """
        Método para analizar el contenido visual de dos páginas web
        aplicando comparación con DCT y DFT para:
        - página web
        - favicon

        :param url1: URL de la página web original
        :param url2: URL de la página web similar
        """
        results = []
        # 1. Comparación web
        dft_r, dct_r = self.__webpage_analyse(url1, url2)

        # 2. Comparación favicon
        favicon_r = self.__favicon_analyse(url1, url2)

        # Devolvemos el resultado
        return {"dft_web": dft_r, "dct_web": dct_r, "favicon": favicon_r}


VISUAL_ANALYSER = VisualAnalyser()
