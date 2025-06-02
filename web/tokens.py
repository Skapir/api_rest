import secrets
from .models import UserToken
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

# Esta vista se encarga de mostrar la lista de tokens generados por el usuario
# y permite la creación de nuevos tokens.
class TokenListView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        # Filtra los tokens del usuario autenticado y ordena por fecha de creación+
        
        tokens = UserToken.objects.filter(user=request.user).order_by('-created_at')
        paginator = Paginator(tokens, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'web/token/token_panel.html', { 'page_obj': page_obj})

# Esta vista se encarga de la creación de nuevos tokens para el usuario.
# Al crear un nuevo token, se invalidan los tokens anteriores.
class TokenCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        UserToken.objects.filter(user=request.user).update(is_active=False)

        token_obj = UserToken.objects.create(
            user=request.user,
            token=secrets.token_hex(20),
            is_active=True
        )

        messages.success(request, "Se ha generado un nuevo token.")
        return redirect('token_panel')

