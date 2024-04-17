import ssl
import socket
from datetime import datetime
import pytz
from pycrtsh import Crtsh
from proactive.models import SimilarDomain

class Certificate:
    """
    Clase para almacenar la información del certificado.
    """
    def __init__(self, ca_name: str, creation_date: datetime):
        self.ca_name = ca_name
        self.creation_date = creation_date

    def __str__(self) -> str:
        return f"CA: {self.ca_name}, Creation Date: {self.creation_date}"

class TLSCertificateChecker:
    """
    Clase para manejar la verificación y obtención de detalles de certificados TLS de un dominio.
    """
    def __init__(self, domain: str, context=None):
        self.domain = domain
        self.context = context if context else ssl.create_default_context()

    def get_certificate(self) -> dict:
        """
        Obtiene el certificado TLS actual del dominio.
        """
        try:
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
            return cert
        except Exception as e:
            print(f"Error al conectar con {self.domain} para obtener el certificado TLS: {e}")
            return None

    def extract_certificate_info(self, cert: dict) -> Certificate:
        """
        Extrae información del certificado TLS como el nombre de la CA y la fecha de creación.
        """
        if cert:
            issuer = dict(x[0] for x in cert["issuer"])
            ca_name = issuer.get("organizationName", "Desconocido")
            utc_zone = pytz.utc
            valid_from = utc_zone.localize(datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z"))
            return Certificate(ca_name, valid_from)
        else:
            return None

class CRTHistoryChecker:
    """
    Clase para manejar la obtención y procesamiento de datos históricos de certificados desde crt.sh.
    """
    def __init__(self, domain, service=None):
        self.domain = domain
        self.service = service if service else Crtsh()

    def get_historical_certificates(self) -> list:
        """
        Consulta crt.sh para obtener datos históricos de certificados del dominio.
        """
        certs = self.service.search(self.domain)
        return certs

    def find_oldest_certificate(self, crt_data: list):
        """
        Encuentra el certificado más antiguo del conjunto de datos obtenidos de crt.sh.
        """
        oldest_certificate_date = None
        for cert in crt_data:
            if oldest_certificate_date is None or cert["not_before"] < oldest_certificate_date:
                oldest_certificate_date = cert["not_before"]
        return oldest_certificate_date

class TLSCertificateAnalyser:
    def analyse_tls_certificate(self, similar_domain: SimilarDomain):
        """
        Obtiene información del certificado TLS de un dominio, incluyendo detalles actuales y el certificado más antiguo.
        """
        tls_checker = TLSCertificateChecker(similar_domain.name)
        crt_history_checker = CRTHistoryChecker(similar_domain.name)

        cert = tls_checker.get_certificate()
        current_cert_info = tls_checker.extract_certificate_info(cert)

        crt_data = crt_history_checker.get_historical_certificates()
        oldest_certificate_date = crt_history_checker.find_oldest_certificate(crt_data)

        # Metemos los resultados en el dominio simiiar
        self.__similar_domain_parser(similar_domain, current_cert_info, oldest_certificate_date)
    
    def __similar_domain_parser(self, similar_domain: SimilarDomain, current_cert_info: Certificate, oldest_certificate_date: datetime):
        # Compruebo que no ha habido errores (None)
        if current_cert_info is None:
            similar_domain.is_certificate_tls = False
            similar_domain.tls_certificate_ca = None
            similar_domain.tls_certificate_creation_date = None
            return

        similar_domain.is_certificate_tls = True
        similar_domain.tls_certificate_ca = current_cert_info.ca_name
        similar_domain.tls_certificate_creation_date = current_cert_info.creation_date
        similar_domain.tls_certificate_oldest_date = oldest_certificate_date

TLS_CERTIFICATE_ANALYSER = TLSCertificateAnalyser()
