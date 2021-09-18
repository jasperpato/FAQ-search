from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest

from algorithm import Algorithm

post_text = lambda post: post.subject if len(post.subject.split(' ')) >= 10 else post.payload

class Tfidf(Algorithm):
    vectorizer = None

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def similarity(self, post, posts, n):
        document_list = [post_text(p) for p in posts]
        document_list.insert(0, post_text(post))
        embeddings = self.vectorizer.fit_transform(document_list)

        scores = cosine_similarity(embeddings[0], embeddings[1:]).flatten()
        post_scores = {posts[i]:scores[i] for i in range(len(posts))}
        return nlargest(n, post_scores, key=post_scores.get)