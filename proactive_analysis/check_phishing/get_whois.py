import socket
import re
from proactive.models import SimilarDomain  # Django


class ServerCluster:
    def __init__(self):
        # TODO Mejora: poner las listas en un fichero e implementar una clase cargador y actualizador. También se puede randomizar el orden de los servidores
        self.whois_servers = {
            "com": [
                "whois.verisign-grs.com",
                "whois.crsnic.net",
                "whois.markmonitor.com",
                "whois.crazydomains.com",
                "whois.tecnocratica.net",
                "whois.enom.com",
            ],
            "net": ["whois.verisign-grs.com", "whois.crsnic.net", "whois.worldnic.com"],
            "org": [
                "whois.pir.org",
                "whois.publicinterestregistry.net",
                "whois.godaddy.com",
            ],
            "info": ["whois.afilias.info", "whois.afilias.net", "whois.godaddy.com"],
            "biz": ["whois.neulevel.biz", "whois.biz", "whois.godaddy.com"],
            "us": ["whois.nic.us", "whois.nic.us", "whois.godaddy.com"],
            "uk": ["whois.nic.uk", "whois.nic.uk", "ukwhois.centralnic.com"],
            "ca": ["whois.cira.ca", "whois.ca.fury.ca", "whois.co.ca"],
            "eu": ["whois.eu", "whois.eu", "whois.eurid.eu"],
            "au": ["whois.auda.org.au", "whois.aunic.net", "whois.ausregistry.net.au"],
            "de": ["whois.denic.de", "whois.denic.de", "de.whois-servers.net"],
            "ru": ["whois.tcinet.ru", "whois.tcinet.ru", "whois.nic.ru"],
            "fr": ["whois.nic.fr", "whois.nic.fr", "whois.afnic.fr"],
            "nl": ["whois.sidn.nl", "whois.sidn.nl", "whois.domain-registry.nl"],
            "br": ["whois.registro.br", "whois.registro.br", "whois.nic.br"],
            "it": ["whois.nic.it", "whois.nic.it", "whois.iit.cnr.it"],
            "es": ["whois.nic.es", "whois.nic.es", "es.whois-servers.net"],
            "se": ["whois.iis.se", "whois.iis.se", "whois.nic-se.se"],
            "jp": ["whois.jprs.jp", "whois.jprs.jp", "whois.nic.ad.jp"],
            "ch": ["whois.nic.ch", "whois.nic.ch", "whois.switch.ch"],
            "no": ["whois.norid.no", "whois.norid.no", "no.whois-servers.net"],
            "at": ["whois.nic.at", "whois.nic.at", "at.whois-servers.net"],
            "dk": [
                "whois.dk-hostmaster.dk",
                "whois.dk-hostmaster.dk",
                "whois.sunet.se",
            ],
            "fi": ["whois.fi", "whois.fi", "whois.ficora.fi"],
            "be": ["whois.dns.be", "whois.dns.be", "whois.nic.be"],
            "pl": ["whois.dns.pl", "whois.dns.pl", "whois.nic.pl"],
            "cz": ["whois.nic.cz", "whois.nic.cz", "whois.iana.org"],
            "io": ["whois.nic.io", "whois.nic.io", "whois.afrinic.net"],
            "club": ["whois.nic.club", "whois.nic.club", "whois.iana.org"],
            "online": ["whois.nic.online", "whois.nic.online", "whois.centralnic.com"],
        }

    def mostrar_alerta(self):
        print(r" _______  _        _______  _______ _________ _  _  _ ")
        print(r"(  ___  )( \      (  ____ \(  ____ )\__   __/( )( )( )")
        print(r"| (   ) || (      | (    \/| (    )|   ) (   | || || |")
        print(r"| (___) || |      | (__    | (____)|   | |   | || || |")
        print(r"|  ___  || |      |  __)   |     __)   | |   | || || |")
        print(r"| (   ) || |      | (      | (\ (      | |   (_)(_)(_)")
        print(r"| )   ( || (____/\| (____/\| ) \ \__   | |    _  _  _ ")
        print(r"|/     \|(_______/(_______/|/   \__/   )_(   (_)(_)(_)")
        print(r"                                                      ")

    def get_server_from_tld(self, domain_name: str) -> list[str]:
        # Sacamos el TLD
        tld = domain_name.split(".")[-1]
        # Obtenemos los servidores WHOIS para el TLD
        servers = self.whois_servers.get(tld, [])
        # Devolvemos la respuesta según el caso
        if not servers:
            self.mostrar_alerta()
            print(f"--> No hay servidores Whois para el dominio {domain_name}")
            return []
        return servers


class WhoisResultParser:
    def parse_results(self, whois_answer: str, similar_domain: SimilarDomain) -> bool:
        # Mostramos la respuesta
        # print("======================= RESPONSE ========================")
        # print(whois_answer)
        # print("=========================================================")

        # Utiliza expresiones regulares para extraer fechas de la información WHOIS
        results = {}
        patterns = {
            "creation_date": r"Creation Date: ([\d\-TZ:]+)",
            "updated_date": r"Updated Date: ([\d\-TZ:]+)",
            "expiration_date": r"Registry Expiry Date: ([\d\-TZ:]+)",
        }
        # Recorremos los patrones y extraemos la información
        for key, pattern in patterns.items():
            match = re.search(pattern, whois_answer)
            if match:
                results[key] = match.group(1)
                # Asignamos el valor al atributo
                setattr(similar_domain, key, results[key])

        # Comprobamos si se ha obtenido alguna fecha
        if not results:
            return False
        return True


class WhoisAnalyser:
    def __init__(self):
        self.server_cluster = ServerCluster()
        self.whois_parser = WhoisResultParser()

    def analyse_whois(self, similar_domain_name: str) -> str:
        # Obtenemos los servidores (según el TLD)
        tld_servers = self.server_cluster.get_server_from_tld(similar_domain_name)

        # Intenta consultar en cada servidor WHOIS hasta obtener una respuesta válida
        for server in tld_servers:
            response = self.__request_whois_servers(server, similar_domain_name)
            # Hacemos el análisis de la respuesta
            return response

        # Si ningún servidor WHOIS devuelve una respuesta válida
        self.server_cluster.mostrar_alerta()
        print(f"---> No se pudo obtener información WHOIS para {similar_domain_name}")
        return False

    def __request_whois_servers(self, server: str, similar_domain_name: str) -> str:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((server, 43))
                s.sendall((similar_domain_name + "\r\n").encode("utf-8"))
                response = b""
                while True:
                    data = s.recv(4096)
                    response += data
                    if not data:
                        break
                # Devolvemos la respuesta
                return response.decode("utf-8")
        except socket.timeout:
            print(f"Tiempo de espera excedido para el servidor {server}")
        except socket.error as e:
            print(f"Error al conectar con el servidor {server}: {e}")


WHOIS_ANALYSER = WhoisAnalyser()
WHOIS_PARSER = WhoisResultParser()
