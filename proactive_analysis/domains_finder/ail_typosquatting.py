import math
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from ail_typo_squatting import runAll, dnsResolving
from proactive.models import SimilarDomain  # Django
from main.models import Domain  # Django


class AilTyposquatting:
    def find(self, domain: Domain) -> SimilarDomain:
        """
        Generamos dominios similares al dominio dado y comprobamos si existen
        """
        print("[*] Comenzando búsqueda con Ail-Typosquatting...", end='\t')

        # Ejecutamos Ail-Typosquatting
        all_domains = runAll(
            domain=domain.name,
            limit=math.inf,
            formatoutput="text",
            pathOutput="/tmp/",
            verbose=False,
            givevariations=True,
            keeporiginal=False,
        )
        print(" OK")
        # dnsResolving(all_domains, domain.name) TODO ver si esto funciona
        return self.__check_domains_exists(all_domains, domain)

    def __check_domains_exists(
        self, domains: list[str], original_domain: Domain
    ) -> list[SimilarDomain]:
        """
        Comprobamos la existencia de todos los dominios generados
        Se recorren todos los dominios generados y se comprueba si existen
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
                try:
                    if future.result():
                        existing_domains.append(
                            SimilarDomain(
                                name=domain,
                                original_domain=original_domain,
                            )
                        )
                except Exception as e:
                    print(f"[!] Error checking domain {domain}: {str(e)}")
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
        except Exception as e:
            print(f"[!] Error de red comprobando {d}: {str(e)}")
            return False


    def __parse_list(self, domains: list[str]) -> list[str]:
        """
        Parseamos la lista de dominios para que solo tengamos nombres de dominio
        y no el resto de información
        """
        return [d[0] for d in domains]


AIL_TYPO_SQUATTING = AilTyposquatting()
