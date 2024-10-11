# Generated by Django 5.1.1 on 2024-10-11 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enemy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('enemy_attack1_name', models.CharField(max_length=30)),
                ('enemy_attack2_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('location_check', models.BooleanField(default=False)),
                ('trap_exists', models.BooleanField(default=False)),
                ('trap_found', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('player_attack1_name', models.CharField(max_length=30)),
                ('player_attack2_name', models.CharField(max_length=30)),
            ],
        ),
    ]
