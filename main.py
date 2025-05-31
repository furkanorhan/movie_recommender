import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=True)
def load_data():
    movie = pd.read_csv('dataset/movie.csv')
    rating = pd.read_csv('dataset/rating.csv')

    df = movie.merge(rating, how='left', on='movieId')

    comment_counts = pd.DataFrame(df["title"].value_counts())
    comment_counts.columns = ["count"]

    rare_movies = comment_counts[comment_counts["count"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]

    user_movie_df = common_movies.pivot_table(index='userId', columns='title', values='rating')

    return user_movie_df

def item_based_recommender(user_movie_df, movie_name):
    if movie_name not in user_movie_df.columns:
        return pd.Series(dtype=float)

    movie_ratings = user_movie_df[movie_name]
    similar_scores = user_movie_df.corrwith(movie_ratings).sort_values(ascending=False)
    similar_scores = similar_scores.dropna()
    similar_scores = similar_scores[similar_scores.index != movie_name]
    return similar_scores.head(10)