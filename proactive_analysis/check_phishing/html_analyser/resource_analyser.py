from bs4 import BeautifulSoup


class HrefAnalyser:
    """
    Clase para analizar el contenido HTML para contar y diferenciar entre enlaces
    internos y externos basados en los atributos href, src y action.
    """

    def get_external_links(
        self, external_links: list, tags: list, attr: str, similar_domain_name: str
    ):
        """
        Extrae los enlaces externos de las etiquetas HTML y los añade a la lista
        de enlaces externos.

        :param external_links: Lista de enlaces externos.
        :param tags: Lista de etiquetas HTML.
        :param attr: Atributo de la etiqueta que contiene el enlace.
        :param similar_domain_name: Nombre del dominio similar.
        """
        for tag in tags:
            url = tag.get(attr)
            print(f"url: {url}")
            # Comprobamos si el enlace es interno o externo
            if url and "http" in url and not similar_domain_name in url:
                external_links.append(url)

    def analyse_resource_links(self, html: str, similar_domain_name: str) -> tuple:
        """
        Analizamos el HTML buscando "href", "src" o "action", calificamos los
        enlaces entre internos y externos para hacer la comparación

        :return: La diferencia entre links internos y externos
        """
        # Sacamos las etiquetas de carga de recursos del HTML
        soup = BeautifulSoup(html, "html.parser")
        href_tags = soup.find_all(["a", "link"])  # usan href
        src_tags = soup.find_all(["script", "img"])  # usan src
        action_tags = soup.find_all("form")  # usan action
        print(f"href_tags: {href_tags} - src_tags: {src_tags} - action_tags: {action_tags}")
        # Inicializamos la lista
        external_links = []

        # Recorremos las etiquetas y extraemos los enlaces
        self.get_external_links(external_links, href_tags, "href", similar_domain_name)
        self.get_external_links(external_links, src_tags, "src", similar_domain_name)
        self.get_external_links(
            external_links, action_tags, "action", similar_domain_name
        )

        # Contamos los enlaces internos y externos
        total_count = len(href_tags) + len(src_tags) + len(action_tags)
        external_count = len(external_links)
        internal_count = total_count - external_count

        # Devolvemos los resultados
        return internal_count, external_count


RESOURCE_ANALYSER = HrefAnalyser()
