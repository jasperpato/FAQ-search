from collections import Counter
from math import sqrt
from typing import List, Set
from utils import merge

Vector = List[float]
Tokens = List[str]

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