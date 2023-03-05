from behave import *
import requests

url = "http://localhost:4567/"

def reset():
    #Resetting todos
    response = requests.get(url + "todos")
    request_data = response.json()
    todos = request_data["todos"]
    for todo in todos:
        if int(todo["id"])==1 or int(todo["id"])==2 : continue
        requests.delete(url + f"/todos/{todo['id']}")

    #Resetting projects
    response = requests.get(url + "projects")
    request_data = response.json()
    projects = request_data["projects"]
    for project in projects:
        if int(project["id"])==1: continue
        requests.delete(url + f"/projects/{project['id']}")

    #Resetting categories
    response = requests.get(url + "categories")
    request_data = response.json()
    categories = request_data["categories"]
    for category in categories:
        if int(category["id"])==1 or int(category["id"])==2 : continue
        requests.delete(url + f"categories/{category['id']}")

# Before each feature file
def before_feature(context, feature):
    pass

# Before each scenario
def before_scenario(context, scenario):
    reset()

# Before each step
def before_step(context, step):
    # steps are the individual steps in a scenario
    # such as "Given ...", "When ...", "Then ..."
    pass

