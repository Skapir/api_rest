from rest_framework import serializers
from .models import paciente_api  # Asegúrate que el nombre del modelo coincida

class PacienteApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = paciente_api
        fields = '__all__'  # Puedes cambiar esto por una lista si deseas campos específicos
        