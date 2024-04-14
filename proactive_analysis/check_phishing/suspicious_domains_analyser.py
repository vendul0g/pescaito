from proactive.models import SimilarDomain
from .get_whois import WHOIS_ANALYSER

class DomainAnalyser:
    def analyse(self, similar_domain:SimilarDomain):
        '''
        En esta función se orquesta el analizador de los dominios para determinar
        si es phishing o no
        '''
        # 1. Analizamos si el dominio está blacklist / whitelist
        # TODO implementar

        # 2. Analizamos el registro WHOIS
        WHOIS_ANALYSER.analyze_whois(similar_domain)
        # TODO comprobar que los datos devueltos no son None


DOMAIN_ANALYSER = DomainAnalyser()
