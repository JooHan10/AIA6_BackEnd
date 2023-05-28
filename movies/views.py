from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Movie, Genre
from .serializers import MovieSerializer
from rest_framework.views import APIView
import requests, random, csv, os, json
from datetime import datetime
from .movies_csv import save_movies_to_csv
from rest_framework.permissions import IsAdminUser
from .movies_ai import similar_overview
from rest_framework.pagination import PageNumberPagination
from urllib.parse import urlparse, parse_qs

# Create your views here.
#api에서 무비 데이터 가져오기
class MovieDataFetcher:
    def fetch_movies_data(self):
        genres_url = "https://api.themoviedb.org/3/genre/movie/list"
        params = {
                    "api_key": "dfffda402827c71395fe46139633c254",
                    "language": "ko-KR"
                 }

        response = requests.get(genres_url, params=params)
        genres_data = response.json()

        # 장르 정보 Genre 모델에 저장
        genres = genres_data['genres']
        for genre in genres:
            Genre.objects.get_or_create(id=genre['id'], defaults={'name': genre['name']})

        # 영화 정보 가져오기
        movies_url = "https://api.themoviedb.org/3/movie/popular"
        movies_data = []
        for page in range(1, 201):
            params = {
                "api_key": "dfffda402827c71395fe46139633c254",
                "language": "ko-KR",
                "page": page
            }
            response = requests.get(movies_url, params=params)
            if response.status_code == 200:
                new_data = response.json().get('results', [])
                page_data = response.json().get('page')                
                movies_data.append([new_data, page_data])
        return movies_data
#무비 출력뷰    
# class MovieListView(APIView):
    
#     def get(self, request):
#         movies = Movie.objects.all()  
#         serialized_data = []
        
#         # 영화 정보 출력
#         for movie_data in movies:
#             genre_ids = movie_data.genres.all().values_list('id', flat=True)
#             genres = Genre.objects.filter(id__in=genre_ids)
#             genre_names = [genre.name for genre in genres]
            
                                                           
#             movie_json = {
#                 "id": movie_data.id,
#                 "title": movie_data.title,
#                 "overview": movie_data.overview,
#                 "release_date" : movie_data.release_date,
#                 "vote_average" : movie_data.vote_average,
#                 "genres" : genre_names,
#                 "poster_path" : movie_data.poster_path
#                     }
                    
#             serialized_data.append(movie_json)
                
#         return Response(serialized_data)
class MovieListView(APIView):
    
    def get(self,request):
        movie_data = MovieDataFetcher()
        movies_data = movie_data.fetch_movies_data()
        serialized_data = []
        for list_data in movies_data:
            page = list_data[1]
            movies = list_data[0]
            for data in movies:
                genre_ids = data.get('genre_ids')
                genres = Genre.objects.filter(id__in =genre_ids)
                genre_names = [genre.name for genre in genres]                
                vote_average = data.get('vote_average', None)
                release_date_str = data.get('release_date', None)
                if data['poster_path']is not None:
                    poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
                else:
                    poster_path = None
                if release_date_str:
                    try:
                        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        release_date = None
                movie_json = {
                    "id": data['id'],
                    "title": data['title'],
                    "overview": data['overview'],
                    "release_date": release_date,
                    "vote_average": vote_average,
                    "genres": genre_names,
                    "poster_path": poster_path,
                    "page": page
                    
                }
                
                serialized_data.append(movie_json)
            
        return Response(serialized_data)



#csv파일 생성 및 모델에 저장 view
class SaveMoviesView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        movie_data = MovieDataFetcher()
        movies_data = movie_data.fetch_movies_data()
        self.save_movie_data(movies_data)
        csv_file_path = "movie_data.csv"
        save_movies_to_csv(csv_file_path)
        
        return Response("CSV파일 및 무비모델 저장완료")
    
    def save_movie_data(self, movies_data):
        for select_data in movies_data:
            page = select_data[1]
            movies = select_data[0]
            for movie_data in movies:
                if movie_data.get('adult') == False:
                    # genre_ids = movie_data['genre_ids']
                    # genres = Genre.objects.filter(id__in=genre_ids)
                    # genre_names = [genre.name for genre in genres]
                    #포스터 경로가 없는 경우 None으로 처리.
                    if movie_data['poster_path']is not None:
                        poster_path = "https://image.tmdb.org/t/p/w500/" + movie_data['poster_path']
                    else:
                        poster_path = None
                    vote_average = movie_data.get('vote_average', None)
                    release_date_str = movie_data.get('release_date', None)
                    # #release_date 값이 '' 인 경우 형식오류.. None으로 반환하게 했으나 ''값은 날짜형식이 아니란 오류. 한번 더 처리해서 강제로 None값을 갖게 함.
                    if release_date_str:
                        try:
                            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            release_date = None
                    genre_ids = movie_data['genre_ids']
                    genres = []
                    for genre_id in genre_ids:
                        try:
                            genre = Genre.objects.get(id=genre_id)
                            genres.append(genre)
                        except: 
                            pass

                    movie = Movie(
                        id=movie_data['id'],
                        title=movie_data['title'],
                        overview=movie_data['overview'],
                        release_date=release_date,
                        vote_average = vote_average,
                        poster_path=poster_path,
                        page = page
                    )
                    movie.save()
                    movie.genres.set(genres)
                    

