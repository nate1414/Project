import requests
import json

url = 'http://pokeapi.co/api/v1/pokemon/charizard/'
response = requests.get(url)

if response.status_code == 200:
    data = json.loads(response.text)
    print data['name']
else:
    print 'An error occurred querying the API'