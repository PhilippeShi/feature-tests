from behave import *
import requests
import json

url = 'http://localhost:4567/'

@given('the application is running')
def step_impl(context):
    res = requests.get(url+'categories')
    assert res.status_code == 200

@given('the following categories exist')
def step_impl(context):
    response = requests.get(url+'categories')
    request_data = response.json()
    categories = request_data["categories"]
    # for row in context.table:
    if context.table[0].get('id') is not None:
        ids = [category['id'] for category in categories]
        titles = [category['title'] for category in categories]
        assert context.table[0]['id'] in ids
        assert context.table[0]['title'] in titles
        assert context.table[1]['id'] in ids
        assert context.table[1]['title'] in titles
    else:
        for row in context.table:
            if row['title'] not in [category['title'] for category in categories]:
                data = {'title': row['title'], 'description': row['description']}
                res = requests.post(url+'categories', data=json.dumps(data))

        
@given('a category with "{title}" and "{description}"')
def step_impl(context, title, description):
    new_category = {}
    if title != "null": new_category['title'] = title
    if description != "null": new_category['description'] = description
    context.new_category = new_category

@when('I create the category')
def step_impl(context):
    response = requests.post(url+'categories', data=json.dumps(context.new_category))
    context.response = response

@then('the category is created')
def step_impl(context):
    context.new_category['id'] = context.response.json().get("id")
    assert context.response.status_code == 201
    assert context.response.json().get("id") is not None
    assert context.response.json().get("title") == context.new_category['title']
    if 'description' in context.new_category:
        assert context.response.json().get("description") == context.new_category['description']

@then('the new category object is different from the existing category')
def step_impl(context):
    response = requests.get(url+f'categories?title={context.new_category["title"]}')
    categories = response.json().get("categories")
    assert len(categories) > 1
    assert categories[0]['id'] != categories[1]['id']

@then('the category is not created')
def step_impl(context):
    response = requests.get(url+f'categories?description={context.new_category["description"]}')
    categories = response.json().get("categories")
    assert context.response.status_code == 400
    assert context.response.json().get("id") is None
    assert len(categories) == 0

@then('an error "{message}" is returned')
def step_impl(context, message):
    error = context.response.json().get("errorMessages")
    assert len(error) == 1
    assert message in error[0]

@when('I delete the category with "{title}" and "{description}"')
def step_impl(context, title, description):
    response = requests.get(url+f'categories?title={title}&description={description}')
    category = response.json().get("categories")
    if len(category) == 0:
        context.category_id = -1
    else:
        context.category_id = category[0]['id']
    response = requests.delete(url+f'categories/{context.category_id}')
    context.response = response

@then('the category is deleted')
def step_impl(context):
    response = requests.get(url+f'categories/{context.category_id}')
    laa = context.category_id
    context.category_id = laa
    assert response.status_code == 404
    assert response.json().get("errorMessages") is not None
    assert context.response.status_code == 200

@then('the category does not exist')
def step_impl(context):
    response = requests.get(url+f'categories/{context.category_id}')
    assert response.status_code == 404
    assert response.json().get("errorMessages") is not None

@given('a todo with "{todo_ID}" exists')
def step_impl(context, todo_ID):
    response = requests.get(url+f'todos/{todo_ID}')
    context.todo = response.json()
    context.todo_id = todo_ID
    assert response.status_code == 200

@given('a category with "{title}" and "{description}" exists')
def step_impl(context, title, description):
    response = requests.get(url+f'categories/?title={title}&description={description}')

    if response.status_code == 404:
        data = {'title': title, 'description': description}
        response = requests.post(url+'categories', data=json.dumps(data))
        context.category_id = response.json()['id']
        assert response.status_code == 201
    else:
        context.category_id = response.json()['categories'][0]['id']
        context.title = title
        context.description = description
        assert response.status_code == 200

@given('the category is assigned to the todo')
def step_impl(context):
    data = {'id': context.category_id}
    response = requests.post(url+f'todos/{context.todo_id}/categories', data=json.dumps(data))
    assert response.status_code == 201

@then('the todo is updated to have no category')
def step_impl(context):
    response = requests.get(url+f'todos/{context.todo_id}/categories')
    categories = response.json().get("categories")
    # The todo should not have the category that was deleted
    deleted_category = context.category_id
    todo_categories = [category['id'] for category in categories]
    assert deleted_category not in todo_categories

@given('a category with "{id_or_title}" exists')
def step_impl(context, id_or_title):
    # Check if the id_or_title is an string of numbers of not
    if id_or_title.strip().isdigit():
        context.category_id = id_or_title
        context.title = None
    else:
        context.title = id_or_title
        context.category_id = None

@when('I get the category by id')
def step_impl(context):
    response = requests.get(url+f'categories/{context.category_id}')
    context.response = response

@then('the response returns the category object')
def step_impl(context):
    categories = context.response.json().get("categories")
    assert len(categories) == 1
    if context.category_id is not None:
        assert int(categories[0]['id']) == int(context.category_id)
    else:
        assert categories[0]['title'] == context.title

@then('the response returns status "{code}"')
def step_impl(context, code):
    assert context.response.status_code == int(code)

@when('I get the category by title')
def step_impl(context):
    response = requests.get(url+f'categories?title={context.title}')
    context.response = response

@given('a category with "{id}" does not exist')
def step_impl(context, id):
    context.category_id = id

@when('I update the category with "{new_title}"')
def step_impl(context, new_title):
    data = {'title': new_title}
    context.new_title = new_title
    category_id = requests.get(url+f'categories?title={context.title}').json()['categories'][0]['id']
    response = requests.put(url+f'categories/{category_id}', data=json.dumps(data))
    context.response = response
    context.category_id = category_id

@then('the category is updated')
def step_impl(context):
    print(context.response.json())
    print(context.response.status_code)
    assert context.response.status_code == 200
    assert context.response.json().get("id") is not None
    if "new_title" in context:
        assert context.response.json().get("title") == context.new_title
    if "new_description" in context:
        assert context.response.json().get("description") == context.new_description

@when('I update the category with both "{new_title}" and "{new_description}"')
def step_impl(context, new_title, new_description):
    data = {}
    if new_title != "null": data['title'] = new_title
    if new_description != "null": data['description'] = new_description
    context.new_title = new_title
    context.new_description = new_description
    response = requests.put(url+f'categories/{context.category_id}', data=json.dumps(data))
    context.response = response

@given('a category with description "{old_description}" exists')
def step_impl(context, old_description):
    print("HELLOOOO")
    context.old_description = old_description
    response = requests.get(url+f'categories?description={old_description}')
    context.category_id = response.json()['categories'][0]['id']
    print("category id: " + str(context.category_id))

@when('I update the category description with "{new_description}"')
def step_impl(context, new_description):
    data = {'description': new_description}
    context.new_description = new_description
    response = requests.post(url+f'categories/{context.category_id}', data=json.dumps(data))
    context.response = response

@then('the category is not updated')
def step_impl(context):
    category = requests.get(url+f'categories/{context.category_id}').json()
    
    assert category.get("categories")[0]['description'] == context.old_description
    print(context.response.json())
