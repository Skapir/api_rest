from django.contrib import admin
from .models import PasswordResetRequest
from .models import UserToken

@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('email',)
    ordering = ('-timestamp',)
    readonly_fields = ('email', 'ip_address', 'timestamp')

    def has_add_permission(self, request):
        # No permitir añadir manualmente desde admin
        return False

    def has_change_permission(self, request, obj=None):
        # No permitir editar registros
        return False
    
@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at", "total_requests", "is_active")
    search_fields = ("user__username", "token")

