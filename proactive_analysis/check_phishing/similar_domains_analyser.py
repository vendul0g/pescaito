from proactive.models import SimilarDomain
from .get_whois import WHOIS_ANALYSER
from .geoip.tld_with_country import TLD_COUNTRY
from .geoip.get_geoip import GEOIP

class SimilarDomainAnalyser:
    def analyse(self, similar_domain:SimilarDomain):
        '''
        En esta función se orquesta el analizador de los dominios para determinar
        si es phishing o no
        '''
        # 1. Analizamos si el dominio está blacklist / whitelist
        # TODO implementar

        # 2. Analizamos el registro WHOIS
        WHOIS_ANALYSER.analyze_whois(similar_domain)
        
        # 3. Analizamos la geolocalización
        # 3.1 Obtenemos el país asociado al TLD
        TLD_COUNTRY.get_country_from_tld(similar_domain)
        # 3.2 Obtenemos los países asociados a las IPs del dominio similar
        GEOIP.get_domain_country(similar_domain)





DOMAIN_ANALYSER = SimilarDomainAnalyser()
