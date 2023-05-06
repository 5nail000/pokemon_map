import folium

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
        Q(Q(disappearted_datetime__gte=now) |
          Q(disappearted_datetime=None),
          Q(appearted_datetime__lt=now) |
          Q(appearted_datetime=None)
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
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_all = Pokemon.objects.all()

    for pokemon in pokemons_all:
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = Pokemon.objects.filter(id=int(pokemon_id))[0].pokemon_entities.all()
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            str(request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.image}'))
        )
    pokemon = {
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': str(request.build_absolute_uri(f'/media/{requested_pokemon.image}'))
    }

    if requested_pokemon.next_evolution:
        pokemon.update({'next_evolution': requested_pokemon.next_evolution})
    if requested_pokemon.previous_evolution:
        pokemon.update({'previous_evolution': requested_pokemon.previous_evolution})

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
