import folium

from datetime import datetime
from django.shortcuts import render, get_object_or_404
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
        Q(Q(disappearted_at__gte=now) |
          Q(disappearted_at=None),
          Q(appearted_at__lt=now) |
          Q(appearted_at=None)
          )
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in entities_all:
        add_pokemon(
            folium_map,
            entity.lat,
            entity.lon,
            str(request.build_absolute_uri(entity.pokemon.image.url))
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
    requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))

    pokemon_entities = Pokemon.objects.filter(id=int(pokemon_id))[0].entities.all()
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            str(request.build_absolute_uri(pokemon_entity.pokemon.image.url))
        )
    pokemon = {
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': str(request.build_absolute_uri(requested_pokemon.image.url))
    }

    if requested_pokemon.next_evolution:
        pokemon.update({'next_evolution': requested_pokemon.next_evolution})
    evolution_prev = Pokemon.objects.filter(id=int(pokemon_id))[0].evolution_in.first()
    if evolution_prev:
        pokemon.update({'previous_evolution': evolution_prev})

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
