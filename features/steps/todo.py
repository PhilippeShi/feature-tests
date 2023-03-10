from behave import *
import requests
import json
import subprocess

url = 'http://localhost:4567/todos'


@given('the following todo instances exist in the database')
def step_impl(context):
    response = requests.get(url)
    request_data = response.json()
    todos = request_data["todos"]
    if context.table[0].get('id') is not None:
        ids = [todo['id'] for todo in todos]
        titles = [todo['title'] for todo in todos]
        dones = [todo['doneStatus'] for todo in todos]
        dess = [todo['description'] for todo in todos]
        assert context.table[0]['id'] in ids
        assert context.table[0]['title'] in titles

        assert context.table[1]['id'] in ids
        assert context.table[1]['title'] in titles
    else:
        for row in context.table:
            if row['title'] not in [todo['title'] for todo in todos]:
                data = {'title': row['title'], 'doneStatus': json.loads(row['doneStatus']),
                        'description': row['description']}
                res = requests.post(url, data=json.dumps(data))


@when('the user makes a request to create a todo instance with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
    newTodo = {}
    if title != "null": newTodo['title'] = title
    if doneStatus != "null":
        newTodo['doneStatus'] = json.loads(doneStatus)
    if description != "null":
        newTodo['description'] = description
    context.newTodo = newTodo
    response = requests.post(url, data=json.dumps(context.newTodo))
    context.response = response
    context.todo_id = response.json().get("id")


@then('the “rest api todo list manager” adds the todo instance to the database')
def step_impl(context):
    context.newTodo['id'] = context.response.json().get("id")
    assert context.response.status_code == 201
    assert context.response.json().get("id") is not None
    assert context.response.json().get("title") == context.newTodo['title']
    if 'doneStatus' in context.newTodo:
        assert json.loads(context.response.json().get("doneStatus")) == context.newTodo['doneStatus']
    if 'description' in context.newTodo:
        assert context.response.json().get("description") == context.newTodo['description']


@when('the user makes a request to delete a todo instance with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
    response = requests.get(url, data=json.dumps(
        {'title': format(title), 'doneStatus': doneStatus, 'description': format(description)}))

    todo = response.json().get("todos")
    if len(todo) == 0:
        context.todo_id = -1
    else:
        context.todo_id = todo[0]['id']
        response = requests.delete(url + f'/{context.todo_id}')
        context.response = response


@then('the “rest api todo list manager” deletes the todo instance from the database')
def step_impl(context):
    response = requests.get(url + '/' + format(context.todo_id))
    assert response.status_code == 404
    assert response.json().get("errorMessages") is not None
    assert context.response.status_code == 200


@when('the user makes a request to delete a todo instance identified by id "{id}" with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, id, title, doneStatus, description):
    response = requests.get(url + f'/{id}')
    context.response = response
    context.todo_id = id


@when('the user makes a request to get a todo instance with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, title, doneStatus, description):
    response = requests.get(url + f'?title={title}&doneStatus={doneStatus}&description={description}')
    todo = response.json().get("todos")
    if len(todo) == 0:
        context.todo_id = -1
    else:
        context.todo_id = todo[0]['id']
        response = requests.get(url + f'/{context.todo_id}')
    context.response = response


@then('the “rest api todo list manager” returns a todo instance from the database')
def step_impl(context):
    response = requests.get(url + f'/{context.todo_id}')
    print(response)
    assert response.status_code == 200
    assert context.response.status_code == 200
    assert response.json().get("errorMessages") is None
    assert response.json().get("todos")[0].get("id") == context.todo_id


@when('the user makes a request to update a todo instance titled "{title}" with fields title "{newTitle}", doneStatus "{newDoneStatus}", and description "{newDescription}"')
def step_impl(context, title, newTitle, newDoneStatus, newDescription):
    newTodo = {}
    if newTitle != "null":
        newTodo['title'] = newTitle
    if newDoneStatus != "null":
        newTodo['doneStatus'] = json.loads(newDoneStatus)
    if newDescription != "null":
        newTodo['description'] = newDescription
    context.newTodo = newTodo
    todo_id = requests.get(url + f'?title={title}').json()['todos'][0]['id']
    response = requests.post(url + f'/{todo_id}', data=json.dumps(newTodo))
    context.response = response
    context.todo_id = todo_id


@then('the “rest api todo list manager” updates the todo instance from the database')
def step_impl(context):
    print(context.response.json())
    print(context.response.status_code)
    assert context.response.status_code == 200
    assert context.response.json().get("id") == context.todo_id
    if "newTitle" in context:
        assert context.response.json().get("title") == context.newTitle
    if "newDoneStatus" in context:
        assert context.response.json().get("doneStatus") == context.newDoneStatus
    if "newDescription" in context:
        assert context.response.json().get("description") == context.newDescription


@when('When the user makes a request to update a todo instance identified by id "<id>" with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
@when('the user makes a request to update a todo instance identified by id "{id}" with fields title "{title}", doneStatus "{doneStatus}", and description "{description}"')
def step_impl(context, id, title, doneStatus, description):
    response = requests.get(url + f'/{id}')
    context.response = response


@given('a todo with "{old_title}" and "{old_description}" exist')
def step_impl(context, old_title, old_description):
    response = requests.get(url, data=json.dumps({'title': format(old_title), 'description': format(old_description)}))
    if (response.status_code == 404):
        response = requests.post(url,
                                 data=json.dumps({'title': format(old_title), 'description': format(old_description)}))
    context.todo_id = response.json().get('todos')[0].get('id')
    assert response.status_code == 200


@when('I update the todo with "{new_title}" and "{new_description}" together')
def step_impl(context, new_title, new_description):
    context.new_title, context.new_description = new_title, new_description
    response = requests.put(url + '/' + format(context.todo_id),
                            data=json.dumps({'title': new_title, 'description': new_description}))
    context.response = response


@then("the todo is not updated")
def step_impl(context):
    assert context.response.status_code == 404

    if "new_title" in context:
        assert context.response.json().get("title") != context.new_title
    if "new_description" in context:
        assert context.response.json().get("description") != context.new_description


@when('I get the todo by "{title}" and "{description}"')
def step_impl(context, title, description):
    response = requests.get(url, data=json.dumps({'title': format(title), 'description': format(description)}))
    context.status_code = response.status_code
    context.todo = response.json().get('todos')[0]
    print(context.todo)
    context.response = response
    context.title = title


@given('a todo with description "{old_description}" exists')
def step_impl(context, old_description):
    response = requests.get(url, data=json.dumps({'description': format(old_description)}))

    if (response.status_code == 404):
        response = requests.post(url, data=json.dumps({'description': format(old_description)}))
    context.todo_id = response.json().get('todos')[0].get('id')
    context.todo = response.json().get('todos')[0]
    context.description = response.json().get('todos')[0].get('description')
    assert response.status_code == 200


@when('I update the todo with description "{new_description}"')
def step_impl(context, new_description):
    context.new_description = new_description
    response = requests.put(url + '/' + format(context.todo_id), data=json.dumps({'description': new_description}))
    context.response = response


@given('a todo with title "{old_title}" exists')
def step_impl(context, old_title):
    response = requests.get(url, data=json.dumps({'title': format(old_title)}))
    if (response.status_code == 404):
        response = requests.post(url,
                                 data=json.dumps({'title': format(old_title)}))
    context.todo_id = response.json().get('todos')[0].get('id')
    assert response.status_code == 200


@when('I update the todo with "{new_title}"')
def step_impl(context, new_title):
    context.new_title = new_title
    response = requests.put(url + '/' + format(context.todo_id),
                            data=json.dumps({'title': new_title}))
    context.response = response


@then("the todo is updated")
def step_impl(context):
    assert context.response.status_code == 200
    assert context.response.json().get("id") is not None
    if "new_title" in context:
        assert context.response.json().get("title") == context.new_title
    if "new_description" in context:
        assert context.response.json().get("description") == context.new_description


@given('a todo with "{id}" not exist')
def step_impl(context, id):
    response = requests.get(url + f'/{id}')
    assert response.status_code == 404
    context.todo_id = id


@step('the length of returned list should be "{length}"')
def step_impl(context, length):
    listLen = len(context.response.json().get('todos'))
    assert listLen==int(length)

@then('the todo instance is not deleted')
def step_impl(context):
    todo = requests.get(url + f'/{context.todo_id}')
    print(todo)
    assert todo.status_code == 200
    assert todo.json().get("id") == context.todo_id

@then('the todo instance is not created')
@then('the todo instance is deleted')
def step_impl(context):
    todo = requests.get(url + f'/{context.todo_id}')
    assert todo.status_code == 404
    assert todo.json().get("errorMessages") is not None