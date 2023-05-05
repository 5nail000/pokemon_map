# Generated by Django 4.2 on 2023-05-05 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pokemon_id', models.IntegerField()),
                ('level', models.IntegerField()),
                ('lat', models.DecimalField(decimal_places=6, max_digits=8)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pokemon_id', models.IntegerField()),
                ('title_ru', models.CharField(max_length=200)),
                ('title_en', models.CharField(max_length=200)),
                ('title_jp', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('img_url', models.CharField(max_length=2048)),
                ('next_evolution', models.IntegerField(default=None)),
                ('previous_evolution', models.IntegerField(default=None)),
            ],
        ),
    ]