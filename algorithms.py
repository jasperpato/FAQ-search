from collections import Counter
from math import sqrt
from typing import List, Set
from utils import merge
from project_types import Tokens, Vector

def dot_product(xs : Vector, ys : Vector) -> float:
    return sum([x*y for (x,y) in zip(xs,ys)])

def norm(xs : Vector) -> float:
    return sqrt(dot_product(xs,xs))

def word_vector(toks : Tokens, words : Set[str]) -> Vector:
    return list(merge({w : 0 for w in words}, Counter(toks)).values())

def cosine_similarity(A : Tokens, B : Tokens) -> float:
    if(len(A) == 0 or len(B) == 0):
        return 0.0
    all_words = set(A) | set(B)
    A_vec = word_vector(A, all_words)
    B_vec = word_vector(B, all_words)
    return dot_product(A_vec, B_vec) / (norm(A_vec) * norm(B_vec))

# calculates the intersection / union of two lists of tokens
# assumes there are no duplicates within A or B
def jaccard(A : Tokens, B : Tokens) -> float:
    union = len(A)
    intersection = 0
    for s in B:
        if s not in A:
            union += 1
        else:
            intersection += 1
    return intersection / union
    