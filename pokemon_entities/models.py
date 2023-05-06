from django.db import models  # noqa F401
import django.utils.timezone


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Имя")
    title_en = models.CharField(max_length=200, verbose_name="Имя(на английском)", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Имя(на японском)", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(default=None, upload_to='pokemons', blank=True, verbose_name="Изображение")
    next_evolution = models.ForeignKey('self',
                                       to_field='id',
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='next_evolution_set',
                                       verbose_name='Эволюционирует в')
    previous_evolution = models.ForeignKey('self',
                                           to_field='id',
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           blank=True,
                                           related_name='previous_evolution_set',
                                           verbose_name='Эволюционировал из')

    def __str__(self):
        return self.title_ru


class Entities(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Имя Покемона", related_name="pokemon_entities")
    lat = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-широта")
    lon = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-долгота")
    appearted_datetime = models.DateTimeField(verbose_name="Момент явления", blank=True, null=True)
    # appearted_time = models.TimeField(verbose_name="Время явления", blank=True, null=True)
    disappearted_datetime = models.DateTimeField(verbose_name="Момент исчезновения", blank=True, null=True)
    # disappearted_time = models.TimeField(verbose_name="Время исчезновения", blank=True, null=True)
    level = models.IntegerField(verbose_name="Уровень")
    health = models.IntegerField(verbose_name="Здоровье")
    strength = models.IntegerField(verbose_name="Сила")
    defence = models.IntegerField(verbose_name="Защита")
    stamina = models.IntegerField(verbose_name="Выносливость")

    def __str__(self):
        date_in = self.appearted_datetime.date() if self.appearted_datetime else "always before"
        date_out = self.disappearted_datetime.date() if self.disappearted_datetime else "and forever"
        title_text = '(always)' if not self.appearted_datetime and not self.disappearted_datetime else f'({date_in} - {date_out})'
        return f'{self.id} - {self.pokemon.title_ru} {title_text}'
