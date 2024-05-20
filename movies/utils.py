import numpy as np
from collections import defaultdict
from math import sqrt

def normalize_ratings(prefs):
    normalized_prefs = defaultdict(dict)
    for user in prefs:
        ratings = prefs[user].values()
        mean = np.mean(list(ratings))
        for item in prefs[user]:
            normalized_prefs[user][item] = prefs[user][item] - mean
    return normalized_prefs

def sim_cosine(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)
    if n == 0:
        return 0

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    num = pSum
    den = sqrt(sum1Sq) * sqrt(sum2Sq)
    if den == 0:
        return 0

    similarity = num / den
    print(f"Similarity between user {p1} and user {p2} (Cosine): {similarity}, common items: {n}")
    return similarity

def get_recommendations(prefs, person, similarity=sim_cosine, min_sim=0.01):
    totals = defaultdict(float)
    simSums = defaultdict(float)
    scaling_factor = 1  # Factor to ensure significant weight for recommendations

    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other) * scaling_factor
        if sim <= min_sim:
            print(f"Skipping user {other} for user {person} due to non-positive similarity ({sim})")
            continue
        for item in prefs[other]:
            totals[item] += prefs[other][item] * sim
            simSums[item] += sim

    rankings = [(total / simSums[item], item) for item, total in totals.items() if simSums[item] != 0]
    rankings.sort(reverse=True)
    print(f"Rankings for user {person}: {rankings}")
    return rankings

def load_movie_ratings():
    from .models import MovieReview

    prefs = defaultdict(dict)
    for review in MovieReview.objects.all():
        prefs[review.user.id][review.movie.id] = review.rating
    print("Movie ratings loaded: ", prefs)
    normalized_prefs = normalize_ratings(prefs)
    print("Normalized movie ratings: ", normalized_prefs)
    return normalized_prefs
