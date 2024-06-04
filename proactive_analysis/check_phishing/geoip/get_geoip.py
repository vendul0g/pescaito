import socket
import requests

ENDPOINT = "http://ip-api.com/json"
PARAMS = "?fields=country"

class GeoIP:
    '''
    Clase para geolocalizar las IPs asociadas a un dominio.
    '''
    def get_domain_country(self, similar_domain_name: str) -> list[str]:
        # Obtenemos las IPs
        ips = self.__resolve(similar_domain_name)
        # Obtenemos los países
        countries = set(self.__get_country(ip) for ip in ips if ip)
        # Convertimos el conjunto a lista para ser compatible con JSONField
        return list(countries)
    
    def __get_country(self, ip: str) -> str:
        # Definimos la URL para la petición
        url = f"{ENDPOINT}{ip}{PARAMS}"
        # Realizamos la petición
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Controlamos los errores
            # Obtenemos el JSON
            data = response.json()
            # Devolvemos el país
            return data.get('country', 'Country not found')
        except requests.RequestException as e:
            return f"Error retrieving geolocation: {str(e)}"
        
    def __resolve(self, domain: str) -> list:
        # Obtenemos las IPs asociadas al dominio
        try:
            return socket.gethostbyname_ex(domain)[2]
        except socket.gaierror:
            return []

GEOIP = GeoIP()
