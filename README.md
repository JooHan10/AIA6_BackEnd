# Coovie 

![](https://img.shields.io/github/license/joohan10/AIA6_Backend?color=blue)

**Coovie**(Cosine + Movie)는 장르와 줄거리를 기준으로 AI가 영화를 추천해주는 사이트입니다.

DB의 랜덤한 영화들 중 6개를 랜덤으로 보여줍니다. 사용자는 6개의 영화 중 마음에 드는 영화가 없다면 '다시검색'을 통해 영화를 다시 뽑을 수 있습니다. AI는 사용자가 선택한 영화를 기준으로 줄거리가 비슷한 영화를 코사인 유사도(Cosine similarity)를 사용하여 새로운 영화를 추천해줍니다.

![README](https://github.com/nueeng/AIA6_FrontEnd/assets/127704498/536ffe64-6d51-4e71-b832-8ed0f0379662)

[Frontend Repository](https://github.com/nueeng/AIA6_FrontEnd)  

## Stacks

<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"><img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"><img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">

<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"><img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">

<img src="https://img.shields.io/badge/TMDB-pink?style=for-the-badge&logo=themoviedatabase&logoColor=black">


## Dependencies

- Django
- Django REST framework
- Django-cors-headers
- Simple JWT
- requests
- pylint
- scikit-learn
- NumPy
- pandas

## 🎬 Description

- 회원 기능
    - 회원가입
    - 로그인
    - 로그아웃
    - 마이페이지 (본인이 작성한 후기 조회, 수정, 삭제 가능)
- 후기 작성
    - 로그인한 회원은 짧은 후기를 작성할 수 있습니다.
    - 로그인한 회원은 평점을 남길 수 있습니다.
    - 로그인한 회원은 좋아요 버튼을 사용할 수 있습니다.
- 영화 추천
    - 영화 선택 페이지 ⇒ 영화 상세 & 영화 추천 페이지
        1. TMDB API 중 Popular Category 영화 랜덤으로 6개를 띄워줍니다. (영화 제목, 포스터, 줄거리, 평점, 장르, 개봉일)
        2. 사용자가 마음에 드는 영화 하나를 선택하면, 해당 영화의 정보와 + 사용자가 선택한 영화와 줄거리가 유사한 영화를 AI가 5개 추천해줍니다.
        3. 만약 마음에 드는 영화가 페이지에 없다면 다시 검색하기 버튼을 누르면 새로운 6개의 영화를 띄워줍니다.
        4. 영화 상세 & 영화 추천 페이지에서 추천 받은 영화 5개 중 한 개를 선택하면 다시 같은 로직을 반복합니다.

## 📽 API Reference

- [TMDB API Reference](https://developer.themoviedb.org/reference/intro/getting-started)  
  TMDB API는 The Movie Database(TMDB)에서 제공하는 영화 데이터 및 관련 정보에 액세스할 수 있는 RESTful API입니다.  
  TMDB API중 [`GET /genre/movie/list`](https://developer.themoviedb.org/reference/genre-movie-list) 엔드포인트를 사용하여 장르와 영화를 연결하고, [`GET /movie/popular`](https://developer.themoviedb.org/reference/movie-popular-list) 엔드포인트를 사용하여 4000개의 데이터를 기준으로 AI를 학습시키고, 리뷰를 작성할 수 있습니다.


## License

- [MIT License](https://github.com/JooHan10/AIA6_BackEnd/blob/main/LICENSE)

 ## Team
 
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/JooHan10"><img src="https://avatars.githubusercontent.com/u/116674496?v=4" width="100px;" alt=""/><br /><sub><b>팀장 : 이주한</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/Songjimyung"><img src="https://avatars.githubusercontent.com/u/116045723?v=4" width="100px;" alt=""/><br /><sub><b>팀원 : 송지명</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/nueeng"><img src="https://avatars.githubusercontent.com/u/127704498?v=4" width="100px;" alt=""/><br /><sub><b>팀원 : 최준영</b></sub></a><br /></td>
    <tr/>
  </tbody>
</table>
