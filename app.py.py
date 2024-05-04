import streamlit as st
import  pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    # Construct the URL with the provided movie_id
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'

    # Send a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the 'poster_path' key exists in the response
        if 'poster_path' in data and data['poster_path'] is not None:
            # Construct the URL for the poster image
            poster_url = f"https://image.tmdb.org/t/p/original{data['poster_path']}"
            return poster_url
        else:
            # If 'poster_path' is not available, return None
            return None
    else:
        # If the request was not successful, print an error message and return None
        print(f"Error fetching poster for movie with ID {movie_id}: {response.status_code}")
        return None


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster of movies from API.
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity= pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')


Selected_Movie_Name= st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

if st.button('Recommend'):
    names,posters= recommend(Selected_Movie_Name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
        st.empty()
    with col2:
        st.header(names[1])
        st.image(posters[1])
        st.empty()
    with col3:
        st.header(names[2])
        st.image(posters[2])
        st.empty()
    with col4:
        st.header(names[3])
        st.image(posters[3])
        st.empty()
    with col5:
        st.header(names[4])
        st.image(posters[4])
        st.empty()
