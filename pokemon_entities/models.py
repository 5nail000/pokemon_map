from django.db import models  # noqa F401
import django.utils.timezone


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Имя", blank=False)
    title_en = models.CharField(max_length=200, verbose_name="Имя(на английском)", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Имя(на японском)", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
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
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Имя Покемона", blank=False)
    lat = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-широта", blank=False)
    lon = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-долгота", blank=False)
    appearted_date = models.DateField(default=django.utils.timezone.now, verbose_name="Дата явления", blank=True)
    appearted_time = models.TimeField(default=django.utils.timezone.now, verbose_name="Время явления", blank=True)
    disappearted_date = models.DateField(default=django.utils.timezone.now, verbose_name="Дата исчезновения", blank=True)
    disappearted_time = models.TimeField(default=django.utils.timezone.now, verbose_name="Время исчезновения", blank=True)
    level = models.IntegerField(default=1, verbose_name="Уровень", blank=False)
    health = models.IntegerField(default=100, verbose_name="Здоровье", blank=False)
    strength = models.IntegerField(default=100, verbose_name="Сила", blank=False)
    defence = models.IntegerField(default=100, verbose_name="Защита", blank=False)
    stamina = models.IntegerField(default=100, verbose_name="Выносливость", blank=False)
