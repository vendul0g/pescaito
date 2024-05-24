from proactive.models import SimilarDomain
from .get_whois import WHOIS_ANALYSER, WHOIS_PARSER
from .geoip.tld_with_country import TLD_COUNTRY
from .geoip.get_geoip import GEOIP
from .ACL.check_acl import ACL_CHECKER
from .certificates.tls_certificates import TLS_CERTIFICATE_ANALYSER, TLS_PARSER
from .redirections import REDIRECT_ANALYSER
from .html_analyser import HTML_ANALYSER

# Variables globales
HTTP_PORT = 80
HTTPS_PORT = 443


class SimilarDomainAnalyser:
    def analyse(self, similar_domain: SimilarDomain):
        """
        En esta función se orquesta el analizador de los dominios para determinar
        si es phishing o no
        """
        # 1. Analizamos si el dominio está blacklist / whitelist
        # 1.1 Comprobamos si está en la whitelist
        if ACL_CHECKER.is_whitelisted(similar_domain.name):
            similar_domain.is_phishing = False
            return
        # 1.2 Comprobamos si está en la blacklist
        if ACL_CHECKER.is_blacklisted(similar_domain.name):
            similar_domain.is_phishing = True
            return

        # 2. Analizamos el registro WHOIS
        whois_response = WHOIS_ANALYSER.analyse_whois(similar_domain.name)
        WHOIS_PARSER.parse_results(whois_response, similar_domain)

        # 3. Analizamos la geolocalización
        # 3.1 Obtenemos el país asociado al TLD
        country = TLD_COUNTRY.get_country_from_tld(similar_domain.name)
        similar_domain.tld_country = country
        # 3.2 Obtenemos los países asociados a las IPs del dominio similar
        countries = GEOIP.get_domain_country(similar_domain.name)
        similar_domain.ip_countries = countries

        # 4. Comprobamos el certificado TLS del dominio
        info_current_cert, oldest_certificate_date = (
            TLS_CERTIFICATE_ANALYSER.analyse_tls_certificate(similar_domain.name)
        )
        TLS_PARSER.similar_domain_parser(
            similar_domain, info_current_cert, oldest_certificate_date
        )

        # 5. Comprobamos las redirecciones HTTP del dominio
        # TODO mejora: que analice tanto el puerto 80 como el 443 haya o no certificado
        port = HTTPS_PORT if similar_domain.is_certificate_tls else HTTP_PORT
        (
            similar_domain.final_url,
            similar_domain.is_redirect_same_domain,
            similar_domain.has_redirect_special_chars,
        ) = REDIRECT_ANALYSER.analyse_redirects(
            similar_domain.name,
            port,
        )

        # 6. Comprobamos el contenido HTML de la página
        HTML_ANALYSER.analyse_html(similar_domain.name, similar_domain.orig_domain_name)
        



SIMILAR_DOMAIN_ANALYSER = SimilarDomainAnalyser()
