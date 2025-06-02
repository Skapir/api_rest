from django.contrib.auth import views as auth_views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views,tokens

# Router para la API
router = DefaultRouter()
router.register(r'pacientes', views.PacienteApiView, basename='pacientes')


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard.as_view(), name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('reportes/', views.reportes, name='reportes'),
    path('usuarios/', views.usuarios, name='usuarios'),

    # 🔐 Token
    path('token/', tokens.TokenListView.as_view(), name='token_panel'),
    path('token/crear/', tokens.TokenCreateView.as_view(), name='token_create'),
    path('token/documentacion/', views.token_documentacion, name='token_documentacion'),
    path('token/estadisticas/', views.estadisticas_tokens, name='estadisticas_tokens'),

    # 👤 Perfil
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),

    # 🔁 Recuperar contraseña
    path('password-reset/', views.CustomPasswordResetView.as_view(template_name='web/auth/password_reset.html'), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='web/auth/password_reset_complete.html'), name='password_reset_complete'),

    # ✅ Incluye las rutas del router API aquí:
    path('api/', include(router.urls)),
]
