# Generated by Django 5.2 on 2025-06-03 02:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='paciente_api',
            fields=[
                ('hi_nreg', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('hi_autase', models.CharField(max_length=100)),
                ('hi_nombre', models.CharField(max_length=255)),
                ('hi_fecnac', models.DateField()),
                ('hi_ubinac', models.CharField(max_length=100)),
                ('hi_direcc', models.CharField(max_length=255)),
                ('hi_sexo', models.CharField(max_length=10)),
                ('hi_ndocum', models.CharField(max_length=20)),
                ('hi_estciv', models.CharField(max_length=20)),
                ('hi_cpolic', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'paciente_api',
            },
        ),
        migrations.CreateModel(
            name='PasswordResetRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo Electrónico')),
                ('ip_address', models.GenericIPAddressField(verbose_name='Dirección IP')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de Solicitud')),
            ],
            options={
                'verbose_name': 'Solicitud de Recuperación',
                'verbose_name_plural': 'Solicitudes de Recuperación',
            },
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=40, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_requests', models.PositiveIntegerField(default=0)),
                ('solicitudes_realizadas', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
