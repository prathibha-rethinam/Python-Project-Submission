import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

num = 1
GENRES = [
    'drama',
    'adventure',
    'thriller',
    'action',
    'crime',
    'comedy',
    'mystery',
    'war',
    'fantasy',
    'sci-Fi',
    'romance',
    'biography',
    'family',
    'animation',
    'history',
    'sport',
    'western',
    'music',
    'horror',
    'musical',
    'film-Noir'
]

def scrape_imdb(genre):
    try:
        url = f"https://www.imdb.com/search/title/?genres={genre.lower()}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        movie_list_ul = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-748571c8-0 jApQAb detailed-list-view ipc-metadata-list--base')
        
        if not movie_list_ul:
            print(f"No movie list found for genre: {genre}")
            return []

        movie_containers = movie_list_ul.find_all('li', class_='ipc-metadata-list-summary-item')

        movies = []
        for movie in movie_containers:

            title_tag = movie.find('h3', class_='ipc-title__text')
            title = title_tag.text.strip() if title_tag else 'N/A'


            if title.split()[0].replace('.', '').isdigit():
                title = title.split('.', 1)[1].strip()


            year_tag = movie.find('span', class_='sc-ab348ad5-8 cSWcJI dli-title-metadata-item')
            year = year_tag.text.strip() if year_tag else 'N/A'

            rating_tag = movie.find('span', class_='ipc-rating-star--rating')
            rating = rating_tag.text.strip() if rating_tag else 'N/A'

            plot_tag = movie.find('div', class_='ipc-html-content-inner-div')
            plot = plot_tag.text.strip() if plot_tag else 'N/A'

            movies.append({
                'Title': title,
                'Year': year,
                'Rating': rating,
                'Plot': plot,
                'Genre': genre
            })

        return movies

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {genre}: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def save_to_csv(data):
    if not os.path.exists('data'):
        os.makedirs('data')
    
    file_path = "data/movies.csv"
    
    if os.path.exists(file_path):
        df = pd.DataFrame(data)
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)




def load_movies(file_path):
    try:
        movies = pd.read_csv(file_path)
        return movies
    except FileNotFoundError:
        print("The specified file was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("The file is empty.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def filter_movies_by_genre(movies, genre):
    filtered_movies = movies[movies['Genre'].str.contains(genre, case=False, na=False)]
    return filtered_movies

def suggest():
    file_path = 'data/movies.csv'
    
    movies = load_movies(file_path)
    
    if movies is not None:
        print("Available genres:")
        print(movies['Genre'].unique())
        
        user_genre = input("Enter the genre you want to filter by: ")
        

        filtered_movies = filter_movies_by_genre(movies, user_genre)
        
        if not filtered_movies.empty and user_genre.lower() in GENRES:
            random_movie = filtered_movies.sample(n=1).iloc[0]

            print(f'\nYou might like the movie: "{random_movie["Title"]}". \nIt was made in year(s) {random_movie["Year"]}. \nThe rating is {random_movie["Rating"]}/10. \nThe plot is: {random_movie["Plot"]}')
        else:
            print(f"No movies found for the genre '{user_genre}'.")

if __name__ == "__main__":
    all_movies = []
    print("Scraping movies from database...")
    total = len(GENRES)
    for genre in GENRES:
        
        movies = scrape_imdb(genre)
        if movies:
            all_movies.extend(movies)
        print("Progress: " + str(((num*100//total))) + "%")
        num = num+1

    if all_movies:
        save_to_csv(all_movies)
        print(f"Successfully scraped data in \"data/movies.csv\".\n\n")
    else:
        print("No data scraped.")


    
    suggest()
