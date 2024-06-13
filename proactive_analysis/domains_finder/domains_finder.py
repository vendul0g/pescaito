from proactive.models import SimilarDomain # Django
from main.models import Domain # Django
from .dnstwist_tool import DNS_TWIST # Django
from .ail_typosquatting import AIL_TYPO_SQUATTING # Django

# from dnstwist_tool import DNSTwist # Local execution:TODO comentar
# from domain_entry_result import DomainEntryResult # Local execution:TODO comentar

class DomainFinder:
    '''
    Clase dedicada a encontrar dominios parecidos a uno dado.
    Para ello hacemos uso de diferentes herramientas
    - DNSTwist
    - ail_typo_squatting
    '''
    def find(self, domain: Domain) -> list[SimilarDomain]: 
        # Análisis de DNSTwist
        domains_dnstwist = DNS_TWIST.find(domain)
        domains_ail = []#AIL_TYPO_SQUATTING.find(domain)

        # Unión de los dominios encontrados
        unique_domains = set(domains_dnstwist) | set(domains_ail)
        # Devolvemos los dominios encontrados - existentes
        return list(unique_domains)


DOMAIN_FINDER = DomainFinder()
