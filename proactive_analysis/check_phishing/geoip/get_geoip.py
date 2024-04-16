import requests
import socket

ENDPOINT = "http://ip-api.com/json"
PARAMS = "?fields=country"

class GeoIP:
    '''
    Clase para geolocalizar las IPs asociadas a un dominio.
    '''
    # Dado un dominio, devuelve los países asociados a las IPs
    def get_domain_country(self, domain: str) -> set[str]:
        # Obtenemos las IPs
        ips = self.__resolve(domain)
        # Obtenemos los países
        countries = set(self.__get_country(ip) for ip in ips if ip)
        return countries
    
    def __get_country(self, ip):
        # Definimos la URL para la petición
        url = f"http://ip-api.com/json/{ip}?fields=country"
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
        
    def __resolve(self, domain: str) -> list[str]:
        # Obtenemos las IPs asociadas al dominio
        try:
            return list(set(socket.gethostbyname_ex(domain)[2]))
        except socket.gaierror:
            return []

GEOIP = GeoIP()

# Example usage
if __name__ == "__main__":
    domain_name = "microsoft.com"
    countries_name = GEOIP.get_domain_country(domain_name)
    print(f"Countries associated with {domain_name}: {countries_name}")
