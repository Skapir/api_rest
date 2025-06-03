from django.db import models
from django.utils import timezone
import secrets
from django.contrib.auth.models import User

# esta modelo se utiliza para almacenar los tokens de restablecimiento de contraseña
# y los correos electrónicos asociados a ellos. Esto es útil para verificar la validez
class PasswordResetRequest(models.Model):
    email = models.EmailField(verbose_name="Correo Electrónico")
    ip_address = models.GenericIPAddressField(verbose_name="Dirección IP")
    timestamp = models.DateTimeField(default=timezone.now,verbose_name="Fecha de Solicitud")

    class Meta:
        verbose_name = "Solicitud de Recuperación"
        verbose_name_plural = "Solicitudes de Recuperación"
        
    def __str__(self):
        return f"{self.email} - {self.ip_address} - {self.timestamp}"

# esta modelo se utiliza para almacenar los tokens de usuario y su fecha de expiración
# Esto es útil para la autenticación de usuarios y la gestión de sesiones   
class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens")
    token = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    total_requests = models.PositiveIntegerField(default=0)
    solicitudes_realizadas = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'web_usertoken'  # <- importante
        managed = False             # <- muy importante

    def __str__(self):
        return f"{self.user.username} - {self.token}"

    def regenerate_token(self):
        self.token = secrets.token_hex(20)
        self.created_at = timezone.now()
        self.total_requests = 0
        self.save()


class paciente_api(models.Model):
    hi_nreg = models.CharField(max_length=20, primary_key=True)
    hi_autase = models.CharField(max_length=100)
    hi_nombre = models.CharField(max_length=255)
    hi_fecnac = models.DateField()
    hi_ubinac = models.CharField(max_length=100)
    hi_direcc = models.CharField(max_length=255)
    hi_sexo = models.CharField(max_length=10)
    hi_ndocum = models.CharField(max_length=20)
    hi_estciv = models.CharField(max_length=20)
    hi_cpolic = models.CharField(max_length=50)

    class Meta:
        db_table = 'paciente_api'  # Nombre real de la tabla ya creada
        managed = False  # Para que Django no intente crearla