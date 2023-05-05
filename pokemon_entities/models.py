from django.db import models  # noqa F401
import django.utils.timezone


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Имя")
    title_en = models.CharField(max_length=200, verbose_name="Имя(на английском)")
    title_jp = models.CharField(max_length=200, verbose_name="Имя(на японском)")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(default=None, upload_to='pokemons', blank=True, verbose_name="Изображение")
    next_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='next_evolution_set',
                                       verbose_name="Эволюционирует из")
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='previous_evolution_set',
                                           verbose_name="Эволюционировал в")

    def __str__(self):
        return self.title_ru


class Entities(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Имя Покемона")
    lat = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-широта")
    lon = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-долгота")
    appearted_date = models.DateField(default=django.utils.timezone.now, verbose_name="Дата явления")
    appearted_time = models.TimeField(default=django.utils.timezone.now, verbose_name="Время явления")
    disappearted_date = models.DateField(default=django.utils.timezone.now, verbose_name="Дата исчезновения")
    disappearted_time = models.TimeField(default=django.utils.timezone.now, verbose_name="Время исчезновения")
    level = models.IntegerField(default=1, verbose_name="Уровень")
    health = models.IntegerField(default=100, verbose_name="Здоровье")
    strength = models.IntegerField(default=100, verbose_name="Сила")
    defence = models.IntegerField(default=100, verbose_name="Защита")
    stamina = models.IntegerField(default=100, verbose_name="Выносливость")
