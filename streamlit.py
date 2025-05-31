# streamlit_app.py
import streamlit as st
from main import load_data, item_based_recommender

st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("🎬 Movie Recommender System")

user_movie_df = load_data()

search_term = st.text_input("Search for a movie:")

selected_movie = None
if search_term:
    filtered_movies = [m for m in user_movie_df.columns if search_term.lower() in m.lower()]
    if filtered_movies:
        selected_movie = st.selectbox("Select a movie:", options=filtered_movies[:20])
    else:
        st.warning("No movies found.")
else:
    st.info("Start typing to search for a movie.")

if selected_movie:
    st.subheader(f"Movies similar to '{selected_movie}'")
    recommendations = item_based_recommender(user_movie_df, selected_movie)
    for i, (movie, score) in enumerate(recommendations.items(), 1):
        st.write(f"{i}. {movie} (Similarity: {score:.2f})")
