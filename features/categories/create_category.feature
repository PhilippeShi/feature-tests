Feature: Create a category
    As a user
    I want to create a category
    So that I can organize my tasks by category

    Background:
        Given the application is running
        And the following categories exist
        | id | title  | description |
        | 1  | Home   |             |
        | 2  | Office |             |
        
    Scenario Outline: Create a category (Normal flow)
        Given a category with "<title>" and "<description>"
        When I create the category
        Then the category is created
        Examples:
        | title     | description       |
        | personal  | personal tasks    |
        | shopping  | shopping tasks    |
        | vacation  | vacation tasks    |


    Scenario Outline: Create a category with an existing title (Alternate flow)
        Given a category with "<title>" and "<description>"
        When I create the category
        Then the category is created
        And the new category object is different from the existing category
        Examples:
        | title  | description          |
        | Home   | Home related tasks   |
        | Office | Office related tasks |
      

    Scenario Outline: Create a category with missing description (Alternate Flow)
        Given a category with "<title>" and "<description>"
        When I create the category
        Then the category is created
        Examples:
        | title    | description|
        | title_1  | null       |
        | title_2  | null       |
        | title_3  | null       |

    Scenario Outline: Create a category with a missing title (Error flow)
        Given a category with "<title>" and "<description>"
        When I create the category
        Then the category is not created
        And an error "<message>" is returned
        Examples:
        | title | description   | message                    | 
        | null  | no title task | title : field is mandatory |

