# Generated by Django 3.1 on 2021-03-14 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.EmailField(max_length=50, unique=True, verbose_name='Correo electronico'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre de usuario'),
        ),
    ]
