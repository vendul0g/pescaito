import ssl
import socket
from datetime import datetime
import pytz
from pycrtsh import Crtsh

class Certificate:
    """
    Clase para almacenar la información del certificado.
    """
    def __init__(self, ca_name: str, creation_date: datetime):
        self.ca_name = ca_name
        self.creation_date = creation_date

    def __str__(self):
        return f"CA: {self.ca_name}, Creation Date: {self.creation_date}"

class TLSCertificateChecker:
    """
    Clase para manejar la verificación y obtención de detalles de certificados TLS de un dominio.
    """
    def __init__(self, domain: str, context=None):
        self.domain = domain
        self.context = context if context else ssl.create_default_context()

    def get_certificate(self):
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

    def extract_certificate_info(self, cert):
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

    def get_historical_certificates(self):
        """
        Consulta crt.sh para obtener datos históricos de certificados del dominio.
        """
        certs = self.service.search(self.domain)
        return certs

    def find_oldest_certificate(self, crt_data):
        """
        Encuentra el certificado más antiguo del conjunto de datos obtenidos de crt.sh.
        """
        oldest_certificate_date = None
        for cert in crt_data:
            if oldest_certificate_date is None or cert["not_before"] < oldest_certificate_date:
                oldest_certificate_date = cert["not_before"]
        return oldest_certificate_date

class TLSCertificateAnalyser:
    @staticmethod
    def analyse_tls_certificate(domain: str):
        """
        Obtiene información del certificado TLS de un dominio, incluyendo detalles actuales y el certificado más antiguo.
        """
        tls_checker = TLSCertificateChecker(domain)
        crt_history_checker = CRTHistoryChecker(domain)

        cert = tls_checker.get_certificate()
        current_cert_info = tls_checker.extract_certificate_info(cert)

        crt_data = crt_history_checker.get_historical_certificates()
        oldest_certificate_date = crt_history_checker.find_oldest_certificate(crt_data)

        print(current_cert_info)
        print(f"Oldest certificate date: {oldest_certificate_date}")

        return current_cert_info, oldest_certificate_date

# Test
if __name__ == "__main__":
    _domain = "legitec.com"
    TLSCertificateAnalyser.analyse_tls_certificate(_domain)
