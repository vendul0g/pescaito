from proactive.models import SimilarDomain

class DomainAnalyser:
    def analyse(self, domain:SimilarDomain):
        '''
        En esta función se orquesta el analizador de los dominios para determinar
        si es phishing o no
        '''
        domain.is_phishing = True


DOMAIN_ANALYSER = DomainAnalyser()