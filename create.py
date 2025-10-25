import requests

movie = {
    "title": "mario",
    "year": 1888,
    "rating": 9,
    "description": "string"
}
res = requests.post("https://0db41aeb0dfe.ngrok-free.app/movies", json=movie)

print(res.json())