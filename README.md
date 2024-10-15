# IMDb Movie Scraper & Recommender

This project scrapes IMDb for movie information across various genres and stores the data in a CSV file. It also includes a recommendation feature that suggests movies based on a user-specified genre.

## Project Description

The project performs the following tasks:

1. **Scrape IMDb movie data** for all 	genres.
2. **Store the scraped data** in a CSV file (`movies.csv`).
3. **Provide random movie recommendations** based on genre filtering.

### Scraping Process

* The script uses the `requests` library to send HTTP requests to IMDb for different genres.
* `BeautifulSoup` is used to parse the HTML response and extract movie details such as:
  * **Title**
  * **Year**
  * **Rating**
  * **Plot**
* The extracted data is saved in the CSV format for future use.

### Movie Recommendation

The user can request a movie recommendation by entering a genre. The script filters the movies by genre and provides a random recommendation from the available data.

## Libraries Used

* `requests`: To send HTTP requests to IMDb.
* `beautifulsoup4`: To parse HTML and extract movie details.
* `pandas`: To manage and manipulate movie data and store it in CSV format.
* `os`: To handle file and directory operations.

## Software Used

* **Visual Studio Code** : Used as the development environment for writing and testing the code.

## Output Screenshots

A folder named `screenshots` is attached to this submission. It contains screenshots of the program's outputs, showing the scraping process, data storage, and movie recommendations.
