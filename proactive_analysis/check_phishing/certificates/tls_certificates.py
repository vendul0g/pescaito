import ssl
import socket
from datetime import datetime
import pytz
from pycrtsh import Crtsh

# Interface para la verificación de certificados
class ICertificateChecker:
    def get_certificate(self):
        pass

    def extract_certificate_info(self, cert):
        pass

# Clase concreta para la verificación de certificados SSL
class SSLCertificateChecker(ICertificateChecker):
    """
    Clase para manejar la verificación y obtención de detalles de certificados SSL de un dominio.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.context = ssl.create_default_context()

    def get_certificate(self) -> dict:
        """
        Obtiene el certificado SSL actual del dominio.
        """
        try:
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
            return cert
        except Exception as e:
            print(f"Error al conectar con {self.domain} para obtener el certificado SSL: {e}")
            return None

    def extract_certificate_info(self, cert: dict) -> dict:
        """
        Extrae información del certificado SSL como el nombre de la CA y la fecha de creación.
        """
        if cert:
            issuer = dict(x[0] for x in cert["issuer"])
            ca_name = issuer.get("organizationName", "Desconocido")
            utc_zone = pytz.utc
            valid_from = utc_zone.localize(datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z"))
            return {"CA": ca_name, "creation_date": valid_from}
        return {"certificate": "Not found"}

# Clase para la verificación de certificados históricos
class CRTSHChecker:
    """
    Clase para manejar la obtención y procesamiento de datos históricos de certificados desde crt.sh.
    """
    def __init__(self, domain):
        self.domain = domain

    def get_historical_certificates(self) -> list:
        """
        Consulta crt.sh para obtener datos históricos de certificados del dominio.
        """
        c = Crtsh()
        certs = c.search(self.domain)
        return certs

    def find_oldest_certificate(self, crt_data: list) -> datetime:
        """
        Encuentra el certificado más antiguo del conjunto de datos obtenidos de crt.sh.
        """
        oldest_certificate_date = None
        for cert in crt_data:
            if oldest_certificate_date is None or cert["not_before"] < oldest_certificate_date:
                oldest_certificate_date = cert["not_before"]
        return oldest_certificate_date

def get_tls_certificate_info(domain):
    """
    Obtiene información del certificado TLS de un dominio, incluyendo detalles actuales y el certificado más antiguo.
    """
    checker = SSLCertificateChecker(domain)
    crt_checker = CRTSHChecker(domain)

    cert = checker.get_certificate()
    current_cert_info = checker.extract_certificate_info(cert)

    crt_data = crt_checker.get_historical_certificates()
    oldest_cert_info = crt_checker.find_oldest_certificate(crt_data)

    cert_info = {
        "current_certificate": current_cert_info,
        "oldest_certificate": oldest_cert_info,
    }

    # Extract the CA issuer name
    ca_issuer = cert_info["current_certificate"]["CA"]

    # Extract the creation date of the current certificate
    current_certificate_date = cert_info["current_certificate"]["creation_date"]

    # Extract the date of the oldest certificate
    oldest_certificate_date = cert_info["oldest_certificate"]

    # Print
    print(f"CA: {ca_issuer}")
    print(f"Current certificate creation date: {current_certificate_date}")
    print(f"Oldest certificate date: {oldest_certificate_date}")

    return cert_info

# Descomentar la siguiente línea para probar la función con un dominio
info = get_tls_certificate_info("legitec.com")
# print(info)
