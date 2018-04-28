import pickle
import re
import string
from nltk.tokenize import word_tokenize
import gensim
global ingredients
global b

recipe_id = pickle.load( open( "recipe_id.pkl", "rb" ) )
ingredients = pickle.load( open( "ingredients.pkl", "rb" ) )
df = pickle.load( open( "df.pkl", "rb" ) )
with open('nutrients.pkl', 'rb') as f:
    b = pickle.load(f)


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
    "yourselves", "\xc2\xbc", "\xc2\xbd", "cup", "cups","ounces","ounce",
    "teaspoon", "tablespoon", "tablespoons", "teaspoons"," extract", 'tbsp', 'teaspoon', 'lb', 'pound', 'tsp', 'cup', 'gms', 'powder',
       'medium', 'g', 'stick', 'whole', 'tablespoon', 'quarts', 'ounce',
       'ml', 'can', 'package', 'oz', 'room', 'temperature', 'ounce'])



def tokeniser(text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    text = regex.sub(" ", text.lower())
    words = text.split(" ")
    words = [w for w in words if not len(w) < 2]
    words = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return words


def similarity_object(ingredients):
    ing = [' '.join(x) for x in ingredients]
    gen_docs = [[w.lower() for w in tokeniser(text)] for text in ing]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity.load('similarity', mmap=None)
    #sims = gensim.similarities.Similarity('/Users/nimesh/Documents/Spring2/app',tf_idf[corpus],num_features=len(dictionary))
    return sims,dictionary,tf_idf


def recommend(ingredients,string):
    sims,dictionary,tf_idf = similarity_object(ingredients)
    query_doc = [w.lower() for w in tokeniser(string)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    rec_recipe = [recipe_id[x] for x in sims[query_doc_tf_idf].argsort()[-3:][::-1]]
    new_ing  = [ingredients[x] for x in sims[query_doc_tf_idf].argsort()[-3:][::-1]]
    print(new_ing)
    
    z = sorted(range(len([b[x] for x in sims[query_doc_tf_idf].argsort()[-3:][::-1]])),
           key=lambda x:[b[y] for y in sims[query_doc_tf_idf].argsort()[-3:][::-1]][x][0][2])
    
    rec_ing = [new_ing[x] for x in z]
    

recommend(ingredients,"Ture, bun")
    
    






