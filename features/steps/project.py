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
                data = {'title': row['title'], 'completed': json.loads(row['completed']),
                        'active': json.loads(row['active']), 'description': row['description']}
                res = requests.post(urlProj, data=json.dumps(data))


@given('a project with "{title}" and "{completed}" and "{active}" and "{description}"')
def step_impl(context, title, completed, active, description):
    new_project = {}
    if title != "null": new_project['title'] = title
    if completed != "null": new_project['completed'] = json.loads(completed)
    if active != "null":
        try:
            new_project['active'] = json.loads(active)
        except json.decoder.JSONDecodeError:
            new_project['active'] = active
    if description != "null": new_project['description'] = description
    context.new_project = new_project

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


@given('a project with "{title}" exists')
def step_impl(context, title):
    response=requests.get(urlProj, data=json.dumps({'title': format(title)}))


    if(response.status_code==404):
        response=requests.post(urlProj, data=json.dumps({'title': format(title)}))
    context.project_id = response.json().get('projects')[0].get('id')
    context.project=response.json().get('projects')[0]
    context.title=response.json().get('projects')[0].get('title')
    assert response.status_code==200


@when("I delete the project")
def step_impl(context):
    response=requests.delete(urlProj+'/'+format(context.project_id))
    context.response=response

@then("the project is deleted")
def step_impl(context):
    response=requests.get(urlProj+'/'+format(context.project_id))
    assert response.status_code==404
    assert response.json().get("errorMessages") is not None


@given('a project with "{id}" not exist')
def step_impl(context, id):
    response = requests.get(urlProj + '/' + format(id))
    context.new_project = response.json()
    context.project_id = id
    assert response.status_code == 404


@when("I get the project by title")
def step_impl(context):
    response=requests.get(urlProj, data=json.dumps({'title': context.project.get('title')}))
    context.status_code=response.status_code
    context.project=response.json().get('projects')[0]
    context.response=response


@then("the response returns the project object")
def step_impl(context):
    assert context.project.get('title')== context.title


@when("I get the project by id")
def step_impl(context):
    response=requests.get(urlProj+'/'+format(context.project_id))
    context.response=response


@when('I update the project with "{new_title}"')
def step_impl(context, new_title):
    context.new_title=new_title
    response=requests.put(urlProj+'/'+format(context.project_id), data=json.dumps({'title':new_title}))
    context.response=response

@then("the project is updated")
def step_impl(context):
    assert context.response.status_code==200
    assert context.response.json().get('id') is not None
    if "new_title" in context:
        assert context.response.json().get("title")==context.new_title
    if "new_description" in context:
        assert context.response.json().get("description")==context.new_description


@given('a project with "{old_title}" and "{old_description}" exist')
def step_impl(context, old_title, old_description):
    response = requests.get(urlProj, data=json.dumps({'title': format(old_title), 'description':format(old_description)}))

    if (response.status_code == 404):
        response = requests.post(urlProj, data=json.dumps({'title': format(old_title),'description':format(old_description)}))
    context.project_id = response.json().get('projects')[0].get('id')
    assert response.status_code == 200


@when('I update the project with "{new_title}" and "{new_description}" together')
def step_impl(context, new_title, new_description):
    context.new_title, context.new_description= new_title, new_description
    response = requests.put(urlProj + '/' + format(context.project_id), data=json.dumps({'title': new_title, 'description':new_description}))
    context.response = response


@then("the project is not updated")
def step_impl(context):
    assert context.response.status_code == 404

    if "new_title" in context:
        assert context.response.json().get("title") == context.new_title
    if "new_description" in context:
        assert context.response.json().get("description") == context.new_description


@when('I get the project by "{title}" and "{description}"')
def step_impl(context, title, description):
    response = requests.get(urlProj, data=json.dumps({'title': format(title), 'description':format(description)}))
    context.status_code = response.status_code
    context.project = response.json().get('projects')[0]
    print(context.project)
    context.response = response
    context.title=title