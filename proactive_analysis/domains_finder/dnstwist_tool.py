from proactive.models import SimilarDomain # Django
from main.models import Domain # Django
import dnstwist


class DNSTwist:
    def find(self, domain: Domain) -> list[SimilarDomain]:
        """
        Función para buscar dominios similares a uno dado con DNSTwist
        """
        # Execute DNSTwist
        domains = dnstwist.run(
            domain=domain.name,
            format="json",
            registered=True,
            # fuzzers="bitsquatting,homoglyph,hyphenation,omission,repetition,replacement,transposition,various,vowel-swap",
            fuzzers="vowel-swap",
            output="/dev/null",
            threads=20,
        )
        return self.__parse_results(domains, domain)

    def __parse_results(self, dnstwist_result: str, original_domain: Domain) -> list[SimilarDomain]:
        """'
        Función para parsear los resultados de dnstwist
        """
        # Extract the domains and the IPs from the JSON
        domains = []
        for entry in dnstwist_result:  # For each entry in the result
            # Creamos una instancia de DomainEntryResult
            domain_entry = SimilarDomain(
                name=entry["domain"],
                original_domain=original_domain,
            )
            domains.append(domain_entry)
        return domains
