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
    response = requests.post(url+'todos', data=json.dumps(context.newTodo))
    context.response = response


@then('the “rest api todo list manager” adds the todo instance to the database')
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
    error = context.response.json().get("errorMessages")
    assert len(error) == 1
    assert message in error[0]


@when('the user makes a request to delete a todo instance with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
   response = requests.get(url+f'todos?title={title}&doneStatus={doneStatus}&description={description}')
   todo = response.json().get("todos")
   if len(todo) == 0:
       context.todo_id = -1
   else:
       context.todo_id = todo[0]['id']
   response = requests.delete(url+f'todos/{context.todo_id}')
   context.response = response


@then('the “rest api todo list manager” deletes the todo instance from the database')
def step_impl(context):
    response = requests.get(url+f'todos/{context.todo_id}')
    laa = context.todo_id
    context.todo_id = laa
    assert response.status_code == 404
    assert response.json().get("errorMessages") is not None
    assert context.response.status_code == 200


@when('When the user makes a request to delete a todo instance identified by id "<id>" with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, id, title, doneStatus, description):
    response = requests.get(url+f'todos/{id}')
    context.response = response

@when('the user makes a request to get a todo instance with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
   response = requests.get(url+f'todos?title={title}&doneStatus={doneStatus}&description={description}')
   todo = response.json().get("todos")
   if len(todo) == 0:
       context.todo_id = -1
   else:
       context.todo_id = todo[0]['id']
   response = requests.get(url+f'todos/{context.todo_id}')
   context.response = response


@then('the “rest api todo list manager” returns a todo instance from the database')
def step_impl(context):
    response = requests.get(url+f'todos/{context.todo_id}')
    laa = context.todo_id
    context.todo_id = laa
    assert response.status_code == 200
    assert context.response.status_code == 200
    assert response.json().get("errorMessages") is not None

@when('the user makes a request to update a todo instance titled "{title}" with fields title "{newTitle}", doneStatus "{newDoneStatus}", and description "{newDescription}"')
def step_impl(context, title, newTitle, newDoneStatus, newDescription):
   newTodo = {}
   if title != "null":
       newTodo['title'] = newTitle
   if doneStatus != "null":
       newTodo['doneStatus'] = newDoneStatus
   if description != "null":
       newTodo['description'] = newDescription
   context.newTodo = newTodo
   todo_id = requests.get(url+f'todos?title={title}').json()['todos'][0]['id']
   response = requests.post(url+f'todos/{context.todo_id}', data=json.dumps(context.newTodo))
   context.response = response
   context.todo_id = todo_id


@then('the “rest api todo list manager” updates the todo instance from the database')
def step_impl(context):
    print(context.response.json())
    print(context.response.status_code)
    assert context.response.status_code == 200
    assert context.response.json().get("id") is not None
    if "newTitle" in context:
        assert context.response.json().get("title") == context.newTitle
    if "newDoneStatus" in context:
        assert context.response.json().get("doneStatus") == context.newDoneStatus
    if "newDescription" in context:
        assert context.response.json().get("description") == context.newDescription


@when('When the user makes a request to update a todo instance identified by id "<id>" with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, id, title, doneStatus, description):
    response = requests.get(url+f'todos/{id}')
    context.response = response




