import os
from datetime import datetime
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from proactive.models import SimilarDomain

# Formato de fecha
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Comparaciones
SUSPICIOUS_CREATION_DATE = 2
LETS_ENCRYPT_CA = "Let's Encrypt"
THRESHOLD_DFT_VISUAL_SIMILARITY = 1 * 10**-6
THRESHOLD_DCT_VISUAL_SIMILARITY = 0.01
THRESHOLD_PHISHING = 60
THRESHOLD_PAAS = 5

# Pesos
WEIGHT_CREATION_DATE = 11.2
WEIGHT_IS_TLS_CERTIFICATE = 8.3
WEIGHT_OLDEST_CERTIFICATE = 11.2
WEIGHT_REDIRECT_SAME_DOMAIN = 8.3
WEIGHT_SPECIAL_CHARS = 5.5
WEIGHT_EXTERNAL_LINKS = 2.7
WEIGHT_LOGIN_FORM = 11.2
WEIGHT_BAD_LINKS = 5.5
WEIGHT_VISUAL_SIMILARITY = 22.2
WEIGHT_PAAS = 11.2


class Reporter:
    def report(self, similar_domain: SimilarDomain):
        """
        Función para reportar los resultados del análisis proactivo a organizaciones
        anti-phishing
        """
        print(f"[*] Reporter enviando email de reporte a: {settings.ADMIN_EMAIL, similar_domain.original_domain.admin_email}")

        subject = f"[!] Sistema Proactivo: reporte dominio similar ({similar_domain.name})"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.ADMIN_EMAIL, similar_domain.original_domain.admin_email]

        html_content = f"""
        <html>
        <body>
            <h1>Información recogida:</h1>
            {similar_domain.get_html_content()}
            <br><br><hr><hr>
            <h1>Webs originales:</h1>
        """

        # Attach each image for the original domains
        for idx, url in enumerate(similar_domain.original_domain.urls):
            image_path = os.path.join(
                settings.MEDIA_ROOT,
                f"{url.split('//')[1].replace('.', '_').replace('/', '-')}.png",
            )
            # Adjust size: specify width and/or height
            html_content += f'<p><img src="cid:image{idx}" style="width:600px; height:auto;"></p>'

        # Attach the image for the phishing web
        phishing_image_path = os.path.join(
            settings.MEDIA_ROOT,
            f"{similar_domain.final_url.split('//')[1].replace('.', '_').replace('/', '-')}.png",
        )
        html_content += """
            <hr>
            <h1>Web phishing:</h1>
            <p><img src="cid:image_phishing" style="width:600px; height:auto;"></p>
        </body>
        </html>
        """

        # Create the email message
        msg = EmailMultiAlternatives(subject, "", email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")

        # Attach the images to the email
        for idx, url in enumerate(similar_domain.original_domain.urls):
            image_path = os.path.join(
                settings.MEDIA_ROOT,
                f"{url.split('//')[1].replace('.', '_').replace('/', '-')}.png",
            )
            with open(image_path, "rb") as f:
                msg_image = MIMEImage(f.read())
                msg_image.add_header("Content-ID", f"<image{idx}>")
                msg.attach(msg_image)

        # Attach the phishing image
        with open(phishing_image_path, "rb") as f:
            msg_image = MIMEImage(f.read())
            msg_image.add_header("Content-ID", "<image_phishing>")
            msg.attach(msg_image)

        # Send the email
        msg.send()

    def check_phishing(self, similar_domain: SimilarDomain) -> bool:
        """
        Comprueba si un dominio es phishing o no.
        """
        # Inicializamos el peso
        print(f"[*] Reporter analizando {similar_domain.name}: 0")
        weight = 0.0

        # Fecha compra Whois
        # Convertimos creation_date a datetime
        creation_date = datetime.strptime(similar_domain.creation_date, DATE_FORMAT)
        if (datetime.now().year - creation_date.year) <= SUSPICIOUS_CREATION_DATE:
            weight += WEIGHT_CREATION_DATE
            print(
                f"[+] fecha de creación inferior a {SUSPICIOUS_CREATION_DATE} años - {weight}"
            )

        # Existencia certificado TLS

        if not similar_domain.is_certificate_tls:
            weight += WEIGHT_IS_TLS_CERTIFICATE
            print("[+] No tiene certificado TLS - {weight}")

        # CA certificado TLS
        if similar_domain.tls_certificate_ca == LETS_ENCRYPT_CA:
            weight += WEIGHT_IS_TLS_CERTIFICATE
            print(f"[+] CA del certificado TLS es {LETS_ENCRYPT_CA} - {weight}")

        # Primer certificado TLS
        # Comprobamos si no es None el tls_certificate_oldest_date
        if similar_domain.tls_certificate_oldest_date:
            if (
                datetime.now().year - similar_domain.tls_certificate_oldest_date.year
            ) <= SUSPICIOUS_CREATION_DATE:
                weight += WEIGHT_OLDEST_CERTIFICATE
                print(
                    f"[+] Certificado TLS más antiguo inferior a {SUSPICIOUS_CREATION_DATE} años - {weight}"
                )

        # Redirección al mismo dominio
        if not similar_domain.is_redirect_same_domain:
            weight += WEIGHT_REDIRECT_SAME_DOMAIN
            print(f"[+] Redirección a otro dominio - {weight}")

        # Caracteres especiales URL final
        if similar_domain.has_redirect_special_chars:
            weight += WEIGHT_SPECIAL_CHARS
            print(f"[+] URL final contiene caracteres especiales - {weight}")

        # Número de recursos externos vs internos
        if similar_domain.external_links > similar_domain.internal_links:
            weight += WEIGHT_EXTERNAL_LINKS
            print(f"[+] Más enlaces externos que internos - {weight}")

        # Existencia de formulario de login
        if similar_domain.is_login_form:
            weight += WEIGHT_LOGIN_FORM
            print(f"[+] Existe formulario de login - {weight}")

        # Número de enlaces maliciosos
        if len(similar_domain.bad_links) > 0:
            weight += WEIGHT_BAD_LINKS
            print(f"[+] Enlaces maliciosos detectados - {weight}")

        # Similaridad visual
        for r in similar_domain.visual_similarity:
            if (
                r["dft_web"] < THRESHOLD_DFT_VISUAL_SIMILARITY
                or r["dct_web"] < THRESHOLD_DCT_VISUAL_SIMILARITY
                or r["favicon"] < THRESHOLD_DCT_VISUAL_SIMILARITY
            ):
                weight += WEIGHT_VISUAL_SIMILARITY
                print(f"[+] Similitud visual detectada - {weight}")
                break

        # PaaS
        if similar_domain.paas_tools > THRESHOLD_PAAS:
            weight += WEIGHT_PAAS
            print("[+] Herramientas PaaS detectadas - {weight}")

        # Actualizamos la información del dominio parecido
        similar_domain.total_weight = weight

        if weight >= THRESHOLD_PHISHING:
            similar_domain.is_phishing = True

        # Devolvemos si es phishing o no
        print(f"[+] Peso total: {weight} --> phishing? {similar_domain.is_phishing}")
        return similar_domain.is_phishing


REPORTER = Reporter()
