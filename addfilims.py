import requests

BASE_URL = "http://127.0.0.1:8000/movies"

movies = [
    {"title": "Inception", "year": 2010, "rating": 8.8, "description": "A thief who steals corporate secrets through dream-sharing technology."},
    {"title": "The Dark Knight", "year": 2008, "rating": 9.0, "description": "Batman faces the Joker in Gotham City."},
    {"title": "Interstellar", "year": 2014, "rating": 8.6, "description": "Explorers travel through a wormhole in space to ensure humanity's survival."},
    {"title": "The Matrix", "year": 1999, "rating": 8.7, "description": "A computer hacker learns about the true nature of reality and his role in the war against its controllers."},
    {"title": "Forrest Gump", "year": 1994, "rating": 8.8, "description": "The life story of a slow-witted but kind-hearted man from Alabama."},
    {"title": "Fight Club", "year": 1999, "rating": 8.8, "description": "An insomniac office worker forms an underground fight club."},
    {"title": "The Shawshank Redemption", "year": 1994, "rating": 9.3, "description": "Two imprisoned men bond over years, finding solace and redemption."},
    {"title": "Pulp Fiction", "year": 1994, "rating": 8.9, "description": "The lives of two hitmen, a boxer, and others intertwine in Los Angeles."},
    {"title": "Gladiator", "year": 2000, "rating": 8.5, "description": "A betrayed Roman general fights his way back as a gladiator."},
    {"title": "Avatar", "year": 2009, "rating": 7.8, "description": "A paraplegic Marine on an alien planet becomes torn between following orders and protecting his new world."},
]

for movie in movies:
    response = requests.post(BASE_URL, json=movie)
    if response.status_code == 201:
        print(f"✅ Added: {movie['title']}")
    else:
        print(f"❌ Failed to add {movie['title']}: {response.status_code} - {response.text}")
