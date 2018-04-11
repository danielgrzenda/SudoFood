import numpy as np
import pandas as pd
import requests
import json

ID = '61b7fa8a'
KEY = '10dc6fd573524c488bcef197bcebaaf4'

def recipe_search(search_params=None):
    if(search_params == None):
        response = requests.get('http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s'%(ID,KEY)).json()
    else:
        response = requests.get('http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&%s'%(ID,KEY,search_params)).json()
    return response

def get_one_recipe(recipe_id):
    response = requests.get('http://api.yummly.com/v1/api/recipe/rs==%s?_app_id=%s&_app_key=%s'%(recipe_id,ID,KEY)).json()
    return response

def build_list()
