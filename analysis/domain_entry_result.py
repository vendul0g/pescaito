'''
Definición de la clase DomainEntryResult
Representa el resultado del análisis de un dominio
'''
class DomainEntryResult:
    def __init__(self, name: str, ip: list[str]):
        self.name = name
        self.ip = ip

    def __str__(self):
        return f"Domain: {self.name} - IPs: {self.ip}"