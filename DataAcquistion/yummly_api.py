import numpy as np
import pandas as pd
import requests
import json
import boto3
import sys

# The ID and KEYS needed to access the Yummly API
ID = sys.argv[1]
KEY = sys.argv[2]


def recipe_search(search_params=None):
    """Returns recipe ids from YummlyAPI based on the given search parameters.

    Parameters
    ----------
    search_params : dict
        Any parameters that the user wishes to search by
    """
    if(search_params is None):
        response = requests.get('http://api.yummly.com/v1/api/recipes?_'
                                'app_id=%s&_app_key=%s' % (ID, KEY)).json()
    else:
        response = requests.get('http://api.yummly.com/v1/api/recipes?_'
                                'app_id=%s&_app_key=%s&%s'
                                % (ID, KEY, search_params)).json()
    return response


def get_one_recipe(recipe_id):
    """ Returns the corresponding recipe for each recipe id

    Parameters
    ----------
    recipe_id : str
        Recipe id that was pulled from search recipe
    """
    response = requests.get('http://api.yummly.com/v1/api/recipe/'
                            '%s?_app_id=%s&_app_key=%s' % (recipe_id, ID, KEY))
    return response


def build_list():
    """
    For every 10 recipes pulled, this function dumps said recipes into a
    single json file and uploads it to the S3 bucket.
    """
    with open('recipe_ids.txt') as f:
        all_recipes = f.readlines()
    all_recipes = [x.strip() for x in all_recipes]
    data = []
    for i, recipe_id in enumerate(all_recipes)[1002:]:
        if len(recipe_id) > 1:
            response = get_one_recipe(recipe_id)
            data.append(response.text)
        if i % 1000 == 0:
            s3 = boto3.resource('s3')
            obj = s3.Object('sudofood', 'recipes/recipe_json%s.json' % (i))
            obj.put(Body=json.dumps(data))
            data = []


#build_list()
