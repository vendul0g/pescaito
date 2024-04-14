from proactive.models import SimilarDomain # Django
from .dnstwist_tool import DNSTwist # Django
from .ail_typosquatting import AilTyposquatting # Django

# from dnstwist_tool import DNSTwist # Local execution:TODO comentar
# from domain_entry_result import DomainEntryResult # Local execution:TODO comentar

class DomainFinder:
    '''
    Clase dedicada a encontrar dominios parecidos a uno dado.
    Para ello hacemos uso de diferentes herramientas
    - DNSTwist
    - ail_typo_squatting
    '''
    def find(self, domain: str) -> list[SimilarDomain]: 
        # Análisis de DNSTwist
        domains_dnstwist = DNSTwist().find(domain)
        domains_ail = AilTyposquatting().find(domain)

        # Unión de los dominios encontrados
        unique_domains = set(domains_dnstwist) | set(domains_ail)
        # Devolvemos los dominios encontrados - existentes
        return list(unique_domains)


DOMAIN_FINDER = DomainFinder()


