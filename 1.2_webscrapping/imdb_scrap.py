import requests
import csv
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('OMDB_API_KEY')

# List of movie titles to search
movies = ['Inception', 'The Dark Knight', 'Interstellar', 'Joker']

# CSV file setup
with open('1_webscrapping/imdb_movies.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Year', 'Genre', 'IMDB Rating', 'Director', 'Plot'])

    for title in movies:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        response = requests.get(url)
        data = response.json()

        if data['Response'] == 'True': #if it exists store the required data of it
            writer.writerow([
                data['Title'],
                data['Year'],
                data['Genre'],
                data['imdbRating'],
                data['Director'],
                data['Plot']
            ])
            print(f"Fetched: {data['Title']}")
        else:
            print(f"Error: {data['Error']} for movie: {title}") #if movie doesn't exist print the error message
