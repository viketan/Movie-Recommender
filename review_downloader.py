import time
import requests
import pandas as pd
import subprocess


def movie_downloader(id):
    payload = {'api_key': '8265bd1679663a7ea12ac168da84d2e8', }
    url = 'https://api.themoviedb.org/3/movie/'+str(id)+'/reviews'
    response = requests.get(url, params=payload, verify=False, timeout=1000)

    review = response.json()

    i = 0
    movie_id = []
    reviews = []
    while i < review['total_results']:
        movie_id.append(review['id'])
        reviews.append(review['results'][i]['content'])
        i += 1

    data = {
        'movie_id': movie_id,
        'review': reviews
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
    dataset = pd.DataFrame(columns=['movie_id', 'review'])
    for id in MovieList:
        time.sleep(2)
        dataset = pd.concat([dataset, movie_downloader(id)])
    dataset.to_csv('review_dataset.csv', index=False)


if __name__ == "__main__":
    main()
