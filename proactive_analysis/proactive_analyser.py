import os
from django.conf import settings
from main.models import Domain
from proactive.models import SimilarDomain
from .domains_finder.domains_finder import (
    DOMAIN_FINDER,
    # DomainFinder,
)
from .check_phishing.similar_domains_analyser import (
    DOMAIN_ANALYSER,
)

class ProactiveAnalyser:
    def proactive_analysis(self, domain: Domain) -> str:
        # Aquí es donde se desarrolla el análisis de cada dominio
        # 1. Encontrar los dominios parecidos
        similar_domains = DOMAIN_FINDER.find(domain) # TODO No limitar las búsquedas

        # 2. Analizar cada dominio parecido para comprobar si es phishing
        for sm in similar_domains:
            DOMAIN_ANALYSER.analyse(sm)

        # 3. Devolver los resultados
        # Creamos una respuesta
        file_content = f"{domain.name} - Dominio original\n=========================================\n\n"
        for r in similar_domains:
            file_content += f"{r}\n\n"

        # Escribimos la respuesta en un fichero
        original_domain_name = domain.name
        file_name = f'{original_domain_name.replace(".", "_")}.txt'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, "w+", encoding="utf-8") as f:
            f.write(file_content)

        # Creamos la URL para descargar el fichero
        return f"{file_name}"

PROACTIVE_ANALYSER = ProactiveAnalyser()
