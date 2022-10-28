import time
import requests
import pandas as pd
import subprocess
import warnings
warnings.filterwarnings('ignore')


def movie_dataset_downloader(id):
    payload = {'api_key': '8265bd1679663a7ea12ac168da84d2e8'}
    url_details = 'https://api.themoviedb.org/3/movie/'+str(id)
    response = requests.get(url_details, params=payload,
                            verify=False, timeout=50)
    details = response.json()
    movie_id = []
    title = []
    overview = []
    genres = []
    movie_id.append(details['id'])
    title.append(details['title'])
    overview.append(details['overview'])
    genre_str = ''
    for genre in details['genres']:
        genre_str = genre_str+genre['name']+' '
    genre = genre_str.rstrip()
    genres.append(genre)
    url_keyword = 'https://api.themoviedb.org/3/movie/'+str(id)+'/keywords'
    response = requests.get(url_keyword, params=payload,
                            verify=False, timeout=50)
    keyword = response.json()
    keywords = []
    keyword_str = ''
    for key in keyword['keywords']:
        keyword_str = keyword_str+key['name']+' '
    keyword_str = keyword_str.rstrip()
    keywords.append(keyword_str)
    url_credit = 'https://api.themoviedb.org/3/movie/'+str(id)+'/credits'
    response = requests.get(url_credit, params=payload,
                            verify=False, timeout=50)
    credit = response.json()
    casts = []
    casts_str = ''
    for cast in credit['cast']:
        casts_str = casts_str+cast['name']+' '
    casts_str = casts_str.rstrip()
    casts.append(casts_str)
    director = []
    director_str = ''
    for crew in credit['crew']:
        if crew['job'] == 'Director':
            director_str = director_str+crew['name']
    director.append(director_str)

    data = {
        'movie_id': movie_id,
        'title': title,
        'genre': genre,
        'overview': overview,
        'casts': casts,
        'keywords': keywords,
        'director': director
    }

    df = pd.DataFrame(data)
    return df


def main():
    print('[//]Input Text File is going to be opened. Please enter Movie IDs.')
    subprocess.run(["notepad", "MovieID.txt"])
    MovieList = []
    f = open("MovieID.txt", "r")
    for x in f:
        MovieList.append(str(x).strip())
    f.close()
    dataset = pd.DataFrame(
        columns=['movie_id', 'title', 'genre', 'overview', 'casts', 'keywords', 'director'])
    for id in MovieList:
        time.sleep(2)
        print(id)
        dataset = pd.concat([dataset, movie_dataset_downloader(id)])
        dataset.to_csv('movie_dataset_test.csv', index=False)


if __name__ == "__main__":
    main()
