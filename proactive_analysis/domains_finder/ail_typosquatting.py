import math
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from ail_typo_squatting import runAll
from proactive.models import SimilarDomain # Django
from main.models import Domain # Django


class AilTyposquatting:
    def find(self, domain: Domain) -> SimilarDomain:
        all_domains = runAll(
            domain=domain.name,
            limit=math.inf,
            formatoutput="text",
            pathOutput="/tmp/",
            verbose=False,
            givevariations=True,
            keeporiginal=False,
        )
        return self.__check_domains_exists(all_domains, domain)

    def __check_domains_exists(self, domains: list[str], original_domain: Domain) -> list[SimilarDomain]:
        """
        Comprobamos la existencia de todos los dominios generados
        """
        # 1. Parseamos la lista para que podamos tener solo nombres de dominio
        domains = self.__parse_list(domains)
        domains = domains[:10]  # Limitamos a 10 dominios TODO BORRAR

        # 2. Comprobamos la existencia de cada dominio - Paralelizando
        existing_domains = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_domain = {
                executor.submit(self.__check_single_domain, d): d for d in domains
            }

            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                if future.result():
                    existing_domains.append(SimilarDomain(
                        name=domain,
                        original_domain=original_domain,
                    ))
        return existing_domains

    def __check_single_domain(self, d: str) -> bool:
        """
        Comprobamos si existe un dominio específico
        """
        try:
            socket.gethostbyname(d)
            return True
        except socket.gaierror:
            return False

    def __parse_list(self, domains: list[str]) -> list[str]:
        """
        Parseamos la lista de dominios para que solo tengamos nombres de dominio
        y no el resto de información
        """
        return [d[0] for d in domains]
