from urllib.parse import urlparse
import requests


class RedirectAnalyser:
    """
    Clase para analizar redirecciones de un dominio y puerto específicos,
    identificar si las redirecciones se realizan al mismo dominio o a otro y
    si la URL final contiene caracteres especiales fuera del código ASCII estándar.
    """

    def analyse_redirects(self, domain: str, port: int):
        """
        Realiza la conexión y sigue todas las redirecciones para el dominio y
        puertodados hasta que no haya más redirecciones, analiza la URL final
        para determinar si se redirige al mismo dominio o a otro y si contiene
        caracteres especiales.

        :param domain: Dominio a analizar.
        :param port: Puerto a analizar.
        :return: Tupla con el nombre de la URL final y dos booleanos que indican
                 si se redirige al mismo dominio y si contiene caracteres
                 especiales, respectivamente.
        """
        scheme = "https" if port == 443 else "http"
        initial_url = f"{scheme}://{domain}:{port}"
        try:
            final_url, final_domain = self.follow_redirects(initial_url)
            is_same_domain = domain in final_domain
            contains_special_chars = any(ord(char) > 127 for char in final_url)
            return (final_url, is_same_domain, contains_special_chars)
        except requests.RequestException as e:
            print(f"Error al conectarse o seguir redirecciones: {e}")
            return (None, False, False)

    def follow_redirects(self, url: str):
        """
        Sigue las redirecciones de una URL dada hasta que no haya más
        redirecciones.

        :param url: URL inicial desde donde empezar a seguir redirecciones.
        :return: URL final y dominio final después de seguir todas las
                 redirecciones.
        """
        response = requests.get(url, allow_redirects=True, timeout=5)
        while response.history:
            response = requests.get(response.url, allow_redirects=True, timeout=5)
        final_url = response.url
        final_domain = urlparse(final_url).netloc
        return final_url, final_domain


if __name__ == "__main__":
    redirect_analyser = RedirectAnalyser()
    final_url_, is_same_domain_, contains_special_chars_ = (
        redirect_analyser.analyse_redirects("balderip.com", 80)
    )
    print(f"URL Final: {final_url_}, Mismo dominio: {is_same_domain_}"
          f", Contiene caracteres especiales: {contains_special_chars_}")
