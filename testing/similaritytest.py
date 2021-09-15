import json
import datetime
import pickle
import time
import nltk
import os
import sys
from re import sub
from os.path import dirname, join
from string import ascii_letters

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from post import Post
from weights import date_weight, verified_weight
from pipeline import pipeline
from parse_file import valid, group_into_threads
from algorithms import cosine_similarity, jaccard
from alt_similarity_algorithms.tfidf import tfidf_similarity
from alt_similarity_algorithms.use import use_similarity, load_use_model

nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

cleaner =  (lambda x: x.lower(),                # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))      # remove extraneous spaces and punctuation

filters =  (lambda x: x not in ascii_letters,       # take non-alphabetical words out
            lambda x: x in stopwords)               # remove stopwords

weights = (verified_weight, date_weight)
#[lambda x: 1.5 if x.verified else 1.0]    # give a bit more priority to Chris's posts
substitutes = tuple([])


# Similarity test. A set of 'targets' are handpicked for each test case in
# the test_case_2019.json file and stored in the test_space_2019_2.json file. The 
# score of an individual test case is calculated by counting the number of posts in 
# the returned top posts had categories that intersected with the test case's categories, 
# and dividing by the number of targets. This score is averaged over all test cases. Provides
# a similarity score for an algorithm in the situation where the optimal targets are known.

def pipeline_test(algo):
    encodings = None
    if algo == 'use':
        load_use_model(use_cpu=True)
        f_path = join(dirname(__file__), '../../encodings/use/test_space_2019.pickle')
        with open(f_path, 'rb') as handle:
            encodings = pickle.load(handle)

    test_space = json.load(open("testing/test_space_2019.json"))["testcases"]
    test_case_posts = json.load(open("testing/test_case_2019.json"))["testcases"]
    score_sum = 0
    time_sum = 0
    for i, test_case in enumerate(test_case_posts):
        print(f"{i + 1}'th Test Case")
        print(f"Subject: {test_case['Subject']}\n")
        print(f"body: {test_case['Body']}\n")
        print("________________________")
        ###
        algo_result = evaluate_algo(algo, test_case, test_space, test_case['target_count'], encodings)
        print(f"Time taken: {algo_result['time']}\n")
        print("________________________")
        ###
        target_categories = set(test_case['Category'].split(' '))
        sum = 0
        for j, post in enumerate(algo_result['top_posts']):
            post_json = [tp for tp in test_space if tp['Body'] == post.payload][0]
            post_categories = set(post_json['Category'].split(' '))
            sum = sum+1 if len(target_categories.intersection(post_categories)) > 0 else sum
            print(f"\t{j + 1}'th Post:") 
            print(f"post category: {post_categories}\n")
            print(f"target category: {target_categories}\n")
            print(f"{post}")
            print("________________________")
        score_sum += sum / test_case["target_count"]
        time_sum += algo_result['time']
        print(f'Total matches identified:{sum}\n')
        print(f'Number of targets existing:{test_case["target_count"]}\n')
        print(f'Recall: {sum / test_case["target_count"]}\n')
        print("<<=====================================>>")
    print('FINAL SCORE:', score_sum / len(test_case_posts))
    print('AVERAGE_ALGO_TIME:', time_sum / len(test_case_posts))
    print("<<=====================================>>\n")


# Similarity test. The score between an input post and set of output posts is 
# calculated by averaging the tag intersection between the input post and the 
# generated top posts and dividing by the optimal tag intersection (i.e., if a tag matching 
# algorithm was used). This score is averaged over all posts in test_space_2019_2.json 
# tested against all other posts in test_space_2019_2.json. Provides
# a similarity score for an algorithm in the situation where a reasonable
# sample of the dataset is tagged.

def tag_intersection_test(algo, n):
    encodings = None
    if algo == 'use':
        load_use_model(use_cpu=False)
        f_path = join(dirname(__file__), '../../encodings/use/test_space_2019_2.pickle')
        with open(f_path, 'rb') as handle:
            encodings = pickle.load(handle)

    overall_test_space = json.load(open("testing/test_space_2019_2.json"))["test_space"]
    overall_score_sum = 0
    num_tests = 0
    for case in overall_test_space:
        target_categories = set(case['Tags'])
        space = overall_test_space[:]; space.remove(case)
        algo_result = evaluate_algo(algo, case, space, n, encodings)
        sum = 0
        for post in algo_result['top_posts']:
            post_json = [tp for tp in space if tp['Body'] == post.payload][0]
            post_categories = set(post_json['Tags'])
            score = len(post_categories & target_categories) / len(target_categories)
            sum += score
        gt_similarity = optimal_tag_intersection(case, space, n)
        if gt_similarity != 0:
            overall_score_sum += sum / n / gt_similarity
            num_tests += 1
    print("<<=====================================>>")
    print('FINAL SCORE:', overall_score_sum / num_tests)
    print("<<=====================================>>")  


# Evaluates the given algorithm to produce a tuple with the format
# (top_posts, time_taken), where top_posts is ordered from most similar
# to least similar.

def evaluate_algo(algo, test_case, test_space, n, encodings=None):
    start_time = time.process_time()
    if 'Category' in test_case.keys():
        input_post = parse_test_case(test_case)
        all_posts = [json_to_post_1(p) for p in test_space]
    else:
        input_post = json_to_post_2(test_case)
        all_posts = [json_to_post_2(p) for p in test_space]

    if algo == 'basic':
        algs = (cosine_similarity, jaccard)
        top_posts = pipeline(input_post, group_into_threads(all_posts), cleaner, filters, substitutes, weights, algs, n)

    elif algo == 'tfidf':
        top_posts = tfidf_similarity(input_post, all_posts, n)

    elif algo == 'use':
        top_posts = use_similarity(input_post, encodings, all_posts, n)
    return {'top_posts': top_posts, 'time': time.process_time() - start_time}


# Used for converting json objects (stored in test_space_2019.json) into post objects

def json_to_post_1(post):
    date = datetime.datetime.strptime(post["Date"], "%a %b %d %H:%M:%S %Y")
    verified = post['From'] in valid
    return Post(date, post['Subject'], post['Body'], verified)


# Used for converting json objects (stored in test_case_2019.json) into post objects

def parse_test_case(post):
    return Post(None, post['Subject'], post['Body'], False)


# Because I (Allen) am an absolute Bonobo, the new test_space (test_space_2019_2.json)
# I made has a different json format than test_space_2019.json, hence this function

def json_to_post_2(post):
    date = datetime.datetime.strptime(post["Date"], "%Y-%m-%d %H:%M:%S")
    return Post(date, post['Subject'], post['Body'], post['Verified'])


# Returns the average similarity score (tag intersection) using an algorithm that utilises 
# tag intersection to find post similarity. I.e., finds the average tag intersection using 
# an optimal similarity function for a test_case and test_space.

def optimal_tag_intersection(test_case, test_space, n):
    intersection_score = lambda list1, list2: len(set(list1) & set(list2)) / len(list1)
    scores = [intersection_score(test_case['Tags'], post['Tags']) for post in test_space]
    scores.sort(reverse=True)
    return sum(scores[0:n]) / n


if __name__ == '__main__':   
    pipeline_test('basic')
