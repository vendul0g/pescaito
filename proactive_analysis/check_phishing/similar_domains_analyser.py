from proactive.models import SimilarDomain
from .get_whois import WHOIS_ANALYSER
from .geoip.tld_with_country import TLD_COUNTRY
from .geoip.get_geoip import GEOIP
from .ACL.check_acl import ACL_CHECKER
from .certificates.tls_certificates import TLS_CERTIFICATE_ANALYSER

class SimilarDomainAnalyser:
    def analyse(self, similar_domain:SimilarDomain):
        '''
        En esta función se orquesta el analizador de los dominios para determinar
        si es phishing o no
        '''
        # 1. Analizamos si el dominio está blacklist / whitelist
        # 1.1 Comprobamos si está en la whitelist
        if ACL_CHECKER.is_whitelisted(similar_domain): 
            similar_domain.is_phishing = False
            return
        # 1.2 Comprobamos si está en la blacklist
        if ACL_CHECKER.is_blacklisted(similar_domain):
            similar_domain.is_phishing = True
            return

        # 2. Analizamos el registro WHOIS
        WHOIS_ANALYSER.analyze_whois(similar_domain)

        # 3. Analizamos la geolocalización
        # 3.1 Obtenemos el país asociado al TLD
        TLD_COUNTRY.get_country_from_tld(similar_domain)
        # 3.2 Obtenemos los países asociados a las IPs del dominio similar
        GEOIP.get_domain_country(similar_domain)

        # 4. Comprobamos el certificado TLS del dominio
        TLS_CERTIFICATE_ANALYSER.analyse_tls_certificate(similar_domain)

DOMAIN_ANALYSER = SimilarDomainAnalyser()
