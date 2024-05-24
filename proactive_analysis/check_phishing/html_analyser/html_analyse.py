from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import requests
from proactive_analysis.check_phishing.html_analyser.resource_analyser import RESOURCE_ANALYSER
from proactive_analysis.check_phishing.html_analyser.login_checker import LOGIN_CHECKER
# from resource_analyser import RESOURCE_ANALYSER
# from login_checker import LOGIN_CHECKER

class HtmlAnalyser:
    """
    Clase para analizar contenido HTML de una URL dada y extraer información
    específica.
    """

    def fetch_html(self, url: str) -> str:
        """
        Obtiene el contenido HTML de la URL especificada.

        :return: Contenido HTML.
        """
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"[!] Error fetching HTML content: {e}")
            return None
        
    def analyze_links(self, html: str) -> list[str]:
        """
        Analiza las etiquetas <a> del HTML para comprobar si contienen "http"
        y si el enlace apunta donde dice.
        """
        soup = BeautifulSoup(html, 'html.parser')
        suspicious_links = [a['href'] for a in soup.find_all('a', href=True) if 'http' in a['href']]
        return suspicious_links

    def analyse_html(self, similar_url: str, orig_domain_name: str) -> dict:
        """
        Realiza un análisis completo del HTML de la página con dominio similar.

        :return: Diccionario con todos los resultados del análisis.
        """
        # Establecemos los parámetros con los que haremos el análisis
        parsed_url = urlparse(similar_url)
        domain = parsed_url.netloc
        html = self.fetch_html(similar_url)
        if not html:
            print(f"[!] No se ha podido obtener el HTML de {similar_url}")
            return None

        # 1. Búsqueda de etiquetas de carga de recursos dentro del HTML
        # 1.1 Comparación de referencias internas vs externas
        internal_links, external_links = RESOURCE_ANALYSER.analyse_resource_links(
            html, domain
        )
        print(f"Internal links: {internal_links}")
        print(f"External links: {external_links}")

        # 2. Búsqueda de formularios de inicio de sesión (login form)
        is_login_form = LOGIN_CHECKER.check_login(html)

        # 3. Búsquedas de referencias al dominio original
        is_original_domain = orig_domain_name in html

        # 4. Comprobar si las etiquetas <a> contienen "http" y si el enlace apunta donde dice
        suspicious_links = self.analyze_links(html)

        return {
            "internal_links": internal_links,
            "external_links": external_links,
            "is_login_form": is_login_form,
            "is_original_domain": is_original_domain,
            "suspicious_links": suspicious_links,
        }

HTML_ANALYSER = HtmlAnalyser()

if __name__ == "__main__":
    r = HTML_ANALYSER.analyse_html("https://iegitec.com", "legitec.com")
    print(f"Result: {r}")
