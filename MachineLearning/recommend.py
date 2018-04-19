import boto3
import pandas as pd
import gensim
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import string
from sklearn.decomposition import PCA
from matplotlib import pyplot
import pickle
import re
import sys

global tfidf
global tfidf1

first_arg = sys.argv[1]

recipe_id = pickle.load(open("recipe_id.pkl", "rb"))
ingredients = pickle.load(open("ingredients.pkl", "rb"))

words = [x.split(' ') for item in ingredients for x in item]
words = [x for item in words for x in item]

ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", "\xc2\xbc", "\xc2\xbd", "cup", "cups", "ounces", "ounce",
    "teaspoon", "tablespoon", "tablespoons", "teaspoons", "extract"])


def tokeniser(text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    text = regex.sub(" ", text.lower())
    words = text.split(" ")
    words = [w for w in words if not len(w) < 2]
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return words


tfidf = TfidfVectorizer(tokenizer=tokeniser, stop_words=ENGLISH_STOP_WORDS).\
                        fit(words)


def cosine_sim(text1, text2):
    tfidf_score = TfidfVectorizer().fit_transform([text1, text2])
    return ((tfidf_score * tfidf_score.T).A)[0, 1]


new_recipe_id = [' '.join(x.split('-')[:-1]) for x in recipe_id]


# Creating a dataframe with recipe name and ingredients
df1 = pd.DataFrame(columns=['name', 'ingredients'])
df1.name = new_recipe_id
df1.ingredients = ingredients
r = [x.split(' ') for x in df1['name']]
r = [x for item in r for x in item]
tfidf1 = TfidfVectorizer(tokenizer=tokeniser, stop_words=ENGLISH_STOP_WORDS).\
                                            fit(r)


def cosine_sim_recipe(text1, text2):
    z = tfidf1.fit_transform([text1, text2])
    return ((z * z.T).A)[0, 1]


def closest_recipe_name(recipe_name, df):
    """
    Takes the recipe name as input and finds the
    closest receipe in our database on the basis
    of name
    """
    cos = []
    names_list = df.name
    for i in range(len(names_list)):
        cos.append([names_list[i],
                    cosine_sim_recipe(', '.join(recipe_name.split(' ')),
                                      ', '.join(names_list[i].split(' ')))])
    return sorted(cos, key=lambda x: -x[1])[0][0]


def recommend_recipes(name, df):
    """
    Takes the closest recipe name found in our database
    and recommends the top ten closest recipe names on basis
    of ingredients
    """
    recipe_name = closest_recipe_name(name, df)
    cos = []
    recommended_recipes = []
    ingredient = df[df['name'] == recipe_name].ingredients
    ingredients_list = df.ingredients
    names = df.name
    for i in range(len(ingredients_list)):
        cos.append([names[i], cosine_sim(', '.join(ingredient.tolist()[0]),
                    ','.join(ingredients_list[i]))])
    return sorted(cos, key=lambda x: -x[1])[0:10]


print(recommend_recipes(first_arg, df1))
