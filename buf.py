import requests

res = requests.get("https://0db41aeb0dfe.ngrok-free.app/movies")
movies = res.json()

print(movies[1])
print(movies[1]["title"])

for movie in movies:
    print(movie["title"])