from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.utils import timezone
from canary.models import Alert
from main.models import Domain

# Create your views here.
def submit(request, token):
    '''
    Método que recibe una alerta y la procesa
    '''
    # Loggeamos la petición
    print(f"[*] Alert: {request}")

    # Obtenemos los valores
    host = request.GET.get("l")
    ref = request.GET.get("r")
    ip = get_client_ip(request)
    date = timezone.now()
    token = request.path.split("/")[2]

    # Recorremos todos los dominios buscando el token correcto
    all_domains = Domain.objects.all()
    for d in all_domains:
        if d.token == token:
            print(f"[*] Domain: {d.name}")

            # Creamos una alerta
            alert = Alert(
                host=host,
                referrer=ref,
                domain=d,
                ip=ip,
                date=date
            )
            alert.save()
            print(f"{alert.get_str_content()}")

            # Enviamos un correo a los administradores
            subject = f"[!] Alerta de clonado - {alert.host} suplantando a {alert.domain.name}"
            message = f"""
            ¡Alerta recibida!
            {alert.get_str_content()}
            """
            recipient_list = [settings.ADMIN_EMAIL, alert.domain.admin_email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

            break

    # Devolvemos un 404
    return render(request, "404.html", status=404)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip