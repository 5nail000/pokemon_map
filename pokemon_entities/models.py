from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Имя")
    title_en = models.CharField(max_length=200, verbose_name="Имя(на английском)", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Имя(на японском)", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='pokemons', verbose_name="Изображение")
    evolution = models.ForeignKey('self',
                                       to_field='id',
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='evolution',
                                       verbose_name='Эволюционирует в')

    def __str__(self):
        return self.title_ru


class Entities(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Имя Покемона", related_name="entities")
    lat = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-широта")
    lon = models.DecimalField(max_digits=8, decimal_places=6, verbose_name="Координата-долгота")
    appeared_at = models.DateTimeField(verbose_name="Момент явления", blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name="Момент исчезновения", blank=True, null=True)
    level = models.IntegerField(verbose_name="Уровень")
    health = models.IntegerField(verbose_name="Здоровье")
    strength = models.IntegerField(verbose_name="Сила")
    defence = models.IntegerField(verbose_name="Защита")
    stamina = models.IntegerField(verbose_name="Выносливость")

    def __str__(self):
        date_in = self.appeared_at.date() if self.appeared_at else "always before"
        date_out = self.disappeared_at.date() if self.disappeared_at else "and forever"
        title_text = '(always)' if not self.appeared_at and not self.disappeared_at else f'({date_in} - {date_out})'
        return f'{self.id} - {self.pokemon.title_ru} {title_text}'
