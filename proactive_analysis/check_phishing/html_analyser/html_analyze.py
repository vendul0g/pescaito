import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class HtmlAnalyser:
    '''
    Clase para analizar contenido HTML de una URL dada y extraer información
    específica.
    '''
    def fetch_html(self, url: str) -> str:
        '''
        Obtiene el contenido HTML de la URL especificada.

        :return: Contenido HTML.
        '''
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching HTML content: {e}")
            return None



    def analyse_html(self, similar_url: str, orig_domain_name: str):
        '''
        Realiza un análisis completo del HTML de la página con dominio similar.

        :return: Diccionario con todos los resultados del análisis.
        '''
        # Establecemos los parámetros con los que haremos el análisis
        parsed_url = urlparse(similar_url)
        domain = parsed_url.netloc
        html = self.fetch_html(similar_url)

        # 1. Búsqueda de "href" dentro del HTML (u otras etiquetas de referencia)
        # 1.1 Comparación de referencias internas vs externas
        # 2. Búsqueda de formularios de inicio de sesión (login form)
        # 3. Búsqueda de los scripts que se están cargando
        # 3.1 Comparación de scripts locales vs externos
        # 4. Búsquedas de referencias al dominio original
        # 5. Comprobar si existe está el propio nombre de dominio en el HTML
        # 6. Comprobar si las etiquetas <a> contienen "http" y si el enlace apunta donde dice
        
        # TODO revisar qué es lo que se devuelve
        # return {
        #     'external_vs_internal_resources': self.analyze_external_resources(),
        #     'has_login_form': self.analyze_login_forms(),
        #     'suspicious_links': self.analyze_links()
        # }


# Ejemplo de uso:
analyzer = HtmlAnalyser("https://legitec.com")
results = analyzer.analyse_html()
print(f"External resources: {results['external_vs_internal_resources']['external']}")
print("="*50)
print(f"Has login form: {results['has_login_form']}")
print("="*50)
print(f"Suspicious links: {results['suspicious_links']}")