# 영화 상세 페이지 view
class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)  

  
    
#비슷한 영화 추천 view
class SimilarMoviesView(APIView):
    
    def post(self, request):
        csv_file_path = "movie_data.csv"
        target_movie_id = request.data.get('target_movie_id')
        if target_movie_id is None:
            return Response("올바른 target_movie_id 값을 제공해주세요")
        target_movie_id = int(target_movie_id)
        target_movie_index = self.find_movie_index(csv_file_path, target_movie_id)
        
        if target_movie_index is None:
            return Response("비슷한 영화가 없네요")
        
        similar_movies = similar_overview(csv_file_path, target_movie_index)

        return Response(similar_movies)
    # 선택한 영화의 ID값을 가져와 csv파일에서 검색 후 인덱스 값으로 변환
    def find_movie_index(self, csv_file_path, target_movie_id):
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for index, row in enumerate(reader):
                if row['id'] == str(target_movie_id):
                    return index
        return None


# class MovieListPaginatedView(MovieListView):
    '''
    MovieListView의 Movie API GET을 상속받아 Pagination을 orverriding 합니다.
    그 후, pagination 인스턴스를 생성하여 시리얼라이즈된 데이터를 pagination 처리하고, pagination된 response을 반환합니다.
    pagination_class를 PageNumberPagination로 설정해 페이지 기준 parameter로 처리합니다.
    
    # API 요청 예시
    GET /movie/?page=2

    # API 응답 예시
    {
        "count": 1000, # 불러오는 영화의 수
        "next": "/movies/paginated/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "title": "영화 제목",
                "overview": "영화 개요",
                "release_date": "2023-05-28",
                "vote_average": 8.5,
                "genres": ["드라마", "로맨스"],
                "poster_path": "http://example.com/poster.jpg"
            },
            // 페이지네이션된 영화 목록
        ]
    }
    '''
    # pagination_class = PageNumberPagination

    # def get(self, request):
    #     inherited_instance = super().get(request)
    #     serialized_data = inherited_instance.data
    #     pagination_instance = self.pagination_class()
    #     paginated_data = pagination_instance.paginate_queryset(serialized_data, request)
    #     pagination_instance.count = len(serialized_data) # 카운트 안주니 오류가 (count = 전체 get해오는 데이터 개수)
    #     return pagination_instance.get_paginated_response(paginated_data)
    


class MovieListPaginatedView(APIView):

    def get(self, request):
        movies_url = "https://api.themoviedb.org/3/movie/popular"
        parsed_url = urlparse(request.build_absolute_uri())       
        page = parse_qs(parsed_url.query).get('page', [1])[0] # URL의 쿼리 파라미터에서 'page' 값을 추출       
        params = {
                "api_key": "dfffda402827c71395fe46139633c254",
                "language": "ko-KR",
                "page": page
            }
        response = requests.get(movies_url, params=params)
        request_data =[]
        if response.status_code == 200:
            movies_data = response.json().get('results')
            request_data.append(movies_data)
        serialized_data = []
        for data in movies_data:

                genre_ids = data.get('genre_ids')
                genres = Genre.objects.filter(id__in =genre_ids)
                genre_names = [genre.name for genre in genres]
                vote_average = data.get('vote_average', None)
                release_date_str = data.get('release_date', None)
                if data['poster_path']is not None:
                    poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
                else:
                    poster_path = None
                if release_date_str:
                    try:
                        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        release_date = None
                movie_json = {
                    "id": data['id'],
                    "title": data['title'],
                    "overview": data['overview'],
                    "release_date": release_date,
                    "vote_average": vote_average,
                    "genres": genre_names,
                    "poster_path": poster_path
                }
                
                serialized_data.append(movie_json)
            
        return Response(serialized_data)
