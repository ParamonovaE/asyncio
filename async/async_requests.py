import asyncio
import aiohttp
import more_itertools
from models import SessionDB, SwapiPeople, init_orm

async def get_film_title(film_url, session):
    response = await session.get(film_url)
    film_data = await response.json()
    return film_data["title"]


async def get_name_from_url(url, session):
    response = await session.get(url)
    data = await response.json()
    return data.get("name", "")


async def get_people(person_id, session):
    response = await session.get(f"https://swapi.dev/api/people/{person_id}/")
    json_data = await response.json()
    
    films = []
    for film_url in json_data.get("films", []):
        film_title = await get_film_title(film_url, session)
        films.append(film_title)

    species = []
    for species_url in json_data.get("species", []):
        species_name = await get_name_from_url(species_url, session)
        species.append(species_name)

    starships = []
    for starship_url in json_data.get("starships", []):
        starship_name = await get_name_from_url(starship_url, session)
        starships.append(starship_name)

    vehicles = []
    for vehicle_url in json_data.get("vehicles", []):
        vehicle_name = await get_name_from_url(vehicle_url, session)
        vehicles.append(vehicle_name)

    homeworld_url = json_data.get("homeworld")
    if homeworld_url:
        homeworld = await get_name_from_url(homeworld_url, session)
    else:
        homeworld = ""

    return {
        "id": person_id,
        "birth_year": json_data.get("birth_year", "unknown"), 
        "eye_color": json_data.get("eye_color", "unknown"),
        "films": ", ".join(films),
        "gender": json_data.get("gender", "unknown"),
        "hair_color": json_data.get("hair_color", "unknown"),
        "height": json_data.get("height", "unknown"),
        "homeworld": homeworld,
        "mass": json_data.get("mass", "unknown"),
        "name": json_data.get("name", "unknown"),
        "skin_color": json_data.get("skin_color", "unknown"),
        "species": ", ".join(species),
        "starships": ", ".join(starships),
        "vehicles": ", ".join(vehicles),
    }


async def insert_people(people_list):
    async with SessionDB() as session:
        orm_model_list = [SwapiPeople(**person_dict) for person_dict in people_list]
        session.add_all(orm_model_list)
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session_http:
        coros = (get_people(i, session_http) for i in range(1, 101))
        for coros_chunk in more_itertools.chunked(coros, 5):
            people_list = await asyncio.gather(*coros_chunk)
            asyncio.create_task(insert_people(people_list))

        tasks = asyncio.all_tasks()
        main_task = asyncio.current_task()
        tasks.remove(main_task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
