import boto3
import pandas as pd
import gensim
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import string
from sklearn.decomposition import PCA
from matplotlib import pyplot


def get_ingredients(bucket_name):
    """
    Receives the json files from S3 bucket
    and puts the recipe id and ingredients
    in list

    Parameters:
        bucket_name (str obj)

    Return:
        A tuple of the recipe id and ingredients from the bucket
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    ingredients = []
    recipe_id = []
    for obj in bucket.objects.all():
        print(obj)
        key = obj.key
        if key.endswith('json'):
            body = obj.get()['Body'].read()
            data = json.loads(body)
            for j in range(len(data)):
                try:
                    recipe = json.loads(data[j])
                    ingredients.append(recipe['ingredientLines'])
                    recipe_id.append(recipe['id'])
                except ValueError:
                    continue
    return (recipe_id, ingredients)


recipe_id, ingredients = get_ingredients('sudofood')
with open('recipe_id.pkl', 'wb') as f:
    pickle.dump(recipe_id, f)
with open('ingredients.pkl', 'wb') as f:
    pickle.dump(ingredients, f)
