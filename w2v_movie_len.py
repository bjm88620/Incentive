import os, multiprocessing
import pandas as pd
import numpy as np
from math import log
from collections import Counter
from gensim.models import Word2Vec

def cosine_similarity(a, b):
    """
    Compute the cosine similarity between vectors a and b.
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def compute_center(model, movies_ratings, verbose):
    """
    Compute the center of user movie vectors.
    """
    center = np.zeros((model.vector_size,))
    total_weight = 0
    # iterating this way handles the problem when a movie might not be found in the model
    i = 0
    for movie in movies_ratings:
        try:
            movie_vec = model[movie]
            rating = movies_ratings[movie]
            center += rating * movie_vec
            total_weight += rating
        except KeyError:
            if verbose:
                print(f"{movie} not contained in model")
            continue
    center /= total_weight
    return center


def compute_score(model, movies_ratings, center, verbose):
    """
    Once we have computed the center we can then compute the GS-score based on the
    user's center and the cosine similarity between each movie vector and the center.
    We assume ratings are positive.
    """
    score, total_weight = 0, 0
    i = 0
    for movie in movies_ratings:
        try:
            movie_vec = model[movie]
            rating = movies_ratings[movie]
            score += rating * cosine_similarity(movie_vec, center)
            total_weight += rating
        except KeyError:
            if verbose:
                print(f"{movie} not contained in model")
            continue

    # removing some numerical errors
    return score / max(total_weight, 1.0)


def generalist_specialist_score(model, movies_ratings, verbose=False):
    """
    Based on the generalist-specialist score from Anderson et al.,
    "Algorithmic Effects on the Diversity of Consumption on Spotify".
    """
    center = compute_center(model, movies_ratings, verbose)
    score = compute_score(model, movies_ratings, center, verbose)
    return score


def compute_shannon_entropy(movie_list):
    """
    Compute Shannon Entropy of a user's movie diversity.
    """
    view_count = Counter(movie_list)
    total_movies = sum(view_count.values())
    entropy = 0
    for value in view_count.values():
        p = value / total_movies
        entropy += -p * log(p, 2)
    return entropy
base_path = r'P:/Downloads/ml-latest-small/ml-latest-small/'

ratings_path = os.path.join(base_path, "ratings.csv")

ratings_df = pd.read_csv(ratings_path)

ratings_df["date"] = pd.to_datetime(ratings_df["timestamp"], unit="s")
ratings_df["month"] = ratings_df["date"].dt.month
ratings_df["year"] = ratings_df["date"].dt.year
ratings_df["movieId"] = ratings_df["movieId"].apply(str)
print(ratings_df.info())
users_movies = ratings_df.sort_values(by=["timestamp"]).groupby(
    "userId",
    as_index=False
).apply(
    lambda x: dict(zip(x["movieId"], x["rating"]))
).reset_index(name="movie_id_ratings")

print(users_movies)

# model parameters
ITEM_VECTOR_SIZE = 60  # dimension of word vector size (multiple of 4 for best performance)
MIN_ITEM_COUNT = 5 # minimum number of times a word must appear in the dataset to be included as a word vector
WINDOW_SIZE = 5

movies_list = users_movies["movie_id_ratings"].apply(lambda x: list(x.keys()))


cores = multiprocessing.cpu_count()
model = Word2Vec(min_count=MIN_ITEM_COUNT,
                     window=WINDOW_SIZE,
                     size=ITEM_VECTOR_SIZE,
                     workers=cores-1)

model.build_vocab(movies_list, progress_per=10000)

model.train(movies_list, total_examples=model.corpus_count, epochs=15, report_delay=1)
model.init_sims(replace=True)



users_movies["gs_score"] = users_movies["movie_id_ratings"].apply(lambda x: generalist_specialist_score(model, x))


print(model.most_similar('500'))
