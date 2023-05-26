import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

    # 오버뷰 비슷한 5개의 영화
def similar_overview(csv_file_path, target_movie_index, top_n=5):
    movie_data = []
    with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        movie_data = list(reader)

    #target_movie_index의 범위 설정
    if target_movie_index < 0 or target_movie_index >= len(movie_data):
        return []
    #csv에 저장된 영화들의 오버뷰
    overviews = [movie['overview'] for movie in movie_data]
    #오버뷰의 Tf-idf 벡터 행렬로 변환.
    tfidf_matrix = TfidfVectorizer().fit_transform(overviews)
    # print('오버뷰변환', tfidf_matrix)
    
    #비교할 특정 영화의 Tf-idf 벡터
    target_vector = tfidf_matrix[target_movie_index]
    # print('타겟', target_vector)
    
    # print('코사인유사도', cosine_similarity(target_vector, tfidf_matrix))
    similar_movie = cosine_similarity(target_vector, tfidf_matrix)[0]
    
    sorted_similar = np.argsort(similar_movie)[::-1]
    # print('행렬소트',sorted_similar)
    similar_movies = []
    for index in sorted_similar[1:top_n+1]:
        movie = movie_data[index]
        similar_movies.append({
            'title': movie['title'],
            'overview': movie['overview'],
            'release_date': movie['release_date'],
            'vote_average': movie['vote_average'],
            'poster_path': movie['poster_path'],
            'genre_ids': movie['genre_ids']
        })

    return similar_movies

similar_overview('movie_data.csv', 3 )
print(similar_overview)