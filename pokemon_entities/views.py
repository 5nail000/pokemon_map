import folium
import json

from datetime import datetime
from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, Entities
from django.db.models import Q


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = datetime.now()
    pokemons_all = Pokemon.objects.all()
    entities_all = Entities.objects.filter(
        Q(Q(disappearted_date__gt=now.date()) |
          Q(disappearted_date=now.date(), disappearted_time__gte=now.time()),
          Q(appearted_date__lt=now.date()) |
          Q(appearted_date=now.date(), disappearted_time__lte=now.time())
          )
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in entities_all:
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            str(request.build_absolute_uri(f'/media/{entity.pokemon.image}'))
        )

    pokemons_on_page = []
    for pokemon in pokemons_all:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    for pokemon in pokemons:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
