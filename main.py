import streamlit as st
import pickle as pl
import pandas as pd
import requests

def movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MWNlMjk0ZTZhNDQwMzFiYjA3Y2EzMjM1MjdjMmYwNSIsIm5iZiI6MTcyMTkzMTU5OS40MTE0NjgsInN1YiI6IjY2YTI5NjNlN2MxOGRlNjZmMWM4M2JhMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.v6_5--3CNaFC9ABhEyoy0F--2cjx72jf8xN2-XuIHtE"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    return f"http://image.tmdb.org/t/p/w500/{data['backdrops'][0]['file_path']}"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    recommended_movies = []

    for i in movie_list:
        mov = {}
        mov['title'] =movies.iloc[i[0]]['title']
        mov['movie_poster'] = movie_poster(movies.iloc[i[0]]['movie_id'])
        recommended_movies.append(mov)

    return recommended_movies

st.title("Movie recommender system")

movie_dict = pl.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pl.load(open('similarity.pkl','rb'))

option = st.selectbox(
    "Pick a Movie",
    movies['title'].values)

try:
    if st.button('Recommend'):
        recommended_movies = recommend(option)
        columns = st.columns(len(recommended_movies))

        for i, movie in enumerate(recommended_movies):
            with columns[i]:
                st.text(movie['title'])
                st.image(movie['movie_poster'])
except:
    st.error('This is an error', icon="🚨")