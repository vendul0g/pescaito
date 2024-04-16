import json
import os
from django.conf import settings
from proactive.models import SimilarDomain # Django

DATA_FILE = os.path.join(settings.BASE_DIR, 'proactive_analysis/check_phishing/geoip/', 'tld_country_data.json')

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

    def get_country_from_tld(self, similar_domain: SimilarDomain):
        """
        Recupera la información del país asociado a un TLD dado.
        
        :param tld: Cadena que representa el TLD 
        :return: La cadena correspondiente al país asociado 
        """
        print(DATA_FILE)
        # Comprobamos si está cropeado el TLD
        if '.' in similar_domain.name:
            tld = similar_domain.name.split('.')[-1]
        # Obtenemos el país asociado al TLD del fichero JSON
        country = self.tld_by_country.get(tld.lower())
        if country is None:
            print(f"No se encuentra el país para el TLD dado: {similar_domain}")
        # Asignamos el país al dominio similar
        similar_domain.tld_country = country


TLD_COUNTRY = TLDCountry()