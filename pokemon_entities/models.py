from django.db import models  # noqa F401


class Pokemon(models.Model):
    pokemon_id = models.IntegerField()
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    description = models.TextField()
    img_url = models.CharField(max_length=2048)
    next_evolution = models.IntegerField(default=None)
    previous_evolution = models.IntegerField(default=None)


class Entities(models.Model):
    pokemon_id = models.IntegerField()
    level = models.IntegerField()
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
