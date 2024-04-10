from .dnstwist_tool import DNSTwist # Django
from ..domain_entry_result import DomainEntryResult # Django
# from dnstwist_tool import DNSTwist # Local execution:TODO comentar
# from domain_entry_result import DomainEntryResult # Local execution:TODO comentar

class DomainFinder:
    '''
    Clase dedicada a encontrar dominios parecidos a uno dado.
    Para ello hacemos uso de diferentes herramientas
    - DNSTwist
    - ...
    '''
    def find(self, domain: str) -> list[DomainEntryResult]: 
        # Análisis de DNSTwist
        domains = DNSTwist().find(domain)
        return domains


DOMAIN_FINDER = DomainFinder()

if __name__ == '__main__':
    domain_results = DOMAIN_FINDER.find('balderip.com')
    for result in domain_results:
        print(result)
