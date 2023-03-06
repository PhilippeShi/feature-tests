Feature: Delete a category
    As a user
    I want to delete a category
    So that I can remove categories that I no longer need

    Background:
        Given the application is running
        And the following categories exist
        | title  | description |
        | Home   |             |
        | Office |             |
        | Work   | works stuff |
        | Other  | other stuff |

    Scenario Outline: Delete a category (Normal flow)
        Given a category with "<title>" and "<description>"
        When I delete the category with "<title>" and "<description>"
        Then the category is deleted
        Examples:
        | title  | description |
        | Work   | works stuff |
        | Other  | other stuff |
    
    Scenario Outline: Delete a category from a todo (Alternate flow)
        Given a todo with "<todo_ID>" exists
        And a category with "<title>" and "<description>" exists
        And the category is assigned to the todo
        When I delete the category with "<title>" and "<description>"
        Then the category is deleted
        And the todo is updated to have no category
        Examples:
        | todo_ID | title  | description | 
        | 1       | Work   | Work stuff  |
        

    Scenario Outline: Delete a category that does not exist (Error flow)
        Given a category with "<title>" and "<description>" 
        When I delete the category with "<title>" and "<description>"
        Then the category does not exist
        And an error "<message>" is returned
        Examples:
        | title  | description | message |
        | Cool   | cool stuff  | Could not find any instances with categories/|
