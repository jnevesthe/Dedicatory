import requests
from .models import SiteAccess

class AccessLogMiddleware:
    """
    Middleware para registrar todos os acessos ao site.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            path = request.path

            # Consulta a localização do IP (usando ipapi.co)
            country = ''
            city = ''
            try:
                r = requests.get(f'https://ipapi.co/{ip}/json/', timeout=1)
                data = r.json()
                country = data.get('country_name', '')
                city = data.get('city', '')
            except:
                pass

            # Salva no banco
            SiteAccess.objects.create(
                ip=ip,
                user_agent=user_agent,
                path=path,
                country=country,
                city=city
            )
        except Exception as e:
            # Evita quebrar o site caso dê erro
            print("Erro ao salvar acesso:", e)

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip