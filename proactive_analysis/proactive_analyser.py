import os
from django.conf import settings
from proactive.models import SimilarDomain
from .domains_finder.domains_finder import (
    DOMAIN_FINDER,
    # DomainFinder,
)
from .check_phishing.suspicious_domains_analyser import (
    DOMAIN_ANALYSER,
    # DomainAnalyser,
)

class ProactiveAnalyser:
    def proactive_analysis(self, domain) -> str:
        # Aquí es donde se desarrolla el análisis de cada dominio
        # 1. Encontrar los dominios8 parecidos
        similar_domains = DOMAIN_FINDER.find(domain) # TODO No limitar las búsquedas

        # 2. Analizar cada dominio parecido para comprobar si es phishing
        for sm in similar_domains:
            DOMAIN_ANALYSER.analyse(sm)
            print(sm.is_phishing)

        # 3. Devolver los resultados
        # Creamos una respuesta
        file_content = f"{domain}\n"
        for r in similar_domains:
            file_content += f"\t{r}\n"

        # Escribimos la respuesta en un fichero
        file_name = domain.replace(".", "_")
        file_path = os.path.join(settings.MEDIA_ROOT, f'{file_name}.txt')
        with open(file_path, "w+", encoding="utf-8") as f:
            f.write(file_content)

        # Creamos la URL para descargar el fichero
        return f"{file_name}.txt"

PROACTIVE_ANALYSER = ProactiveAnalyser()
