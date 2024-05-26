from proactive.models import SimilarDomain
from datetime import datetime

# Formato de fecha
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Comparaciones
SUSPICIOUS_CREATION_DATE = 2
LETS_ENCRYPT_CA = "Let's Encrypt"
THRESHOLD_VISUAL_SIMILARITY = 1 * 10**-6
THRESHOLD_PHISHING = 70
THRESHOLD_PAAS = 5

# Pesos
WEIGHT_CREATION_DATE = 11.2
WEIGHT_IS_TLS_CERTIFICATE = 8.3
WEIGHT_OLDEST_CERTIFICATE = 11.2
WEIGHT_REDIRECT_SAME_DOMAIN = 8.3
WEIGHT_SPECIAL_CHARS = 5.5
WEIGHT_EXTERNAL_LINKS = 2.7
WEIGHT_LOGIN_FORM = 11.2
WEIGHT_BAD_LINKS = 5.5
WEIGHT_VISUAL_SIMILARITY = 22.2
WEIGHT_PAAS = 11.2


class Reporter:
    def check_phishing(self, similar_domain: SimilarDomain) -> bool:
        """
        Comprueba si un dominio es phishing o no.
        """
        # Inicializamos el peso
        weight = 0.0

        # Fecha compra Whois
        # Convertimos creation_date a datetime
        creation_date = datetime.strptime(similar_domain.creation_date, DATE_FORMAT)
        if (datetime.now().year - creation_date.year) <= SUSPICIOUS_CREATION_DATE:
            weight += WEIGHT_CREATION_DATE

        # Existencia certificado TLS

        if similar_domain.is_certificate_tls:
            weight += WEIGHT_IS_TLS_CERTIFICATE

        # CA certificado TLS
        if similar_domain.tls_certificate_ca == LETS_ENCRYPT_CA:
            weight += WEIGHT_IS_TLS_CERTIFICATE

        # Primer certificado TLS
        if (
            datetime.now().year - similar_domain.tls_certificate_oldest_date.year
        ) <= SUSPICIOUS_CREATION_DATE:
            weight += WEIGHT_OLDEST_CERTIFICATE

        # Redirección al mismo dominio
        if not similar_domain.is_redirect_same_domain:
            weight += WEIGHT_REDIRECT_SAME_DOMAIN

        # Caracteres especiales URL final
        if similar_domain.has_redirect_special_chars:
            weight += WEIGHT_SPECIAL_CHARS

        # Número de recursos externos vs internos
        if similar_domain.external_links > similar_domain.internal_links:
            weight += WEIGHT_EXTERNAL_LINKS

        # Existencia de formulario de login
        if similar_domain.is_login_form:
            weight += WEIGHT_LOGIN_FORM

        # Número de enlaces maliciosos
        if len(similar_domain.bad_links) > 0:
            weight += WEIGHT_BAD_LINKS

        # Similaridad visual
        for r in similar_domain.visual_similarity:
            if (
                r["dft_web"] < THRESHOLD_VISUAL_SIMILARITY
                or r["dct_web"] < THRESHOLD_VISUAL_SIMILARITY
                or r["favicon"] < THRESHOLD_VISUAL_SIMILARITY
            ):
                weight += WEIGHT_VISUAL_SIMILARITY
                break

        # PaaS
        if similar_domain.paas_tools > THRESHOLD_PAAS:
            weight += WEIGHT_PAAS

        # Actualizamos la información del dominio parecido
        similar_domain.total_weight = weight

        if weight > THRESHOLD_PHISHING:
            similar_domain.is_phishing = True

        # Devolvemos si es phishing o no
        return similar_domain.is_phishing


REPORTER = Reporter()
