# SudoFood 

How superusers do food!

This is an work in progress application. We are going to use machine learning to understand ingredients in recipes. With an ingredient level understanding the algorithm will be able to adjust and suggest recipes to users better than the ones on the market.

## Collaborators
Daniel Grzenda  
John Rumpel  
Danielle Savage  
Mathew Shaw  
Nimesh Sinha  

## Application Structure

Data_Aquistion/ - a place for all of our data acquistion scripts
* get_recipe_names.ipynb - exploratoring the yummly api  
* yummly_api.py - the main script for retreieving both ids and recipes  
* recipe_ids.txt - a file storing all the recipe ids from yummly  
* recipe_take2.txt - old data stored for backup  
* test.json - a test of converting it to json  

requirements.txt  
sudofood/ - the project directory (composed of apps)
* accounts/ - the current login and user app 
* login/ - an old app that allows login (Depricated next week)  
* manage.py - the main python file where we run the project from  
* sudofood/ - the main app fro the project  
* templates/ - where all the static files are stored  

venv/  
.gitignore   

## How to Run Our Application

source venv/bin/activate
pip3 install -r requirements.txt
cd sudofood/
python3 manage.py runserver  
go to http://localhost:8000

## Running the Data Acquistion Script
Need yummly key and id  
python yummly_api.py key id  
