from django.shortcuts import render
from django.urls import resolve, Resolver404

class Force404Middleware:
    """
    Força qualquer URL inválida a mostrar a página 404 mesmo com DEBUG=True
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Tenta resolver a URL
            resolve(request.path)
        except Resolver404:
            # Se não existir, mostra a página 404
            return render(request, "404.html", status=404)

        # Se existir, segue normalmente
        response = self.get_response(request)
        return response
