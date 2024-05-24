from bs4 import BeautifulSoup

class LoginChecker:
    '''
    Clase para comprobar si una página web contiene un formulario 
    de inicio de sesión y ver la URL donde se manda el formulario
    '''

    def check_login(self, html: str) -> tuple:
        '''
        Método para comprobar si una página web contiene un formulario de 
        inicio de sesión
        '''
        # Parseamos el HTML
        soup = BeautifulSoup(html, "html.parser")

        # Buscamos los formularios de inicio de sesión
        login_forms = soup.find_all('form')

        # Imprimimos los resultados
        print(f"Login forms: {len(login_forms)}")

        # Devolvemos el resultado
        return len(login_forms)>0

LOGIN_CHECKER = LoginChecker()