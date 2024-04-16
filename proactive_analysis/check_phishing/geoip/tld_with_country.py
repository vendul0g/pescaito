import json
from sys import argv

DATA_FILE = 'tld_country_data.json'

class TLDCountry:
    def __init__(self):
        """
        Inicializamos la clase cargando el fichero JSON con los datos de
        TLD y países.
        """
        try:
            with open(DATA_FILE, 'r', encoding='utf8') as file:
                self.tld_by_country = json.load(file)
        except FileNotFoundError:
            print(f"Data file {DATA_FILE} not found.")
            exit(1)
        except json.JSONDecodeError:
            print(f"Data file {DATA_FILE} is not a valid JSON.")
            exit(1)

    def get_country_from_tld(self, tld: str) -> str:
        """
        Recupera la información del país asociado a un TLD dado.
        
        :param tld: Cadena que representa el TLD 
        :return: La cadena correspondiente al país asociado 
        """
        country = self.tld_by_country.get(tld.lower())
        if country is None:
            raise ValueError(f"No se encuentra el país para el TLD dado: {tld}")
        return country

if __name__ == "__main__":
    tld = argv[1]
    tld_country = TLDCountry()
    country = tld_country.get_country_from_tld(tld)
    print(f"País asociado al TLD {tld}: {country}")