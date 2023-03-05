from behave import *
import requests
import json
import subprocess

url = 'http://localhost:4567/'

@given('the following todo instances exist in the database:')
def step_impl(context):
    res = requests.get(url+'todos')
    assert res.status_code == 200
    response = requests.get(url+'todos')
    request_data = response.json()
    todos = request_data["todos"]
    # for row in context.table:
    if context.table[0].get('id') is not None:
        ids = [todo['id'] for todo in todos]
        titles = [todo['title'] for todo in todos]
        assert context.table[0]['id'] in ids
        assert context.table[0]['title'] in titles
        assert context.table[1]['id'] in ids
        assert context.table[1]['title'] in titles
    else:
        for row in context.table:
            if row['title'] not in [todo['title'] for todo in todos]:
                data = {'title': row['title'], 'doneStatus': row['doneStatus'], 'description': row['description']}
                res = requests.post(url+'todos', data=json.dumps(data))

@when('the user makes a request to create a todo instance with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
    newTodo = {}
    if title != "null":
        newTodo['title'] = title
    if doneStatus != "null":
        newTodo['doneStatus'] = doneStatus
    if description != "null":
        newTodo['description'] = description
    context.newTodo = newTodo
    response = requests.post(url+'todos', data=json.dumps(context.todos))
    context.response = response


@then('the “rest api todo list manager” adds the new todo instance to the database')
def step_impl(context):
    context.newTodo['id'] = context.response.json().get("id")
    assert context.response.status_code == 201
    assert context.response.json().get("id") is not None
    assert context.response.json().get("title") == context.newTodo['title']
    if 'doneStatus' in context.newTodo:
        assert context.response.json().get("doneStatus") == context.newTodo['doneStatus']
    if 'description' in context.newTodo:
        assert context.response.json().get("description") == context.newTodo['description']


@then('the “rest api todo list manager” returns an error message "{error}"')
def step_impl(context, error):
    response = requests.get(url+f'todos?doneStatus={context.newTodo["doneStatus"]}&description={context.newTodo["description"]}')
    todos = response.json().get("todos")
    assert context.response.status_code == 400
    assert context.response.json().get("id") is None
    assert len(todos) == 0
    error = context.response.json().get("errorMessages")
    assert len(error) == 1
    assert message in error[0]






