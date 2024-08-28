import pickle
import pandas as pd
import streamlit as st
import requests

# Load the dataset
data = pickle.load(open('movie_dict.pkl', mode='rb'))
movies = pd.DataFrame(data)

similarity = pickle.load(open('similarity.pkl', mode='rb'))

# Function to fetch poster URL from TMDB API
def fetch_poster(movie_title):
    api_key = '39e5af262fdfffe63b8ee7e0e6594da0' 
    base_url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': api_key,
        'query': movie_title
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_poster_url
    return None

def recommend(movie):
    recommended = []
    posters = []

    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x: x[1])[1:6]

    for i in movie_list:
        ####fetch poster from tmdb api
        posters_url = fetch_poster(movies.iloc[i[0]].title)
        posters.append(posters_url)

        recommended.append(movies.iloc[i[0]].title)

    return recommended, posters

# Streamlit Web-app
st.title('Movie Recommendation System')

selected_movies = st.selectbox(
    "Enter Movie Name to Recommend",
    movies['title'].values
)

btn = st.button('Recommend')

if btn:
    recommended_movies, posters = recommend(selected_movies)

    cols = st.columns(5)  
    for col, title, poster in zip(cols, recommended_movies, posters):
        with col:
            st.text(title)
            if poster:
                st.image(poster, width=135)  
            else:
                st.write("No poster available")

