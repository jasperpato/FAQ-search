import tensorflow_hub as hub

import numpy as np
import pandas as pd
from heapq import nlargest
from sklearn.metrics.pairwise import cosine_similarity
import json
import nltk

from post import Post
from thread_obj import Thread, all_posts


# load universal sentence encoder module
encoder  = None
post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload


def load_use_model():
    global encoder
    encoder = hub.load('../pretrained_models/universal-sentence-encoder_4')


# return a pandas dataframe that includes the similarity between every post. 
# can be used to generate clusters
def get_similarity_dataframe(posts, encoded_posts, encoder):
    num_posts = len(posts)
    similarities_df = pd.DataFrame()
    for i in range(num_posts):
        for j in range(num_posts): 
            # cos(theta) = x . y / (mag_x * mag_y)
            cos_theta = cosine_similarity(encoded_posts[i], encoded_posts[j])
            similarities_df = similarities_df.append(
                {
                    'similarity': cos_theta, 
                    'post1': posts[i], 
                    'post2': posts[j]
                },
                ignore_index=True
            )


# Identical in use-case to the function defined in algorithm.py
def use_similarity(post, encoded_posts, posts, n):
    in_vec = encoder([post_text(post)])
    scores = cosine_similarity(in_vec, encoded_posts)
    post_score_map = {posts[i]:scores[i] for i in range(len(posts))}
    return tuple(nlargest(n, post_score_map, key=post_score_map.get))


def encode_posts(posts, save_name):
    encoded_posts = encoder([post_text(post) for post in posts])
    np.save(f'../encodings/use/{save_name}', encoded_posts)
    return encoded_posts


if __name__== '__main__':
    from testing.similaritytest import parse_post

    test_space_posts = json.load(open("testing/test_space_2019.json"))["testcases"]
    posts = [parse_post(p) for p in test_space_posts]
    load_use_model()
    encode_posts(posts, 'test_space.npy')


    
