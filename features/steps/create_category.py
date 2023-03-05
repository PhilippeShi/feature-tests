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
    for row in context.table:
        data = {'title': row['title'], 'description': row['description']}
        response = requests.post(url+'categories', data=json.dumps(data))
    
@given('A category with "{title}" and "{description}"')
def step_impl(context, title, description):
    new_category = {}
    if title != "null": new_category['title'] = title
    if description != "null": new_category['description'] = description
    context.new_category = new_category

@given('A category with no title and "{description}"')
def step_impl(context, description):
    context.new_category = {'description': description}

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

@then('the new category has a different ID from the existing category')
def step_impl(context):
    response = requests.get(url+f'categories?title={context.new_category["title"]}&description={context.new_category["description"]}')
    categories = response.json().get("categories")
    assert len(categories) > 1

@then('the category is not created')
def step_impl(context):
    assert context.response.status_code == 400

@then('an error "{message}" is returned')
def step_impl(context, message):
    error = context.response.json().get("errorMessages")
    assert len(error) == 1
    assert error[0] == message

