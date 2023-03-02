from behave import *

@given('we have behave installed')
def step_impl(context):
    pass

@given('the database is filled with the following books')
def step_impl(context):
    table_data = dict()
    table_data['Book'] = list()
    table_data['Author'] = list()
    table_data['Year'] = list()
    for row in context.table:
        table_data['Book'].append(row['Book'])
        table_data['Author'].append(row['Author'])
        table_data['Year'].append(row['Year'])

    # Save the table data in context
    context.table_data = table_data

@then('we can read the data table')
def step_impl(context):
    print(context.table_data)

@when('we implement a test')
def step_impl(context):
    assert True is not False

@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False

