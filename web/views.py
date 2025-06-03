from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import PasswordResetConfirmView , PasswordResetView
from django.urls import reverse_lazy
from datetime import timedelta
from .models import PasswordResetRequest,UserToken,paciente_api
from django.utils import timezone
from rest_framework import viewsets,filters, status
from .serializers import PacienteApiSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from .authentication import CustomTokenAuthentication
from rest_framework.response import Response


# Esta clase se encarga de la vista de confirmación del restablecimiento de contraseña
# y se utiliza para personalizar el comportamiento de la vista.
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'web/auth/password_reset_confirm.html' 
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        messages.success(self.request, "🎯 Contraseña actualizada correctamente.")
        return super().form_valid(form)
    def form_invalid(self, form):
        # Aquí capturamos los errores del formulario
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)
    
# Esta clase se encarga de la vista de restablecimiento de contraseña y se utiliza para
# personalizar el comportamiento de la vista.
class CustomPasswordResetView(PasswordResetView):
    template_name = 'web/auth/password_reset.html'
    success_url = reverse_lazy('password_reset')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        ip = self.request.META.get('REMOTE_ADDR')

        # Verificamos si el correo existe en la base de datos de usuarios
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "El correo electrónico no está registrado.")
            return self.form_invalid(form)

        # Limitar cantidad de solicitudes
        limit_time = timezone.now() - timedelta(hours=1)
        requests_count = PasswordResetRequest.objects.filter(email=email, timestamp__gte=limit_time).count()

        if requests_count >= 3:
            messages.error(self.request, "Has superado el límite de solicitudes, intenta más tarde.")
            return self.form_invalid(form)

        # Registrar la solicitud
        PasswordResetRequest.objects.create(email=email, ip_address=ip)

        # Si todo está OK
        messages.success(self.request, "Se ha enviado un enlace de recuperación a tu correo electrónico.")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)
    

# Esta clase se encarga de la vista del dashboard y se utiliza para mostrar información
# relacionada con el usuario autenticado. Se utiliza el decorador LoginRequiredMixin
class dashboard(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        token = UserToken.objects.filter(user=request.user,is_active=True).first()
        context = {
            'token': token,
            "solicitudes": token.solicitudes_realizadas if token else 0,
            "ultima_solicitud": token.updated_at if token else "Sin uso",
        }
        return render(request, 'web/dashboard.html',context)

# Esta clase se encarga de la vista de inicio y se utiliza para mostrar la página principal
# de la aplicación. No requiere autenticación.
class PacienteApiView(viewsets.ReadOnlyModelViewSet):
    queryset = paciente_api.objects.all()
    serializer_class = PacienteApiSerializer
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['hi_ndocum']

    def list(self, request, *args, **kwargs):
        # Validar token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Token '):
            token = auth_header.split('Token ')[1].strip()
            try:
                user_token = UserToken.objects.get(token=token, is_active=True)
                user_token.total_requests += 1
                user_token.save()
            except UserToken.DoesNotExist:
                return Response({'detail': 'Token inválido o inactivo.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Filtro aplicado al queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Si no hay resultados, mostrar mensaje personalizado
        if not queryset.exists():
            return Response({'detail': 'Paciente no encontrado con ese DNI.'}, status=status.HTTP_404_NOT_FOUND)

        # Si existe al menos un resultado, continuar flujo normal
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'web/index.html')

@login_required
def reportes(request):
    return render(request, 'web/reportes.html')

@login_required
def usuarios(request):
    return render(request, 'web/usuarios.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('register')

        # Crear el usuario
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        messages.success(request, "¡Cuenta creada exitosamente! Ahora inicia sesión.")
        return redirect('register')  # o redirigir al login

    return render(request, 'web/auth/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, "Sesión iniciada correctamente.")
            return redirect('dashboard')  # Cambiar luego a tu vista privada
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('login')

    return render(request, 'web/auth/login.html')

def logout_view(request):
    logout(request)
    #messages.success(request, "Sesión cerrada correctamente.")
    return redirect('index')

@login_required
def token_documentacion(request):
    LENGUAJES_DISPONIBLES = [
    {"nombre": "python", "icono": "🐍"},
    {"nombre": "java", "icono": "☕"},
    {"nombre": "vb", "icono": "🖥️"},
    {"nombre": "php", "icono": "🐘"},
    {"nombre": "javascript", "icono": "📟"},
    ]
    return render(request, 'web/token/token_documentacion.html',{'lenguajes': LENGUAJES_DISPONIBLES})

@login_required
def perfil_usuario(request):
    user = request.user
    abrir_modal = False
    modal_messages = []

    if request.method == 'POST':
        if 'password_form' in request.POST:
            actual = request.POST.get('actual')
            nueva = request.POST.get('nueva')
            repetir = request.POST.get('repetir')

            if not user.check_password(actual):
                modal_messages.append("❌ La contraseña actual no es correcta.")
                abrir_modal = True
            elif nueva != repetir:
                modal_messages.append("❌ Las nuevas contraseñas no coinciden.")
                abrir_modal = True
            elif len(nueva) < 6:
                modal_messages.append(" ❌ La nueva contraseña debe tener al menos 6 caracteres.")
                abrir_modal = True
            else:
                user.set_password(nueva)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, "¡Contraseña actualizada con éxito!")
                return redirect('perfil_usuario')

    return render(request, 'web/usuario/perfil.html', {
        'usuario': user,
        'abrir_modal': abrir_modal,
        'modal_messages': modal_messages
    })

@login_required
def cambiar_contrasena(request):
    #if request.method == "POST":
        # = CustomPasswordChangeForm(request.user, request.POST)
       # if form.is_valid():
          #  user = form.save()
          #  update_session_auth_hash(request, user)  # Mantiene la sesión activa
           # messages.success(request, "Tu contraseña ha sido cambiada exitosamente.")
          #  return redirect('perfil_usuario')
        #else:
           # messages.error(request, "Por favor corrige los errores.")
   # else:
       # form = CustomPasswordChangeForm(request.user)

    return render(request, 'web/usuario/cambiar_contrasena.html')#, {'form': form})

@staff_member_required
def estadisticas_tokens(request):
    hoy = timezone.now().date()
    hace_30 = hoy - timezone.timedelta(days=30)

    # Agrupamos por fecha (sólo fecha, sin hora)
    qs = (
        UserToken.objects
            .filter(created_at__date__gte=hace_30)          # ajusta el campo timestamp
            .extra({'dia': "date(created_at)"})
            .values('dia')
            .annotate(cantidad=Count('id'))
            .order_by('dia')
    )
    labels = [item['dia'].strftime('%Y-%m-%d') for item in qs]
    data   = [item['cantidad']             for item in qs]

    return render(request,
                  'web/token/estadisticas.html',
                  {
                    'labels': labels,
                    'data': data,
                  })