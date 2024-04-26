 def analyze_external_resources(self):
        '''
        Analiza los recursos externos cargados en el HTML y verifica la ubicación de los scripts.

        :return: Diccionario con información sobre los recursos externos y la ubicación de scripts.
        '''
        soup = BeautifulSoup(self.html, 'html.parser')
        resources = {'external': [], 'internal': [], 'scripts': []}
        tags = soup.find_all(['script', 'link', 'img', 'a'])
        
        for tag in tags:
            src = tag.get('src') or tag.get('href')
            if src:
                full_url = urljoin(self.url, src)
                if urlparse(full_url).netloc != self.domain:
                    resources['external'].append(full_url)
                else:
                    resources['internal'].append(full_url)
            
            if tag.name == 'script' and src:
                resources['scripts'].append(full_url)

        return resources

    def analyze_login_forms(self):
        '''
        Busca formularios de inicio de sesión en el HTML.

        :return: Verdadero si se encuentra un formulario de inicio de sesión, falso de lo contrario.
        '''
        soup = BeautifulSoup(self.html, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            if 'login' in form.get('action', '').lower() or 'password' in str(form):
                return True
        return False

    def analyze_links(self):
        '''
        Analiza las etiquetas <a> para verificar discrepancias entre el texto visible y los dominios en href.

        :return: Lista de etiquetas <a> con discrepancias.
        '''
        soup = BeautifulSoup(self.html, 'html.parser')
        suspicious_links = []
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            href = a['href']
            if href.startswith('http'):
                link_domain = urlparse(href).netloc
                if link_domain != self.domain:
                    suspicious_links.append(href)
                if self.domain not in text and text:
                    suspicious_links.append(f"Text mismatch: {text} in {href}")
        return suspicious_links


# 1. Búsqueda de "href" dentro del HTML
        soup = BeautifulSoup(html, 'html.parser')
        suspicious_links = []
        for a in soup.find_all('a', href=True):
            text = a.get_text(strip=True)
            href = a['href']
            if href.startswith('http'):
                link_domain = urlparse(href).netloc
                if link_domain != domain:
                    suspicious_links.append(href)
                if domain not in text and text:
                    suspicious_links.append(f"Text mismatch: {text} in {href}")