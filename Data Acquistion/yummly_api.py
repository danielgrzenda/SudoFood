import numpy as np
import pandas as pd
import requests
import json
import boto3

ID = '8738e7a2'
KEY = '234f4fe2774becb61689975054fb6d03'

#CONN = boto.connect_s3('AKIAJWS4ZY2SMW6AXTGQ', '17gowsdljqy7908eKykX6W9YBJttlH3H9/aSIYxr')
#BUCKET = CONN.get_bucket('sudofood', validate=False)

def recipe_search(search_params=None):
    if(search_params == None):
        response = requests.get('http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s'%(ID,KEY)).json()
    else:
        response = requests.get('http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&%s'%(ID,KEY,search_params)).json()
    return response

def get_one_recipe(recipe_id):
    response = requests.get('http://api.yummly.com/v1/api/recipe/%s?_app_id=%s&_app_key=%s'%(recipe_id,ID,KEY))
    return response

def build_list():
    with open('recipe_ids.txt') as f:
        all_recipes = f.readlines()
    all_recipes = [x.strip() for x in all_recipes]
    all_recipes = all_recipes[:50]
    for i, recipe_id in enumerate(all_recipes):
        data = []
        if len(recipe_id) > 1:
            print(recipe_id)
            data.append(str(get_one_recipe(recipe_id).text))

        if i%10 == 0:
            s3 = boto3.resource('s3')
            obj = s3.Object('sudofood', 'recipe_json%s.json'%(i))
            obj.put(Body=json.dumps(data))
            data = []

build_list()
