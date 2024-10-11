from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=30)
    damage_max = models.IntegerField(default=3)
    damage_min = models.IntegerField(default=1)
    health = models.IntegerField(default=10)
    player_attack1_name = models.CharField(max_length=30)
    player_attack1_damage_max = models.IntegerField(default=3)
    player_attack1_damage_min = models.IntegerField(default=1)
    player_attack1_cooldown = models.IntegerField(default=1)
    player_attack2_name = models.CharField(max_length=30)
    player_attack2_damage_max = models.IntegerField(default=3)
    player_attack2_damage_min = models.IntegerField(default=1)
    player_attack2_cooldown = models.IntegerField(default=1)


class Enemy(models.Model):
    name = models.CharField(max_length=30)
    enemy_class = models.IntegerField(default=1)
    health = models.IntegerField(default=5)
    enemy_attack1_name = models.CharField(max_length=30)
    enemy_attack1_damage_max = models.IntegerField(default=3)
    enemy_attack1_damage_min = models.IntegerField(default=1)
    enemy_attack1_cooldown = models.IntegerField(default=1)
    enemy_attack2_name = models.CharField(max_length=30)
    enemy_attack2_damage_max = models.IntegerField(default=3)
    enemy_attack2_damage_min = models.IntegerField(default=1)
    enemy_attack2_cooldown = models.IntegerField(default=1)

class Location(models.Model):
    id_number = models.IntegerField(null=True)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    location_check = models.BooleanField(default=False)
    trap_exists = models.BooleanField(default=False)
    trap_found = models.BooleanField(default=False)
    trap_damage_max = models.IntegerField(default=3)
    trap_damage_min = models.IntegerField(default=1)

class Map(models.Model):
    id_number = models.IntegerField(null=True)
    location_id = models.IntegerField(null=True)
    enemy_class = models.IntegerField(default=0)
    is_it_enemy = models.BooleanField(default=False)

class Map_len(models.Model):
    map_len = models.IntegerField(default=7)
