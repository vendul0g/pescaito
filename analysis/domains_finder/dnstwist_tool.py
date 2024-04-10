import dnstwist

from ..domain_entry_result import DomainEntryResult  # Django
# from domain_entry_result import DomainEntryResult  # Local execution


class DNSTwist:
    def find(self, domain: str) -> list[DomainEntryResult]:
        """
        Función para buscar dominios similares a uno dado con DNSTwist
        """
        # Execute DNSTwist
        domains = dnstwist.run(
            domain=domain,
            format="json",
            registered=True,
            fuzzers="vowel-swap",
            output="/dev/null",
        )
        return self.parse_results(domains)

    def parse_results(self, dnstwist_result: str) -> list[DomainEntryResult]:
        """'
        Función para parsear los resultados de dnstwist
        """
        # Extract the domains and the IPs from the JSON
        domains = []
        for entry in dnstwist_result:  # For each entry in the result
            # Creamos una instancia de DomainEntryResult
            domain_entry = DomainEntryResult(
                name=entry["domain"],
                ip=entry["dns_a"] if "dns_a" in entry else [],
            )
            domains.append(domain_entry)
        return domains
