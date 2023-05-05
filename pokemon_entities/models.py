from django.db import models  # noqa F401
import django.utils.timezone


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(default=None, upload_to='pokemons', blank=True)
    next_evolution = models.IntegerField(default=None)
    previous_evolution = models.IntegerField(default=None)

    def __str__(self):
        return self.title_ru


class Entities(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lon = models.DecimalField(max_digits=8, decimal_places=6)
    appearted_date = models.DateField(default=django.utils.timezone.now)
    appearted_time = models.TimeField(default=django.utils.timezone.now)
    disappearted_date = models.DateField(default=django.utils.timezone.now)
    disappearted_time = models.TimeField(default=django.utils.timezone.now)
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=100)
    defence = models.IntegerField(default=100)
    stamina = models.IntegerField(default=100)
