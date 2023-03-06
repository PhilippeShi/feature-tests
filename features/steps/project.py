from behave import *
import requests
import json

urlProj = 'http://localhost:4567/projects'

#use_step_matcher("re")


@step("the following project exist")
def step_impl(context):
    response = requests.get(urlProj)
    request_data = response.json()
    projects = request_data["projects"]
    if context.table[0].get('id') is not None:
        ids = [project['id'] for project in projects]
        titles = [project['title'] for project in projects]
        completed = [project['completed'] for project in projects]
        active = [project['active'] for project in projects]
        description = [project['description'] for project in projects]
        assert context.table[0]['id'] in ids
        assert context.table[0]['title'] in titles
        assert context.table[0]['completed'] in completed
        assert context.table[0]['active'] in active
        assert context.table[0]['description'] in description
    else:
        for row in context.table:
            if row['title'] not in [project['title'] for project in projects]:
                data = {'title': row['title'], 'completed': row['completed'],
                        'active': row['active'], 'description': row['description']}
                res = requests.post(urlProj, data=json.dumps(data))


@given('a project with "{title}" and "{completed}" and "{active}" and "{description}"')
def step_impl(context, title, completed, active, description):
    new_project = {}
    if title != "null": new_project['title'] = title
    if completed != "null": new_project['completed'] = json.loads(completed)
    if active != "null": new_project['active'] = json.loads(active)
    if description != "null": new_project['description'] = description
    context.new_project = new_project
    print(new_project)

@when("I create the project")
def step_impl(context):
    response = requests.post(urlProj, data=json.dumps(context.new_project))
    context.response = response


@then("the project is created")
def step_impl(context):
    context.new_project['id'] = context.response.json().get("id")
    assert context.response.status_code == 201
    assert context.response.json().get("id") is not None
    try:
        assert context.response.json().get("title") == context.new_project['title']
    except KeyError:
        i=0
    try:
        assert json.loads(context.response.json().get("completed")) == context.new_project['completed']
    except KeyError:
        i=0
    assert json.loads(context.response.json().get("active")) == context.new_project['active']
    if 'description' in context.new_project:
        assert context.response.json().get("description") == context.new_project['description']


@step("the new project object is different from the existing project")
def step_impl(context):
    response = requests.get(urlProj + '?title=' + format(context.new_project["title"]))
    projects = response.json().get("projects")
    assert len(projects) > 0
    assert projects[0]['id'] != ""


@then("the project is not created")
def step_impl(context):
    response = requests.get(urlProj + '?description=' + format({context.new_project["description"]}))
    projects = response.json().get("projects")
    assert context.response.status_code == 400
    assert context.response.json().get("id") is None
    assert len(projects) == 0


