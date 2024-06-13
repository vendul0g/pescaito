import os
import subprocess
from django.conf import settings
from main.models import Domain


class TokenGenerator:
    """
    Clase que se encarga de generar los token canary dado un dominio
    """

    def __obfuscate_js(self, input_file, output_file):
        # Construct the command
        command = [
            settings.JAVASCRIPT_OBFUSCATOR_BIN,
            input_file,
            "--output",
            output_file,
        ]

        # Run the obfuscator
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Error obfuscating JavaScript: {result.stderr}")

        print(f"JavaScript obfuscated successfully: {output_file}")

    def __to_hexadecimal_representation(self, input_string: str) -> str:
        """
        Método para convertir las cadenas de texto en su representación hexadecimal
        """
        hex_representation = "".join(f"\\x{ord(char):02x}" for char in input_string)
        return hex_representation

    def generate_canary_token(self, domain: Domain) -> str:
        """
        Genera un token canary para un dominio, lo guarda en un fichero y devuelve la ruta
        del mismo
        """
        file_content = (
            f"Canary token for: {domain.name}\n{'='*70}\n\n"
            f"Codigo javascript sin ofuscacion\n{'-'*70}\n\n"
        )

        # Generamos el token canary sin ofuscar
        code = (
            f'if (window.location.hostname != "{domain.name}"'
            f'\n    && !window.location.hostname.endsWith(".{domain.name}"))'
            f"\n{{"
            f"\n    var l = location.href;"
            f"\n    var r = document.referrer;"
            f"\n    var m = new Image();"
            f'\n    m.src = "http://{settings.DOMAIN_ALERT_SERVER}/images/{domain.token}/post.jsp?l=" + encodeURI(l) + "&r=" + encodeURI(r);'
            f"\n}}"
            f"\n"
        )

        # Guardamos el código sin ofuscar
        file_path_normal = os.path.join(
            settings.MEDIA_ROOT,
            f"{domain.name.replace('.','_')}_canary_token_normal.js",
        )
        with open(file_path_normal, "w+", encoding="utf-8") as f:
            f.write(code)

        file_content += code + "\n\n"

        # Ofuscamos las cadenas
        name = self.__to_hexadecimal_representation(domain.name)
        cc = self.__to_hexadecimal_representation(settings.DOMAIN_ALERT_SERVER)
        code_str_ob = (
            f'if (window.location.hostname != "{name}"'
            f'\n    && !window.location.hostname.endsWith(".{name}"))'
            f"\n{{"
            f"\n    var l = location.href;"
            f"\n    var r = document.referrer;"
            f"\n    var m = new Image();"
            f'\n    m.src = "http://{cc}/images/{domain.token}/post.jsp?l=" + encodeURI(l) + "&r=" + encodeURI(r);'
            f"\n}}"
            f"\n"
        )

        file_content += (
            f"{'-'*70}\nCadenas ofuscadas\n{'-'*70}\n\n" + code_str_ob + "\n\n"
        )

        # Guardamos el código de las cadenas ofuscadas
        file_path_str = os.path.join(
            settings.MEDIA_ROOT,
            f"{domain.name.replace('.','_')}_canary_token_str_obfuscated.js",
        )
        with open(file_path_str, "w+", encoding="utf-8") as f:
            f.write(code_str_ob)


        # ofuscamos el código 
        file_path_ob = os.path.join(
            settings.MEDIA_ROOT,
            f"{domain.name.replace('.','_')}_canary_token_full_obfuscated.js",
        )
        title = f"{'-'*70}\nCodigo javascript ofuscado\n{'-'*70}\n\n"
        print(f"[+] Obfuscating JavaScript: {file_path_str} to {file_path_ob}")
        self.__obfuscate_js(
            file_path_str,
            file_path_ob,
        )

        # ofuscamos las cadenas del código totalmente ofuscado
        with open(file_path_ob, "r", encoding="utf-8") as f:
            content = f.read()
            content = content.replace(f"{settings.DOMAIN_ALERT_SERVER}", cc)
            content = content.replace(f"{domain.name}", name)
        with open(file_path_ob, "w+", encoding="utf-8") as f:
            f.write(content)

        # añadimos el código ofuscado file_content
        file_content += title + content + "\n\n"

        # Escribimos el contenido en un fichero
        file_name = f"{domain.name.replace('.','_')}_canary_token.txt"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        with open(file_path, "w+", encoding="utf-8") as f:
            f.write(file_content)

        domain.canary_token = f"{settings.MEDIA_URL}{file_name}"
        domain.save()
        print(f"[+] Canary token generated successfully: {file_path}")
        return file_name


TOKEN_GENERATOR = TokenGenerator()
