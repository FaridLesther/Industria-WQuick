# Generated by Django 3.1 on 2021-03-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombre', models.CharField(max_length=15, unique=True, verbose_name='Nombre de usuario')),
                ('imagen', models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='Imagen de perfil')),
                ('correo', models.EmailField(max_length=60, unique=True, verbose_name='Correo electronico')),
                ('admin', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
