# Generated by Django 4.2 on 2023-05-05 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_entities_appearted_date_entities_appearted_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entities',
            name='defence',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='entities',
            name='health',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='entities',
            name='stamina',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='entities',
            name='strength',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='entities',
            name='level',
            field=models.IntegerField(default=1),
        ),
    ]
