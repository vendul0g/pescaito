from proactive.models import SimilarDomain
from .get_whois import WHOIS_ANALYSER, WHOIS_PARSER
from .geoip.tld_with_country import TLD_COUNTRY
from .geoip.get_geoip import GEOIP
from .ACL.check_acl import ACL_CHECKER
from .certificates.tls_certificates import TLS_CERTIFICATE_ANALYSER, TLS_PARSER
from .redirections import REDIRECT_ANALYSER
from .html_analyser.html_analyse import HTML_ANALYSER
from .visual_analysis.visual_analyser import VISUAL_ANALYSER
from .paas_checker import PAAS_CHECKER

# Variables globales
HTTP_PORT = 80
HTTPS_PORT = 443


class SimilarDomainAnalyser:
    def check_acl(self, similar_domain: SimilarDomain) -> bool:
        """
        Comprueba si el dominio está en una lista negra o blanca.
        """
        # Comprobamos si está en la whitelist
        if ACL_CHECKER.is_whitelisted(similar_domain.name):
            similar_domain.is_whitelisted = True
            return True

        # Comprobamos si está en blacklist
        if ACL_CHECKER.is_blacklisted(similar_domain.name):
            similar_domain.is_blacklisted = True
            return True

        # En caso contrario, no está en ninguna lista
        return False

    def whois(self, similar_domain: SimilarDomain):
        """
        Realiza un análisis WHOIS del dominio similar.
        """
        whois_response = WHOIS_ANALYSER.analyse_whois(similar_domain.name)
        WHOIS_PARSER.parse_results(whois_response, similar_domain)

    def geolocate(self, similar_domain: SimilarDomain):
        """
        Realiza una geolocalización del dominio similar. Tanto del TLD como de las IPs.
        """
        # Obtenemos el país asociado al TLD
        country = TLD_COUNTRY.get_country_from_tld(similar_domain.name)
        similar_domain.tld_country = country

        # Obtenemos los países asociados a las IPs del dominio similar
        countries = GEOIP.get_domain_country(similar_domain.name)
        # print(f"[+] Countries: {countries}")
        similar_domain.ip_countries = countries
        # print(f"[+] IP Countries: {similar_domain.ip_countries}")

    def tls(self, similar_domain: SimilarDomain):
        """
        Realiza un análisis del certificado TLS del dominio similar.
        """
        info_current_cert, oldest_certificate_date = (
            TLS_CERTIFICATE_ANALYSER.analyse_tls_certificate(similar_domain.name)
        )
        TLS_PARSER.similar_domain_parser(
            similar_domain, info_current_cert, oldest_certificate_date
        )

    def redirections(self, similar_domain: SimilarDomain):
        """
        Realiza un análisis de las redirecciones HTTP del dominio similar.
        """
        # TODO mejora: que analice tanto el puerto 80 como el 443 haya o no certificado
        # Obtenemos el puerto (si es HTTP o HTTPS)
        port = HTTPS_PORT if similar_domain.is_certificate_tls else HTTP_PORT
        
        # Analizamos las redirecciones
        (
            similar_domain.final_url,
            similar_domain.is_redirect_same_domain,
            similar_domain.has_redirect_special_chars,
        ) = REDIRECT_ANALYSER.analyse_redirects(
            similar_domain.name,
            port,
        )

    def html(self, similar_domain: SimilarDomain) -> bool:
        """
        Realiza un análisis del contenido HTML del dominio similar.
        """
        # Analizamos el contenido HTML y obtenemos los resultados
        r = HTML_ANALYSER.analyse_html(
            similar_domain.final_url, similar_domain.original_domain.name
        )
        # Asignamos los resultados al dominio similar
        if r:
            similar_domain.internal_links = r["internal_links"]
            similar_domain.external_links = r["external_links"]
            similar_domain.is_login_form = r["is_login_form"]
            similar_domain.is_original_domain = r["is_original_domain"]
            similar_domain.suspicious_links = r["suspicious_links"]
        else:
            print(f"[!] Error con el HTML de {similar_domain.name}")

        # Comprobamos si hay referencias al dominio original ==> phishing
        if similar_domain.is_original_domain:
            similar_domain.is_phishing = True
            print(f"[+] {similar_domain.name} es phishing")
            return True
        return False

    def visually(self, similar_domain: SimilarDomain):
        """
        Realiza un análisis visual del dominio similar.
        """
        results = []
        print(f"[*] URLs: {similar_domain.original_domain.urls}")
        # Recorremos todas las URLs del dominio original para ver si son phishing
        for url in similar_domain.original_domain.urls:
            print(f"[+] Analizando visualmente {similar_domain.final_url} y {url}")
            r = VISUAL_ANALYSER.visual_analysis(similar_domain.final_url, url)
            print(f"--> {r}")
            results.append(r)

        similar_domain.visual_similarity = results
        print(f"[+] Resultados visuales: {similar_domain.visual_similarity}")

    def paas(self, similar_domain: SimilarDomain):
        """
        Realiza un análisis de las herramientas PaaS utilizadas en el dominio similar.
        - GoPhish
        """
        similar_domain.paas_tools = PAAS_CHECKER.check_gophish(similar_domain.final_url)

    def analyse(self, similar_domain: SimilarDomain):
        """
        En esta función se orquesta el analizador de los dominios para determinar
        si es phishing o no
        """
        # 1. Analizamos si el dominio está blacklist / whitelist
        stop = self.check_acl(similar_domain)
        if stop:
            return

        # 2. Analizamos el registro WHOIS
        self.whois(similar_domain)

        # 3. Analizamos la geolocalización
        self.geolocate(similar_domain)

        # 4. Comprobamos el certificado TLS del dominio
        self.tls(similar_domain)

        # 5. Comprobamos las redirecciones HTTP del dominio
        self.redirections(similar_domain)

        # 6. Comprobamos el contenido HTML de la página
        stop = self.html(similar_domain)
        print("[+] Stop: ", stop)
        if stop:
            return
        
        # 7. Hacemos el análisis visual
        self.visually(similar_domain)

        #8. Análisis de PaaS
        self.paas(similar_domain)


SIMILAR_DOMAIN_ANALYSER = SimilarDomainAnalyser()
