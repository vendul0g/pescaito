import os
from django.conf import settings

BLACKLIST_FILE = os.path.join(
    settings.BASE_DIR, "proactive_analysis/check_phishing/ACL/blacklist.txt"
)
WHITELIST_FILE = os.path.join(
    settings.BASE_DIR, "proactive_analysis/check_phishing/ACL/whitelist.txt"
)


class ACLChecker:
    def __init__(self):
        # Inicializa las listas negra y blanca leyendo desde archivos
        self.blacklist = self.__load_domains(BLACKLIST_FILE)
        self.whitelist = self.__load_domains(WHITELIST_FILE)

    def __load_domains(self, file_path: str) -> set:
        """
        Carga los dominios desde un archivo de texto y los retorna como un conjunto.
        Esto permite una búsqueda rápida y eficiente.
        :param file_path: la ruta al archivo de texto con los dominios
        :return: conjunto de dominios
        """
        try:
            with open(file_path, "r", encoding="utf8") as file:
                return set(line.strip() for line in file if line.strip())
        except FileNotFoundError:
            print(f"[!] Error: file {file_path} does not exists.")
            return set()

    def is_whitelisted(self, domain: str) -> bool:
        """
        Verifica si un dominio está en la Whitelist.
        :param domain: el dominio a verificar
        :return: True si el dominio está en la whitelist, False en caso contrario
        """
        return domain in self.whitelist

    def is_blacklisted(self, domain: str) -> bool:
        """
        Verifica si un dominio está en la blacklist.
        :param domain: el dominio a verificar
        :return: True si el dominio está en la blacklist, False en caso contrario
        """
        print(f"Domain: {domain}")
        print(f"Blacklist: {self.blacklist}")
        return domain in self.blacklist


ACL_CHECKER = ACLChecker()
