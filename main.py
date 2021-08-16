import sys
from parse_file import parse_file
from thread import Thread
from post import Post
from algorithm import pipe_line
import nltk
from re import sub
from string import ascii_letters

nltk.download('punkt')
nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

if __name__=="__main__":
    threads = parse_file(sys.argv[1])
    new_post = Post(None,None,None,None)
    print("Enter a new post and view the most similar existing posts.")
    new_post.subject = input("Subject: ")
    new_post.payload = input("Question body: ")
    N = 3 # number of most similar posts

    substitutes = ( lambda x: x.lower(),                # lowercase all text
                    lambda x: sub(r'\s+', ' ', x))      # remove extraneous spaces

    filters = (  lambda x: x not in ascii_letters,       # take non-alphabetical words out
                lambda x: x in stopwords)               # remove stopwords

    weights = [ lambda x: 1.5 if x.verified else 1.0]   # give a bit more priority to Chris' posts

    for p in pipe_line(new_post, threads, substitutes, filters, weights, N):
        print(p)

        