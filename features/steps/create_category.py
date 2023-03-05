from behave import *
import requests
import json
import subprocess

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
    ids = [category['id'] for category in categories]
    titles = [category['title'] for category in categories]
    assert context.table[0]['id'] in ids
    assert context.table[0]['title'] in titles
    assert context.table[1]['id'] in ids
    assert context.table[1]['title'] in titles
        
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
    assert error[0] == message

