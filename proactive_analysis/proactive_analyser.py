import os
from django.conf import settings
from main.models import Domain
from proactive.models import SimilarDomain
from .domains_finder.domains_finder import DOMAIN_FINDER
from .check_phishing.similar_domains_analyser import SIMILAR_DOMAIN_ANALYSER
from .reporter import REPORTER
from django.utils import timezone

class ProactiveAnalyser:
    def proactive_analysis(self, domain: Domain) -> str:
        """
        Función para realizar un análisis proactivo de un dominio
        """
        print(f"{'='*50}\n[*] Analizando dominio {domain} de forma proactiva\n{'='*50}")
        # Aquí es donde se desarrolla el análisis de cada dominio
        # 1. Encontrar los dominios8 parecidos
        similar_domains = [] #DOMAIN_FINDER.find(domain) # TODO No limitar las búsquedas
        similar_domains.append(SimilarDomain(name='iegitec.com', original_domain=domain, found_date=timezone.now()))# TODO borrar
        # 2. Analizar cada dominio parecido y comprobar si es phishing
        for sm in sorted(similar_domains):
            # Análisis
            SIMILAR_DOMAIN_ANALYSER.analyse(sm)
            # Comprobación de phishing
            is_phishing = REPORTER.check_phishing(sm)
            if is_phishing:
                # Alertamos
                print(f"[!] {sm.name} es phishing")
            REPORTER.report(sm)


        # 4. Devolver los resultados
        # Creamos una respuesta
        file_content = f"{domain.name} - Dominio original\n{'='*70}\n\n"
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
